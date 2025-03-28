from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Election, Position
from users.models import Membership
from clubs.models import Club

#@receiver(post_save, sender=Election)
#def reset_leaders_and_create_positions(sender, instance, created, **kwargs):
    
    #When a new Election is created:
    #1) Reset all existing leaders to 'member'
    #2) Create 'President' position for every club
    
    #if created:
        # 1) Reset all leaders to member
        #Membership.objects.filter(membership_type="leader").update(membership_type="member")

        # 2) Create 'President' positions for all clubs
        #all_clubs = Club.objects.all()
        #for club in all_clubs:
            #Position.objects.create(
                #name="President",
                #election=instance,
                #club=club
            #)
