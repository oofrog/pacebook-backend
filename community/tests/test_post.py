from rest_framework.test import APITestCase
from community.models import Post
from .factories import UserFactory, PostFactory


class TestPostDetail(APITestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.post = PostFactory(owner=self.user1)

    def test_get_post_detail(self):
        # not found
        response = self.client.get("/api/v1/posts/404")
        self.assertEqual(
            response.status_code,
            404,
        )
        response = self.client.get("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        self.assertEqual(
            data["payload"],
            self.post.payload,
        )

    def test_put_post(self):

        # unauth
        response = self.client.put("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            401,
        )
        # auth
        self.client.force_login(self.user2)
        # not found
        response = self.client.put("/api/v1/posts/404")
        self.assertEqual(
            response.status_code,
            404,
        )
        # permission denied
        response = self.client.put("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            403,
        )
        # permission
        # invalid data
        self.client.force_login(self.user1)
        response = self.client.put(
            "/api/v1/posts/1",
            {
                "payload": "",
            },
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertIn(
            "payload",
            data,
        )
        # valid data
        updated_data = {"payload": "updated"}
        response = self.client.put(
            "/api/v1/posts/1",
            updated_data,
        )
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            data["payload"],
            updated_data["payload"],
        )

    def test_delete_post(self):
        # unauth
        response = self.client.delete("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            401,
        )
        # auth
        self.client.force_login(self.user2)
        # not found
        response = self.client.delete("/api/v1/posts/404")
        self.assertEqual(
            response.status_code,
            404,
        )
        # permission denied
        response = self.client.delete("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            403,
        )
        self.client.force_login(self.user1)
        # happy case
        response = self.client.delete("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            204,
        )
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        response = self.client.delete("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            404,
        )
