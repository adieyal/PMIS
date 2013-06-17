import decimal
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.webdesign import lorem_ipsum
import factory
from .models import Client, District, Municipality, Programme, Project, Entity, Role, ProjectRole, ProjectFinancial, Budget, YEARS, ScopeCode, ScopeOfWork


class UserFactory(factory.Factory):
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


class ClientFactory(factory.Factory):
    FACTORY_FOR = Client
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class DistrictFactory(factory.Factory):
    FACTORY_FOR = District
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class MunicipalityFactory(factory.Factory):
    FACTORY_FOR = Municipality
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    district = factory.SubFactory(DistrictFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class ProgrammeFactory(factory.Factory):
    FACTORY_FOR = Programme
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    client = factory.SubFactory(ClientFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class ProjectFactory(factory.Factory):
    FACTORY_FOR = Project
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))
    programme = factory.SubFactory(ProgrammeFactory)
    municipality = factory.SubFactory(MunicipalityFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()


class EntityFactory(factory.Factory):
    FACTORY_FOR = Entity
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))


class RoleFactory(factory.Factory):
    FACTORY_FOR = Role
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))


class ProjectRoleFactory(factory.Factory):
    FACTORY_FOR = ProjectRole
    project = factory.SubFactory(Project)
    role = factory.SubFactory(Role)
    entity = factory.SubFactory(Entity)


class ProjectFinancialFactory(factory.Factory):
    FACTORY_FOR = ProjectFinancial
    total_anticipated_cost = decimal.Decimal(random.random() * 5000).quantize(decimal.Decimal('.01'))
    project_planning_budget = decimal.Decimal(random.random() * 5000).quantize(decimal.Decimal('.01'))
    project = factory.SubFactory(Project)


class BudgetFactory(factory.Factory):
    FACTORY_FOR = Budget
    year = random.choice(YEARS)
    allocated_budget = decimal.Decimal(random.random() * 5000).quantize(decimal.Decimal('.01'))
    project_financial = factory.SubFactory(ProjectFinancial)


class ScopeCodeFactory(factory.Factory):
    FACTORY_FOR = ScopeCode
    name = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()
    code = factory.Sequence(lambda n: u'{0}_{1}'.format(lorem_ipsum.words(1, 0), n))


class ScopeOfWorkFactory(factory.Factory):
    FACTORY_FOR = ScopeOfWork
    quantity = random.randint(0, 1000)
    scope_code = factory.SubFactory(ScopeCodeFactory)
    project = factory.SubFactory(ProjectFactory)

    @factory.lazy_attribute
    def description(self):
        return lorem_ipsum.words(200, False).capitalize()
