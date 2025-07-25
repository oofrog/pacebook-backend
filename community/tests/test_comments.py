from rest_framework.test import APITestCase
from .factories import PostFactory, UserFactory, CommentFactory


class TestComments(APITestCase):

    URL = "/api/v1/posts/"
    NUM = 3

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()
        CommentFactory.create_batch(self.NUM, post=self.post)

    def test_get_comments_not_found(self):
        response = self.client.get(f"{self.URL}{self.post.pk+1}/comments")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_get_commments_success(self):
        response = self.client.get(f"{self.URL}{self.post.pk}/comments")
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            self.NUM,
        )
        for comment in data:
            self.assertEqual(
                comment["post"]["pk"],
                self.post.pk,
            )

    def test_post_comment_not_auth(self):
        response = self.client.post(f"{self.URL}{self.post.pk}/comments")
        self.assertEqual(
            response.status_code,
            403,
        )

    def test_post_comment_not_found(self):
        self.client.force_login(self.user)
        response = self.client.post(f"{self.URL}{self.post.pk+1}/comments")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_post_comment_not_valid(self):
        self.client.force_login(self.user)
        response = self.client.post(f"{self.URL}{self.post.pk}/comments")
        self.assertEqual(
            response.status_code,
            400,
        )
        response = self.client.post(
            f"{self.URL}{self.post.pk}/comments",
            {
                "payload": "",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_post_comment_success(self):
        self.client.force_login(self.user)
        text = "test"
        response = self.client.post(
            f"{self.URL}{self.post.pk}/comments",
            {
                "payload": text,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        keys = ["user", "post", "payload"]

        for key in keys:
            self.assertIn(
                key,
                data,
            )
        self.assertEqual(
            data["user"]["pk"],
            self.user.pk,
        )
        self.assertEqual(
            data["post"]["pk"],
            self.post.pk,
        )
        self.assertEqual(
            data["payload"],
            text,
        )
