import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, F, Count
from reversion.models import Revision
import reversion


MONTHS = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)

YEARS = tuple(map(lambda x: (str(x), x), range(1960, 2060)))

class PMISUser(User):
    @property
    def projects(self):
        return Project.objects.get_project(self)

    class Meta:
        proxy=True

class Versioned(models.Model):
    revision = models.OneToOneField(Revision, related_name='versioned')  # This is required
    update_date = models.DateTimeField(auto_now=True)
    update_comment = models.TextField()
    update_user = models.ForeignKey(User)


class Client(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    district = models.ForeignKey(District, related_name='municipalities')

    def __unicode__(self):
        return self.name


class Programme(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client, related_name='programmes')

    def __unicode__(self):
        return self.name


class ProjectManager(models.Manager):
    def get_project(self, user_id=None):
        return self.annotate(cl=Count('group_perm_objs__group_perm', distinct=True)).filter(
            group_perm_objs__group_perm__in=GroupPerm.objects.filter(user__id=user_id)).annotate(
            c=Count('group_perm_objs')).distinct().filter(~Q(c=F('cl'))).distinct()


class Project(models.Model):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(blank=True)
    programme = models.ForeignKey(Programme, related_name='projects', null=True)
    municipality = models.ForeignKey(Municipality, related_name='projects', null=True)
    objects = ProjectManager()

    def __unicode__(self):
        return self.name


class Entity(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Entities"


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class ProjectRole(models.Model):
    project = models.ForeignKey(Project, related_name='project_roles')
    role = models.ForeignKey(Role, related_name='project_roles')
    entity = models.ForeignKey(Entity, related_name='project_roles', blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s: %s' % (self.project, self.role, self.entity)


class ProjectFinancial(models.Model):
    total_anticipated_cost = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    project = models.OneToOneField(Project, related_name='project_financial')

    def __unicode__(self):
        return u'Financial for %s' % self.project.name


class Budget(models.Model):
    year = models.CharField(max_length=255, choices=YEARS)
    allocated_budget = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    allocated_planning_budget = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    project = models.ForeignKey(Project, related_name='budgets')

    def __unicode__(self):
        return u'Budget for %s  for  %s year' % (self.project.name, self.year)

    class Meta:
        unique_together = ('year', 'project',)


class ScopeCode(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class ScopeOfWork(models.Model):
    quantity = models.PositiveIntegerField(null=True, blank=True)
    scope_code = models.ForeignKey(ScopeCode, related_name='scope_of_works')
    project = models.ForeignKey(Project, related_name='scope_of_works')
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'Scope of work for %s' % self.project.name

    class Meta:
        verbose_name_plural = "Scopes of Work"


class Planning(models.Model):
    month = models.CharField(max_length=255, choices=MONTHS)
    year = models.CharField(max_length=255, choices=YEARS, default=lambda: datetime.datetime.now().year)
    planned_expenses = models.FloatField(blank=True, null=True)
    planned_progress = models.FloatField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='plannings')

    def __unicode__(self):
        return u'Planning for project %s for month %s' % (self.project.name, self.month)

    class Meta:
        verbose_name_plural = "Project planning"


class Milestone(models.Model):
    PHASE = (
        ('planning', 'Planning'),
        ('implementation', 'Implementation'),
        ('completed', 'Completed')
    )
    phase = models.CharField(choices=PHASE, max_length=255)
    name = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return "%s - %s" % (self.phase, self.name)

    class Meta:
        unique_together = ('phase', 'order',)


class ProjectMilestone(models.Model):
    completion_date = models.DateField(default=datetime.datetime.now, blank=True, null=True)
    project = models.ForeignKey(Project, related_name='project_milestone')
    milestone = models.ForeignKey(Milestone, related_name='project_milestone')

    def __unicode__(self):
        return "%s - %s" % (self.project, self.milestone)


class CommentType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class MonthlySubmission(models.Model):
    month = models.CharField(max_length=255, choices=MONTHS, default=lambda: datetime.datetime.now().month)
    year = models.CharField(max_length=255, choices=YEARS, default=lambda: datetime.datetime.now().year)
    project = models.ForeignKey(Project, related_name='monthly_submissions')
    actual_expenditure = models.FloatField()
    actual_progress = models.FloatField()
    comment = models.TextField(blank=True)
    comment_type = models.ForeignKey(CommentType, related_name='submissions', null=True, blank=True)
    remedial_action = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "Submission for %s for %s/%s" % (self.project, self.year, self.month)


class ProjectStatus(models.Model):
    STATUS = (
        (0, 'Running'),
        (1, 'Terminated')
    )
    project = models.OneToOneField(Project)
    status = models.CharField(max_length=255, choices=STATUS)

    class Meta:
        verbose_name_plural = "Project statuses"


class VarianceOrder(models.Model):
    project = models.ForeignKey(Project, related_name='variance_orders')
    description = models.TextField()
    amount = models.FloatField()


class GroupPerm(models.Model):
    user = models.ManyToManyField(User, related_name='group_perms', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.name


class GroupPermObj(models.Model):
    group_perm = models.ManyToManyField(GroupPerm, related_name='group_perm_objs')
    project = models.ManyToManyField(Project, related_name='group_perm_objs')
