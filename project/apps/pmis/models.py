import datetime
from django.contrib.auth.models import User
from django.db import models
from revisions.models import VersionedModel


class Story(VersionedModel):
    update_date = models.DateTimeField(default=datetime.datetime.now())
    update_comment = models.TextField()
    update_user = models.ForeignKey(User)

    class Meta:
        abstract = True

    class Versioning:
        clear_each_revision = ['update_date', 'update_comment', 'update_user']


class Client(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class District(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    municipality = models.ForeignKey(Municipality, related_name='districts')


class Programme(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(Client, related_name='programmes')

    def __unicode__(self):
        return self.name


class Project(Story):
    name = models.CharField(max_length=255)
    description = models.TextField()
    programme = models.ForeignKey(Programme, related_name='projects', null=True)
    municipality = models.ForeignKey(Municipality, related_name='projects')
    district = models.ManyToManyField(District, related_name='projects')

    def __unicode__(self):
        return self.name


class PeopleType(models.Model):
    name = models.CharField(max_length=255)


class ProjectPeople(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='project_peoples')
    people_type = models.ManyToManyField(PeopleType, related_name='project_peoples')


class ProjectFinancial(Story):
    total_anticipated_cost = models.DecimalField(max_digits=20, decimal_places=2)
    project_planning_budget = models.DecimalField(max_digits=20, decimal_places=2)
    project = models.OneToOneField(Project)

    def __unicode__(self):
        return u'Financial for %s' % self.project.name


class Budget(Story):
    year = models.DateField()
    allocated_budget = models.DecimalField(max_digits=20, decimal_places=2)
    project_financial = models.ForeignKey(ProjectFinancial, related_name='budgets')

    def __unicode__(self):
        return u'Budget for %s  for  %s year' % (self.project_financial.project.name, self.year)


class ScopeCode(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=255, unique=True, primary_key=True)


class ScopeOfWork(Story):
    quantity = models.PositiveIntegerField()
    scope_code = models.ForeignKey(ScopeCode, related_name='scope_of_works')
    project = models.ForeignKey(Project, related_name='scope_of_works')

    def __unicode__(self):
        return u'Scope of work for %s' % self.project.name


class Planning(Story):
    month = models.CharField(max_length=255)
    planned_expanses = models.PositiveIntegerField()
    planned_progress = models.PositiveIntegerField()
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
    weeks_after_previous = models.PositiveSmallIntegerField()
    project = models.ForeignKey(Project, related_name='milestones')


class ProjectMilestone(Story):
    completion_date = models.DateTimeField(default=datetime.datetime.now())
    milestone = models.ForeignKey(Milestone, related_name='project_milestone')


class CommentType(models.Model):
    name = models.CharField(max_length=255)


class MonthlySubmission(Story):
    month = models.DateField()
    current_milestone = models.ForeignKey(Milestone, related_name='monthly_submissions')
    actual_expenditure = models.PositiveIntegerField()
    actual_progress = models.PositiveIntegerField()
    comment = models.TextField()
    comment_type = models.ForeignKey(CommentType, related_name='coment_types')
    remedial_action = models.CharField(max_length=255)
