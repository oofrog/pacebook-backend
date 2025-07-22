from rest_framework.test import APITestCase
from .factories import UserFactory, PostFactory


class TestPostDetail(APITestCase):

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.post = PostFactory(owner=self.user1)

    def test_post_not_found(self):
        response = self.client.get("/api/v1/posts/404")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_get_post_detail(self):
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
        response = self.client.put("/api/v1/posts/1")
        # unauth
        response = self.client.put("/api/v1/posts/1")
        self.assertEqual(
            response.status_code,
            403,
        )
        # auth
        # permission denied
        self.client.force_login(self.user2)
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
