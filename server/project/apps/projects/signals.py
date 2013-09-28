from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from project.apps.projects import models

@receiver(post_save, sender=models.Client, dispatch_uid="project.apps.projects.signals.add_client_to_groups")
def add_client_to_groups(**kwargs):
    instance = kwargs["instance"]

    instance_type = ContentType.objects.get_for_model(instance)

    t, create = models.GroupPerm.objects.get_or_create(
        content_type_id=instance_type.id,
        object_id=instance.id
    )
    t.name = instance.name
    t.save()


@receiver(post_save, sender=models.District, dispatch_uid="project.apps.projects.signals.add_district_to_groups")
def add_district_to_groups(**kwargs):
    instance = kwargs["instance"]

    instance_type = ContentType.objects.get_for_model(instance)

    t, create = models.GroupPerm.objects.get_or_create(
        content_type_id=instance_type.id,
        object_id=instance.id
    )

    t.name = instance.name
    t.save()


# TODO commented this out because it intermittently breaks tests - need to figure out what is going on
#@receiver(post_save, sender=models.Project, dispatch_uid="project.apps.projects.signals.create_group_perms_obj")
#def create_group_perms_obj(**kwargs):
#    instance = kwargs['instance']
#    g1 = models.GroupPerm.objects.get(name=instance.programme.client.name)
#    g2 = models.GroupPerm.objects.get(name=instance.municipality.district.name)
#    g = [g1, g2]
#    if not models.GroupPermObj.objects.filter(group_perm__in=g).annotate(c=Count('group_perm')).distinct().filter(c=len(g)).count():
#        group_perms_obj = models.GroupPermObj.objects.create()
#        group_perms_obj.group_perm.add(g1, g2)
#        group_perms_obj.project.add(instance)
#        group_perms_obj.save()
#    else:
#        group_perms_obj = models.GroupPermObj.objects.filter(group_perm__in=g).annotate(c=Count('group_perm')).distinct().filter(c=len(g)).get()
#        group_perms_obj.project.add(instance)
#        group_perms_obj.save()

def _update_is_bad(**kwargs):
    instance = kwargs["instance"]
    date = instance.date
    project = instance.project

    calc, _ = models.ProjectCalculations.objects.get_or_create(
        project=project, date=date
    )

    calc.is_bad = project.is_bad(date)
    calc.performance = project.performance(date)
    calc.most_recent_submission = project.most_recent_submission(date)
    calc.most_recent_planning= project.most_recent_planning(date)
    calc.save()

@receiver(post_save, sender=models.MonthlySubmission, dispatch_uid="project.apps.projects.signals.ms_update_is_bad")
def ms_update_is_bad(**kwargs):
    return _update_is_bad(**kwargs)

@receiver(post_save, sender=models.Planning, dispatch_uid="project.apps.projects.signals.pl_update_is_bad")
def pl_update_is_bad(**kwargs):
    return _update_is_bad(**kwargs)

@receiver(post_save, sender=models.Project, dispatch_uid="project.apps.projects.signals.ensure_has_financial")
def ensure_has_financial(**kwargs):
    try:
        instance = kwargs["instance"]
        instance.project_financial
    except models.ProjectFinancial.DoesNotExist:
        models.ProjectFinancial.objects.create(project=instance)
