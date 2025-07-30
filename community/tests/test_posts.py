from rest_framework.test import APITestCase
from users.models import User
from community.models import Post


class TestPosts(APITestCase):

    TEXT = "test desc"
    URL = "/api/v1/posts/"

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

        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "not 200")
        data = response.json()
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

    def test_create_post(self):

        # unauth
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code,
            403,
        )

        # auth
        self.client.force_login(self.user)
        # no content
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code,
            400,
        )
        # content
        response = self.client.post(
            self.URL,
            data={
                "payload": self.TEXT,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        self.assertIn(
            "owner",
            data,
        )
        self.assertEqual(
            data["owner"]["pk"],
            self.user.pk,
        )
        self.assertEqual(
            data["owner"]["username"],
            self.user.username,
        )
        self.assertIn(
            "payload",
            data,
        )
        self.assertEqual(
            data["payload"],
            self.TEXT,
        )
