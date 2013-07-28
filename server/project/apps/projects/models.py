import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, F, Count
from reversion.models import Revision


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

financial_year = range(4, 13) + range(1,4)

YEARS = tuple(map(lambda x: (str(x), x), range(2010, 2060)))


class ProjectException(Exception):
    pass

class PMISUser(User):
    @classmethod
    def from_user(cls, user):
        return PMISUser.objects.get(id=user.id)

    @property
    def projects(self):
        return Project.objects.get_project(self.id)

    class Meta:
        proxy = True

class CalendarFunctions(object):
    onemonth = relativedelta(months=1)
    @staticmethod
    def previous_year(year, month):
        return (year - 1, month)

    @staticmethod
    def next_year(year, month):
        return (year + 1, month)

    @staticmethod
    def previous_month(year, month):
        dt = datetime.datetime(year=year, month=month, day=1)
        dt2 = dt - CalendarFunctions.onemonth
        return (dt2.year, dt2.month)

    @staticmethod
    def next_month(year, month):
        dt = datetime.datetime(year=year, month=month, day=1)
        dt2 = dt + CalendarFunctions.onemonth
        return (dt2.year, dt2.month)


class FinancialYearQuerySet(QuerySet):
    previous_months = ["4", "5", "6", "7", "8", "9", "10", "11", "12"]
    current_months = ["1", "2", "3"]

    def in_financial_year(self, year):
        year = int(year)
        previous_year = year - 1
        return self.filter(
            Q(year=previous_year, month__in=FinancialYearQuerySet.previous_months) 
            | Q(year=year, month__in=FinancialYearQuerySet.current_months)
        )

class FinancialYearManager(models.Manager):
    """
    Apply to any model that is time based
    Defines the financial year which starts in April of the previous year and ends in March of the current year
    """

    previous_months = FinancialYearQuerySet.previous_months
    current_months = FinancialYearQuerySet.current_months

    def get_query_set(self):
        return FinancialYearQuerySet(self.model)

    def __getattr__(self, name):
        """
        Any method defined on our queryset is now available in our manager
        """
        return getattr(self.get_query_set(), name)

    @classmethod
    def financial_year(cls, year, month):
        return year if str(month) in FinancialYearQuerySet.current_months else year + 1

    @classmethod
    def date_in_financial_year(cls, year, dt):
        return (dt.year == year and str(dt.month) in FinancialYearManager.current_months) \
            or (dt.year + 1 == year and str(dt.month) in FinancialYearManager.previous_months)

    @classmethod
    def yearmonth_in_financial_year(cls, year, year2, month2):
        return FinancialYearManager.date_in_financial_year(year, datetime.datetime(year2, month2, 1))

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


class ProjectManagerQuerySet(QuerySet):
    def client(self, client):
        if type(client) == int:
            return self.filter(programme__client__id=client)
        else:
            return self.filter(programme__client=client)

    def municipality(self, municipality):
        if type(municipality) == int:
            return self.filter(municipality__id=municipality)
        else:
            return self.filter(municipality=municipality)

    def district(self, district):
        if type(district) == int:
            return self.filter(municipality__district__id=district)
        else:
            return self.filter(municipality__district=district)

    def programme(self, programme):
        if type(programme) == int:
            return self.filter(programme__id=programme)
        else:
            return self.filter(programme__id=programme)

    def _sort_by_performance(self, year, month, reverse):
        projects_with_plannings_for_date = self.filter(
            plannings__year__exact=year, plannings__month__exact=month
        )
        performance = lambda x : x.performance(year, month)
        return sorted(projects_with_plannings_for_date, key=performance, reverse=reverse) 

    def best_performing(self, year, month, count=5):
        return self._sort_by_performance(year, month, True)[0:count]

    def worst_performing(self, year, month, count=5):
        return self._sort_by_performance(year, month, False)[0:count]


class ProjectManager(models.Manager):
    def get_project(self, user_id=None):
        return self.annotate(cl=Count('group_perm_objs__group_perm', distinct=True)).filter(
            group_perm_objs__group_perm__in=GroupPerm.objects.filter(user__id=user_id)).annotate(
            c=Count('group_perm_objs')).distinct().filter(~Q(c=F('cl'))).distinct()

    def get_query_set(self):
        return ProjectManagerQuerySet(self.model)

    def __getattr__(self, name):
        """
        Any method defined on our queryset is now available in our manager
        """
        return getattr(self.get_query_set(), name)

class Project(models.Model):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(blank=True)
    programme = models.ForeignKey(Programme, related_name='projects', null=True)
    municipality = models.ForeignKey(Municipality, related_name='projects', null=True)
    objects = ProjectManager()

    @property
    def district(self):
        return self.municipality.district

    def __unicode__(self):
        return self.name

    def actual_progress(self, year, month):
        try:
            s = MonthlySubmission.objects.get(year=year, month=month, project=self)
            return s.actual_progress
        except MonthlySubmission.DoesNotExist:
            raise ProjectException("Could not find actual progress for %s/%s" % (year, month))

    def planned_progress(self, year, month):
        try:
            s = self.plannings.get(year=year, month=month)
            return s.planned_progress
        except Planning.DoesNotExist:
            raise ProjectException("Could not find planned progress for %s/%s" % (year, month))

    def actual_expenditure(self, year, month):
        try:
            s = MonthlySubmission.objects.get(year=year, month=month, project=self)
            return s.actual_expenditure
        except MonthlySubmission.DoesNotExist:
            raise ProjectException("Could not find actual expenditure for %s/%s" % (year, month))
            
    def planned_expenditure(self, year, month):
        try:
            s = Planning.objects.get(year=year, month=month, project=self)
            return s.planned_expenses
        except Planning.DoesNotExist:
            raise ProjectException("Could not find planned progress for %s/%s" % (year, month))

    @property
    def start_milestone(self):
        return ProjectMilestone.objects.project_start(self)

    @property
    def practical_completion_milestone(self):
        return ProjectMilestone.objects.project_practical_completion(self)

    @property
    def final_completion_milestone(self):
        return ProjectMilestone.objects.project_final_completion(self)

    @property
    def final_accounts_milestone(self):
        return ProjectMilestone.objects.project_final_accounts(self)

    # TODO implement
    @property
    def jobs(self):
        return 434343
            
        
    def performance(self, year, month):
        try:
            return self.actual_progress(year, month) / self.planned_progress(year, month)
        except ZeroDivisionError:
            return 0

    @property
    def district(self):
        return self.municipality.district



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

    def percentage_expenditure(self, year, month):
        try:
            actual = self.project.monthly_submissions.get(year=year, month=month)
            
            return float(actual.actual_expenditure) / float(self.total_anticipated_cost) * 100
        except MonthlySubmission.DoesNotExist:
            raise ProjectException("No submission exists for %s/%s" % (year, month))
        except ZeroDivisionError:
            raise ProjectException("Missing project budget - cannot calculate percentage expenditure")
            

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

    objects = FinancialYearManager()

    def __unicode__(self):
        return u'Planning for project %s for month %s' % (self.project.name, self.month)

    class Meta:
        verbose_name_plural = "Project planning"
        unique_together = ('project', 'month', 'year')


class Milestone(models.Model):
    PHASE = (
        ('planning', 'Planning'),
        ('implementation', 'Implementation'),
        ('completed', 'Completed')
    )
    phase = models.CharField(choices=PHASE, max_length=255)
    name = models.CharField(max_length=255)
    order = models.PositiveSmallIntegerField()

    @classmethod
    def start_milestone(cls):
        return Milestone.objects.get(name="Project Identification")

    @classmethod
    def practical_completion(cls):
        return Milestone.objects.get(name="Practical Completion")

    @classmethod
    def final_completion(cls):
        return Milestone.objects.get(name="Final Completion")

    @classmethod
    def final_accounts(cls):
        return Milestone.objects.get(name="Final Accounts")

    def __unicode__(self):
        return "%s - %s" % (self.phase, self.name)

    class Meta:
        unique_together = ('phase', 'order',)


class ProjectMilestoneManager(models.Manager):
    def project_start(self, project):
        return project.milestones.get(milestone=Milestone.start_milestone())

    def project_practical_completion(self, project):
        return project.milestones.get(milestone=Milestone.practical_completion())
    
    def project_final_completion(self, project):
        return project.milestones.get(milestone=Milestone.final_completion())

    def project_final_accounts(self, project):
        return project.milestones.get(milestone=Milestone.final_accounts())

class ProjectMilestone(models.Model):
    completion_date = models.DateField(default=datetime.datetime.now, blank=True, null=True)
    project = models.ForeignKey(Project, related_name='milestones')
    milestone = models.ForeignKey(Milestone, related_name='project_milestone')

    objects = ProjectMilestoneManager()

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

    objects = FinancialYearManager()

    def __unicode__(self):
        return "Submission for %s for %s/%s" % (self.project, self.year, self.month)

    class Meta:
        unique_together = ('project', 'month', 'year')


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

    def __unicode__(self):
        projects = self.project.all()
        s_projects = " ".join(map(str, projects))
        perms = self.group_perm.all()
        s_perms = ", ".join(map(str, perms))
        return "%s (%s)" % (s_projects, s_perms)
