from rest_framework.test import APITestCase
from users.models import User
from community.models import Post


class TestPosts(APITestCase):

    TEXT = "test desc"

    def setUp(self):
        user = User.objects.create(
            username="testuser",
        )
        user.set_password("0000")
        user.save()
        self.user = user

        Post.objects.create(
            owner=user,
            payload=self.TEXT,
        )

    def test_get_posts(self):

        response = self.client.get("/api/v1/posts/")
        self.assertEqual(response.status_code, 200, "not 200")
        data = response.data
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["owner"],
            self.user.pk,
        )
        self.assertEqual(
            data[0]["payload"],
            self.TEXT,
        )
