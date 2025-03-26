import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from messaging.models import ChatRoom, Message, DirectChatRoom, DirectMessage
from polls.models import Poll, PollVote, Choice
from users.models import Membership
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]
            self.room_group_name = f"chat_{self.room_slug}"
            self.user = self.scope["user"]

            self.room = await sync_to_async(ChatRoom.objects.select_related("club").get)(slug=self.room_slug)
            club = self.room.club

            is_member = await sync_to_async(Membership.objects.filter(
                user=self.user,
                club=club,
                membership_type__in=["member", "leader"]
            ).exists)()

            if not self.user.is_authenticated or not is_member:
                await self.close()
                return

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            print("WebSocket connection error:", e)
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()

            # --- Handle new chat message ---
            if message:
                new_message = await sync_to_async(Message.objects.create)(
                    sender=self.user,
                    room=self.room,
                    content=message
                )

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": message,
                        "sender": self.user.name,
                        "sender_id": self.user.id,
                        "profile_picture": self.user.profile_picture.url if self.user.profile_picture else "",
                        "timestamp": new_message.timestamp.strftime("%H:%M"),
                    }
                )

            # --- Handle real-time vote ---
            if "vote_poll_id" in data and "vote_choice_id" in data:
                poll_id = int(data["vote_poll_id"])
                choice_id = int(data["vote_choice_id"])

                already_voted = await sync_to_async(PollVote.objects.filter(
                    poll_id=poll_id, user=self.user).exists)()

                if not already_voted:
                    await sync_to_async(PollVote.objects.create)(
                        poll_id=poll_id, choice_id=choice_id, user=self.user
                    )

                    # ✅ Increment vote count
                    choice = await sync_to_async(Choice.objects.get)(id=choice_id)
                    choice.vote_count += 1
                    await sync_to_async(choice.save)()

                    # ✅ Broadcast poll update to all clients
                    choices = await sync_to_async(list)(Choice.objects.filter(poll_id=poll_id))
                    choice_data = [
                        {"id": c.id, "text": c.text, "vote_count": c.vote_count}
                        for c in choices
                    ]

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "poll_update",
                            "poll_id": poll_id,
                            "choices": choice_data,
                            "user_id": self.user.id,
                            "user_choice_id": choice_id,
                        }
                    )

            # --- Handle real-time poll creation ---
            if "new_poll_question" in data and "new_poll_choices" in data:
                question = data["new_poll_question"]
                choices = data["new_poll_choices"]
                club = self.room.club

                is_leader = await sync_to_async(Membership.objects.filter(
                    user=self.user,
                    club=club,
                    membership_type="leader"
                ).exists)()

                if not is_leader:
                    return  # Only leaders can create polls

                new_poll = await sync_to_async(Poll.objects.create)(
                    club=club,
                    question=question,
                    created_by=self.user,
                    is_active=True
                )

                choice_objs = []
                for text in choices:
                    if text.strip():
                        choice = await sync_to_async(Choice.objects.create)(poll=new_poll, text=text.strip())
                        choice_objs.append({
                            "id": choice.id,
                            "text": choice.text,
                            "vote_count": 0
                        })

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "new_poll_broadcast",
                        "poll_id": new_poll.id,
                        "question": new_poll.question,
                        "choices": choice_objs,
                    }
                )

        except Exception as e:
            print("Error in receive():", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "sender": event["sender"],
            "sender_id": event["sender_id"],
            "profile_picture": event["profile_picture"],
            "timestamp": event["timestamp"]
        }))

    async def poll_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "poll_update",
            "poll_id": event["poll_id"],
            "choices": event["choices"],
            "user_id": event["user_id"],
            "user_choice_id": event["user_choice_id"]
        }))

    async def new_poll_broadcast(self, event):
        await self.send(text_data=json.dumps({
            "type": "new_poll",
            "poll_id": event["poll_id"],
            "question": event["question"],
            "choices": event["choices"]
        }))


class DirectChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_name = f"dm_{min(self.user.id, int(self.other_user_id))}_{max(self.user.id, int(self.other_user_id))}"
        self.room_group_name = f"chat_{self.room_name}"

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        other_user = await sync_to_async(User.objects.get)(id=self.other_user_id)

        room, _ = await sync_to_async(DirectChatRoom.get_or_create_between_users)(self.user, other_user)
        msg = await sync_to_async(DirectMessage.objects.create)(
            room=room,
            sender=self.user,
            receiver=other_user,
            content=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user.id,
                "sender": self.user.name,
                "profile_picture": self.user.profile_picture.url if self.user.profile_picture else "",
                "timestamp": msg.timestamp.strftime("%H:%M"),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
