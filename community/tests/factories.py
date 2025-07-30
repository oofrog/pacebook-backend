import factory
from users.models import User
from community.models import Post,Comment, Like

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpass")

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    owner = factory.SubFactory(UserFactory)
    payload = factory.Faker('sentence')

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    payload = factory.Faker('sentence')

class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Like
    
    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)