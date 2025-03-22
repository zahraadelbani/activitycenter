import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Election, Candidate

class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.election_id = self.scope['url_route']['kwargs']['election_id']
        self.room_group_name = f"election_{self.election_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def vote_update(self, event):
        candidates = await Candidate.objects.filter(election_id=self.election_id).all()
        data = [
            {"name": c.user.name, "position": c.position.name, "votes": c.votes}
            for c in candidates
        ]
        await self.send(text_data=json.dumps({"candidates": data}))
