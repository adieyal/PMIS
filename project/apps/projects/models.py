import datetime
from django.contrib.auth.models import User
from django.db import models
from revisions.models import VersionedModel


MONTHS = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'July'),
    (9, 'August'),
    (10, 'September'),
    (11, 'October'),
    (12, 'November'),
    (13, 'December'),
)

YEARS = tuple(map(lambda x: (x, x), range(1960, 2060)))


class Versioned(VersionedModel):
    update_date = models.DateTimeField(default=datetime.datetime.now())
    update_comment = models.TextField()
    update_user = models.ForeignKey(User)

    class Meta:
        abstract = True

    class Versioning:
        clear_each_revision = ['update_date', 'update_comment', 'update_user']


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
    description = models.TextField()
    client = models.ForeignKey(Client, related_name='programmes')

    def __unicode__(self):
        return self.name


class Project(Versioned):
    name = models.CharField(max_length=255)
    description = models.TextField()
    programme = models.ForeignKey(Programme, related_name='projects', null=True)
    municipality = models.ForeignKey(Municipality, related_name='projects')

    def __unicode__(self):
        return self.name


class Entity(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class ProjectRole(models.Model):
    project = models.ForeignKey(Project, related_name='project_roles')
    role = models.ForeignKey(Role, related_name='project_roles')
    entity = models.ForeignKey(Entity, related_name='project_roles')


class ProjectFinancial(Versioned):
    total_anticipated_cost = models.DecimalField(max_digits=20, decimal_places=2)
    project_planning_budget = models.DecimalField(max_digits=20, decimal_places=2)
    project = models.OneToOneField(Project)

    def __unicode__(self):
        return u'Financial for %s' % self.project.name


class Budget(Versioned):
    year = models.CharField(max_length=255, choices=YEARS)
    allocated_budget = models.DecimalField(max_digits=20, decimal_places=2)
    project_financial = models.ForeignKey(ProjectFinancial, related_name='budgets')

    def __unicode__(self):
        return u'Budget for %s  for  %s year' % (self.project_financial.project.name, self.year)


class ScopeCode(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class ScopeOfWork(Versioned):
    quantity = models.PositiveIntegerField()
    scope_code = models.ForeignKey(ScopeCode, related_name='scope_of_works')
    project = models.ForeignKey(Project, related_name='scope_of_works')

    def __unicode__(self):
        return u'Scope of work for %s' % self.project.name


class Planning(Versioned):
    month = models.CharField(max_length=255, choices=MONTHS)
    year = models.CharField(max_length=255, choices=YEARS, default=datetime.datetime.now().year)
    planned_expenses = models.FloatField()
    planned_progress = models.FloatField()
    project = models.ForeignKey(Project, related_name='plannings')

    def __unicode__(self):
        return u'Planning for project %s for month %s' % (self.project.name, self.month)


class Milestone(models.Model):
    PHASE = (
        (0, 'Planning'),
        (1, 'Implementation'),
        (2, 'Completed')
    )
    phase = models.CharField(choices=PHASE, max_length=255)
    name = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name


class ProjectMilestone(Versioned):
    completion_date = models.DateTimeField(default=datetime.datetime.now())
    project = models.ForeignKey(Project, related_name='project_milestone')


class CommentType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class MonthlySubmission(Versioned):
    month = models.CharField(max_length=255, choices=MONTHS, default=datetime.datetime.now().month)
    year = models.CharField(max_length=255, choices=YEARS, default=datetime.datetime.now().year)
    project = models.ForeignKey(Project, related_name='monthly_submissions')
    actual_expenditure = models.FloatField()
    actual_progress = models.FloatField()
    comment = models.TextField()
    comment_type = models.ForeignKey(CommentType, related_name='monthly_submissions')
    remedial_action = models.CharField(max_length=255)


class ProjectStatus(Versioned):
    STATUS = (
        (0, 'Running'),
        (1, 'Terminated')
    )
    project = models.OneToOneField(Project)
    status = models.CharField(max_length=255, choices=STATUS)


class VarianceOrder(Versioned):
    project = models.ForeignKey(Project, related_name='variance_orders')
    description = models.TextField()
    amount = models.FloatField()