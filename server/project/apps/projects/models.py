from __future__ import division
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q, F, Count
from reversion.models import Revision
from django.db.models import Sum, Avg


financial_year = range(4, 13) + range(1,4)

YEARS = tuple(map(lambda x: (str(x), x), range(2010, 2060)))
onemonth = relativedelta(months=1)

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
    @staticmethod
    def previous_year(year, month):
        return (year - 1, month)

    @staticmethod
    def next_year(year, month):
        return (year + 1, month)

    @staticmethod
    def previous_month(year, month):
        dt = datetime.datetime(year=year, month=month, day=1)
        dt2 = dt - onemonth
        return (dt2.year, dt2.month)

    @staticmethod
    def next_month(year, month):
        dt = datetime.datetime(year=year, month=month, day=1)
        dt2 = dt + onemonth
        return (dt2.year, dt2.month)


class FinancialYearQuerySet(QuerySet):
    previous_months = [4, 5, 6, 7, 8, 9, 10, 11, 12]
    current_months = [1, 2, 3]

    def month_in(self, months, field='date'):
        q = Q()
        for m in months:
           q |= Q(**{field + '__month': m})
        return q

    def in_financial_year(self, dt):
        year = FinancialYearManager.financial_year(dt.year, dt.month)
        previous_year = year - 1
        return self.filter(
            (Q(date__year=previous_year) & self.month_in(FinancialYearQuerySet.previous_months)) |\
            (Q(date__year=year) & self.month_in(FinancialYearQuerySet.current_months))
        )

class FinancialYearManager(models.Manager):
    """
    Apply to any model that is time based
    Defines the financial year which starts in April of the previous year and ends in March of the current year
    """

    previous_months = FinancialYearQuerySet.previous_months
    current_months = FinancialYearQuerySet.current_months
    oneday = relativedelta(days=1)

    def get_query_set(self):
        return FinancialYearQuerySet(self.model)

    def __getattr__(self, name):
        """
        Any method defined on our queryset is now available in our manager
        """
        return getattr(self.get_query_set(), name)

    @classmethod
    def financial_year(cls, year, month):
        return year if month in FinancialYearQuerySet.current_months else year + 1

    @classmethod
    def date_in_financial_year(cls, year, dt):
        return (dt.year == year and dt.month in FinancialYearManager.current_months) \
            or (dt.year + 1 == year and dt.month in FinancialYearManager.previous_months)

    @classmethod
    def start_of_year(cls, year):
        return datetime.datetime(year - 1, cls.previous_months[0], 1)

    @classmethod
    def end_of_year(cls, year):
        dt = datetime.datetime(year, cls.previous_months[0], 1)
        return dt - cls.oneday
        

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
        return "%s - %s" % (self.name, self.client)

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
    def consultant_milestone(cls):
        return Milestone.objects.get(name="Consultant appointment")

    @classmethod
    def design_milestone(cls):
        return Milestone.objects.get(name="Design and Costing")

    @classmethod
    def documentation_milestone(cls):
        return Milestone.objects.get(name="Documentation")

    @classmethod
    def tendering_milestone(cls):
        return Milestone.objects.get(name="Tendering")
 
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

class ProjectQuerySet(QuerySet):

    @property
    def fy(self):
        self.__class__ = FYProjectQuerySet
        return self

    @property
    def alltime(self):
        self.__class__ = AllProjectQuerySet
        return self

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

    def actual_progress_between(self, progress_start, progress_end):
        return self.filter(
            monthly_submissions__actual_progress__gte=progress_start,
            monthly_submissions__actual_progress__lt=progress_end,
        )

    def planned_progress_between(self, progress_start, progress_end):
        return self.filter(
            monthly_submissions__actual_progress__gte=progress_start,
            monthly_submissions__actual_progress__lt=progress_end,
        )

    def _sort_by_performance(self, date, reverse=False):
        order_field = "calculations__performance"
        if reverse:
            order_field = "-" + order_field

        return self.filter(
            calculations__project__in=self,
            calculations__date__year=date.year,
            calculations__date__month=date.month,
        ).order_by(order_field)

    def best_performing(self, date, count=5):
        return self._sort_by_performance(date, True)[0:count]

    def worst_performing(self, date, count=5):
        return self._sort_by_performance(date)[0:count]

    def bad(self, date):
        return self.filter(calculations__project__in=self, calculations__is_bad=True)


    def completed_by_fye(self, year):
        ystart = FinancialYearManager.start_of_year(year)
        yend = FinancialYearManager.end_of_year(year)

        return self.due_by(yend)

    def due_by(self, date):
        return self.filter(milestones__milestone=Milestone.practical_completion(), milestones__completion_date__lte=date)

    def due_in_3_months(self, date):
        dt = date + 3 * onemonth
        return self.filter(milestones__milestone=Milestone.practical_completion(), milestones__completion_date__lte=dt)

    def due_in_1_month(self, date):
        dt = date + onemonth
        return self.filter(milestones__milestone=Milestone.practical_completion(), milestones__completion_date__lte=dt)

    @property
    def in_planning(self):
        return self.filter(current_step__phase="planning")

    @property
    def in_implementation(self):
        return self.filter(current_step__phase="implementation")

    @property
    def in_practicalcompletion(self):
        return self.filter(current_step=Milestone.final_completion())

    @property
    def in_finalcompletion(self):
        return self.filter(current_step=Milestone.final_accounts())

    def total_budget(self):
        
        val =  self.aggregate(Sum("project_financial__total_anticipated_cost"))["project_financial__total_anticipated_cost__sum"]
        if val == None:
            return 0
        return val

    def average_actual_progress(self, date):
        # TODO - rather than using an exact date - should get the most recent submission
        res = MonthlySubmission.objects\
            .filter(project__in=self, date__year=date.year, date__month=date.month)\
            .aggregate(Avg("actual_progress"))
        return res["actual_progress__avg"] or 0
        
    def average_planned_progress(self, date):
        # TODO - rather than using an exact date - should get the most recent submission
        res = Planning.objects\
            .filter(project__in=self, date__year=date.year, date__month=date.month)\
            .aggregate(Avg("planned_progress"))
        return res["planned_progress__avg"] or 0

    def total_planned_expenditure(self, date):
        expenditure = Planning.objects\
            .filter(project__in=self, date__lte=date)\
            .aggregate(Sum("planned_expenses"))["planned_expenses__sum"]

        if expenditure == None:
            return 0
        return expenditure

class ProjectManager(models.Manager):
    def get_project(self, user_id=None):
        return self.annotate(cl=Count('group_perm_objs__group_perm', distinct=True)).filter(
            group_perm_objs__group_perm__in=GroupPerm.objects.filter(user__id=user_id)).annotate(
            c=Count('group_perm_objs')).distinct().filter(~Q(c=F('cl'))).distinct()

    def get_query_set(self):
        return ProjectQuerySet(self.model)

    def __getattr__(self, name):
        """
        Any method defined on our queryset is now available in our manager
        """
        return getattr(self.get_query_set(), name)

class FYProjectQuerySet(ProjectQuerySet):
    def actual_expenditure(self, date):
        return MonthlySubmission.objects.filter(project__in=self).fyexpenditure(date)

    def percentage_actual_expenditure(self, date):
        actual_expenditure = self.actual_expenditure(date)
        budget = self.total_budget()
        if budget == 0:
            return 0

        return (actual_expenditure / budget) * 100

class AllProjectQuerySet(ProjectQuerySet):
    def actual_expenditure(self, date):
        prevexp = ProjectFinancial.objects\
            .filter(project__in=self)\
            .aggregate(Sum("previous_expenses"))["previous_expenses__sum"]

        expenditure = MonthlySubmission.objects.filter(project__in=self).expenditure(date)
        
        if not prevexp: prevexp = 0
        if not expenditure: expenditure = 0

        return float(prevexp) + expenditure

    def percentage_actual_expenditure(self, date):
        actual_expenditure = self.actual_expenditure(date)
        budget = self.total_budget()
        if budget == 0:
            return 0

        return (actual_expenditure / budget) * 100

class Project(models.Model):
    name = models.CharField(max_length=255)
    project_number = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(blank=True)
    programme = models.ForeignKey(Programme, related_name='projects', null=True)
    municipality = models.ForeignKey(Municipality, related_name='projects', null=True)
    current_step = models.ForeignKey(Milestone, null=True, help_text="Next milestone that this project must meet")
    # TODO - at some point we will need to actually only return active projects - we could add another manager to do this
    # e.g. Project.active.average_progress
    objects = ProjectManager()

    class _FY(object):
        def __init__(self, project, date):
            self.project = project
            self.date = date
        
        @property
        def actual_expenditure(self):
            return MonthlySubmission.objects.filter(project=self.project).fyexpenditure(self.date)

        @property
        def planned_expenditure(self):
            return Planning.objects.filter(project=self.project).fyexpenditure(self.date)
        
        def __getattr__(self, attr):
            return getattr(self.project, name)

    class _ALL(object):
        def __init__(self, project, date):
            self.project = project
            self.date = date
        
        @property
        def actual_expenditure(self):
            actual_expenditure = MonthlySubmission.objects.filter(project=self.project).expenditure(self.date)
            try:
                previous_years = self.project_financial.previous_expenses
            except ProjectFinancial.DoesNotExist:
                previous_years = 0
            return actual_expenditure + previous_years
        
        def __getattr__(self, attr):
            return getattr(self.project, attr)

    def fy(self, dt):
        return Project._FY(self, dt)

    def all(self, dt):
        return Project._ALL(self, dt)

    @property
    def district(self):
        return self.municipality.district

    def actual_progress(self, date):
        try:
            submissions = MonthlySubmission.objects.filter(date__lte=date, project=self).order_by("-date")
            most_recent_submission = submissions[0]
            return most_recent_submission.actual_progress
        except IndexError:
            return 0

    def planned_progress(self, date):
        try:
            plannings = Planning.objects.filter(date__lte=date, project=self).order_by("-date")
            most_recent_planning = plannings[0]
            return most_recent_planning.planned_progress
        except IndexError:
            return 0

    def is_bad(self, date, progress_threshold=10):
        # TODO need to figure out how to do this more efficiently
        if self.planned_progress(date) - self.actual_progress(date) > progress_threshold:
            return True
        return False

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
            
    def performance(self, date):
        try:
            return self.actual_progress(date) / self.planned_progress(date)
        except ZeroDivisionError:
            return 0

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
    total_anticipated_cost = models.FloatField(default=0)
    previous_expenses = models.FloatField(default=0)
    final_accounts = models.FloatField(null=True, blank=True)
    project = models.OneToOneField(Project, related_name='project_financial')


    def percentage_expenditure(self, date):
        try:
            actual = self.project.fy(date).actual_expenditure
            
            return actual / float(self.total_anticipated_cost) * 100
        except (MonthlySubmission.DoesNotExist, ZeroDivisionError):
            return 0

    def __unicode__(self):
        return u'Financial for %s' % self.project.name


class Budget(models.Model):
    year = models.CharField(max_length=255, choices=YEARS)
    allocated_budget = models.FloatField(default=0)
    allocated_planning_budget = models.FloatField(default=0)
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

class PlanningQuerySet(FinancialYearQuerySet):
    def fyexpenditure(self, date):
        return self.in_financial_year(date).expenditure(date)

    def expenditure(self, date):
        s = self.filter(date__lte=date).aggregate(Sum("planned_expenses"))
        return s["planned_expenses__sum"] or 0

class PlanningManager(FinancialYearManager):
    def get_query_set(self):
        return PlanningQuerySet(self.model)

class Planning(models.Model):
    date = models.DateTimeField(default=lambda : datetime.datetime.now())
    planned_expenses = models.FloatField(blank=True, null=True)
    planned_progress = models.FloatField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='plannings')

    objects = PlanningManager()

    def __unicode__(self):
        return u'Planning for project %s for month %s' % (self.project.name, self.date.month)

    class Meta:
        verbose_name_plural = "Project planning"
        # How can this been done?
        #unique_together = ('project', 'date__month', 'date.year')


class ProjectMilestoneManager(models.Manager):
    def _return_milestone(self, project, milestone):
        try:
            return project.milestones.get(milestone=milestone)
        except ProjectMilestone.DoesNotExist:
            # TODO If a project is missing a start date - return a factitious date
            # so sue me - this is the simplest thing that can work. Wait for
            # client recommendation
            import factories
            return factories.ProjectMilestoneFactory.build()

    def project_start(self, project):
        return self._return_milestone(project, Milestone.start_milestone())

    def project_practical_completion(self, project):
        return self._return_milestone(project, Milestone.practical_completion())
    
    def project_final_completion(self, project):
        return self._return_milestone(project, Milestone.final_completion())

    def project_final_accounts(self, project):
        return self._return_milestone(project, Milestone.final_accounts())

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

class MonthlySubmissionQuerySet(FinancialYearQuerySet):
    def fyexpenditure(self, date):
        return self.in_financial_year(date).expenditure(date)

    def expenditure(self, date):
        s = self\
            .filter(date__lte=date)\
            .aggregate(Sum("actual_expenditure"))
        return s["actual_expenditure__sum"] or 0

class MonthlySubmissionManager(FinancialYearManager):
    def get_query_set(self):
        return MonthlySubmissionQuerySet(self.model)

class MonthlySubmission(models.Model):
    date = models.DateTimeField(default=lambda : datetime.datetime.now())
    project = models.ForeignKey(Project, related_name='monthly_submissions')
    actual_expenditure = models.FloatField(help_text="Actual expenditure this month")
    actual_progress = models.FloatField(help_text="Actual progress at this point")
    comment = models.TextField(blank=True)
    comment_type = models.ForeignKey(CommentType, related_name='submissions', null=True, blank=True)
    remedial_action = models.CharField(max_length=255, blank=True)

    objects = MonthlySubmissionManager()

    def __unicode__(self):
        return "Submission for %s for %s/%s" % (self.project, self.date.year, self.date.month)

    class Meta:
        # How can this been done?
        #unique_together = ('project', 'date__month', 'date.year')
        pass

class ProjectCalculations(models.Model):
    date = models.DateTimeField(default=lambda : datetime.datetime.now())
    project = models.ForeignKey(Project, related_name='calculations')
    is_bad = models.NullBooleanField(null=True)
    performance = models.FloatField(null=True)

    def __unicode__(self):
        return unicode(self.project)

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
