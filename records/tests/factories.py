import factory
from users.models import User
from records.models import Record

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass")

class RecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Record

    owner = factory.SubFactory(UserFactory)
    duration_sec = factory.Faker("pyint", min_value=600, max_value=7200)
    distance_m = factory.Faker("pyint", min_value=1000, max_value=20000)
    pace = factory.Faker("pyint", min_value=180, max_value=600)
    kcal = factory.Faker("pyint", min_value=50, max_value=1000)
    route = factory.Faker("text", max_nb_chars=200)