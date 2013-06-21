import decimal
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum
import factory
from .models import Client, District, Municipality, Programme, Project, Entity, Role, ProjectRole, ProjectFinancial, Budget, YEARS, ScopeCode, ScopeOfWork, Planning, MONTHS, Milestone, ProjectMilestone, CommentType, MonthlySubmission, ProjectStatus, VarianceOrder
from datetime import date


class UserFactory(factory.DjangoModelFactory):
    """Represents user factories"""

    FACTORY_FOR = User

    username = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    email = factory.LazyAttribute(lambda a: u'{0}@localhost.local'.format(a.username))
    password = make_password('qwerty', hasher="pbkdf2_sha256")

    @factory.lazy_attribute
    def first_name(self):
        return lorem_ipsum.words(1, False).capitalize()

    @factory.lazy_attribute
    def last_name(self):
        return lorem_ipsum.words(1, False).capitalize()

        # @classmethod
        # def _prepare(cls, create, **kwargs):
        #     user = super(UserFactory, cls)._prepare(create, **kwargs)
        #     for k, v in UserProfileFactory.attributes().iteritems():
        #         setattr(user.profile, k, v)
        #     user.profile.save()
        #     return user


class AdminFactory(UserFactory):
    """Represents admin user factories"""

    username = 'admin'
    password = make_password('admin', hasher="pbkdf2_sha256")
    email = 'admin@example.com'
    is_active = True
    is_staff = True
    is_superuser = True


class ClientFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Client
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class DistrictFactory(factory.DjangoModelFactory):
    FACTORY_FOR = District
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class MunicipalityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Municipality
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    district = factory.SubFactory(DistrictFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class ProgrammeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Programme
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    client = factory.SubFactory(ClientFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    programme = factory.SubFactory(ProgrammeFactory)
    municipality = factory.SubFactory(MunicipalityFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class EntityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Entity
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))


class RoleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Role
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))


class ProjectRoleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProjectRole
    project = factory.SubFactory(Project)
    role = factory.SubFactory(Role)
    entity = factory.SubFactory(Entity)


class ProjectFinancialFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProjectFinancial
    total_anticipated_cost = decimal.Decimal(random.random() * 5000).quantize(decimal.Decimal('.01'))
    project_planning_budget = decimal.Decimal(random.random() * 5000).quantize(decimal.Decimal('.01'))
    project = factory.SubFactory(Project)


class BudgetFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Budget
    year = random.choice(YEARS)
    allocated_budget = decimal.Decimal(random.random() * 5000).quantize(decimal.Decimal('.01'))
    project_financial = factory.SubFactory(ProjectFinancial)


class ScopeCodeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ScopeCode
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()

    code = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))


class ScopeOfWorkFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ScopeOfWork
    quantity = random.randint(0, 1000)
    scope_code = factory.SubFactory(ScopeCodeFactory)
    project = factory.SubFactory(ProjectFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class PlanningFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Planning
    month = random.choice(MONTHS)
    year = random.choice(YEARS)
    planned_expenses = random.randint(0, 100)
    planned_progress = random.randint(0, 100)
    project = factory.SubFactory(ProjectFactory)


class MilestoneFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Milestone
    phase = random.choice(Milestone.PHASE)
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    order = random.randint(0, 100)


class ProjectMilestoneFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProjectMilestone
    completion_date = date.fromordinal(
        random.randint(date.today().replace(day=1, month=1).toordinal(), date.today().toordinal()))
    project = factory.SubFactory(ProjectFactory)
    milestone = factory.SubFactory(MilestoneFactory)


class CommentTypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CommentType
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))


class MonthlySubmissionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MonthlySubmission
    month = random.choice(MONTHS)
    year = random.choice(YEARS)
    project = factory.SubFactory(ProjectFactory)
    actual_expenditure = random.randint(0, 100)
    actual_progress = random.randint(0, 100)
    comment = lorem_ipsum.words(5, False)
    comment_type = factory.SubFactory(CommentTypeFactory)
    remedial_action = lorem_ipsum.words(5, False)


class ProjectStatusFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProjectStatus
    project = factory.SubFactory(ProjectFactory)
    status = random.choice(ProjectStatus.STATUS)


class VarianceOrderFactory(factory.DjangoModelFactory):
    FACTORY_FOR = VarianceOrder
    project = factory.SubFactory(ProjectFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()

    amount = random.random()*1000
