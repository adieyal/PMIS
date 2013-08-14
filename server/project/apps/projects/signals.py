from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from project.apps.projects.models import Client, District, GroupPerm, Project, GroupPermObj


@receiver(post_save, sender=Client, dispatch_uid="project.apps.projects.signals.add_client_to_groups")
def add_client_to_groups(**kwargs):
    instance = kwargs['instance']

    instance_type = ContentType.objects.get_for_model(instance)

    t, create = GroupPerm.objects.get_or_create(
        content_type_id=instance_type.id,
        object_id=instance.id
    )
    t.name = instance.name
    t.save()


@receiver(post_save, sender=District, dispatch_uid="project.apps.projects.signals.add_district_to_groups")
def add_district_to_groups(**kwargs):
    instance = kwargs['instance']

    instance_type = ContentType.objects.get_for_model(instance)

    t, create = GroupPerm.objects.get_or_create(
        content_type_id=instance_type.id,
        object_id=instance.id
    )

    t.name = instance.name
    t.save()


# TODO commented this out because it intermittently breaks tests - need to figure out what is going on
#@receiver(post_save, sender=Project, dispatch_uid="project.apps.projects.signals.create_group_perms_obj")
#def create_group_perms_obj(**kwargs):
#    instance = kwargs['instance']
#    g1 = GroupPerm.objects.get(name=instance.programme.client.name)
#    g2 = GroupPerm.objects.get(name=instance.municipality.district.name)
#    g = [g1, g2]
#    if not GroupPermObj.objects.filter(group_perm__in=g).annotate(c=Count('group_perm')).distinct().filter(c=len(g)).count():
#        group_perms_obj = GroupPermObj.objects.create()
#        group_perms_obj.group_perm.add(g1, g2)
#        group_perms_obj.project.add(instance)
#        group_perms_obj.save()
#    else:
#        group_perms_obj = GroupPermObj.objects.filter(group_perm__in=g).annotate(c=Count('group_perm')).distinct().filter(c=len(g)).get()
#        group_perms_obj.project.add(instance)
#        group_perms_obj.save()
