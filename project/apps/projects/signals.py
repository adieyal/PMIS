from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from project.apps.projects.models import Client, District


@receiver(post_save, sender=Client)
def add_client_to_groups(**kwargs):
    instance = kwargs['instance']
    group, create = Group.objects.get_or_create(name=instance.name)
    group.save()


@receiver(post_save, sender=District)
def add_district_to_groups(**kwargs):
    instance = kwargs['instance']
    group, create = Group.objects.get_or_create(name=instance.name)
    group.save()