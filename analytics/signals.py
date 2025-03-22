from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from clubs.models import Event
from polls.models import Poll
from users.models import Membership
from .models import ClubAnalytics


def update_analytics_for_club(club):
    """Utility to create or update analytics for a given club."""
    analytics, created = ClubAnalytics.objects.get_or_create(club=club)
    analytics.update_stats()


@receiver(post_save, sender=Membership)
@receiver(post_delete, sender=Membership)
def membership_changed(sender, instance, **kwargs):
    update_analytics_for_club(instance.club)


@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def event_changed(sender, instance, **kwargs):
    update_analytics_for_club(instance.club)


@receiver(post_save, sender=Poll)
@receiver(post_delete, sender=Poll)
def poll_changed(sender, instance, **kwargs):
    update_analytics_for_club(instance.club)
