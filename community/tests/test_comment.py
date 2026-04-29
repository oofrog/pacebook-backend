from rest_framework.test import APITestCase
from . import factories
from community.models import Comment


class TestPatchComment(APITestCase):

    def setUp(self):
        self.owner = factories.UserFactory()
        self.non_owner = factories.UserFactory()
        self.post = factories.PostFactory()
        self.comment = factories.CommentFactory(
            user=self.owner,
            post=self.post,
        )

        self.URL = f"/api/v1/posts/{self.post.pk}/comments/"

    def test_unauth(self):
        response = self.client.patch(f"{self.URL}999")
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_not_found(self):
        self.client.force_login(self.non_owner)
        response = self.client.patch(f"{self.URL}999")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_permission_denied(self):
        self.client.force_login(self.non_owner)
        response = self.client.patch(f"{self.URL}{self.comment.pk}")
        self.assertEqual(
            response.status_code,
            403,
        )

    def test_not_valid(self):
        self.client.force_login(self.owner)
        response = self.client.patch(f"{self.URL}{self.comment.pk}")
        self.assertEqual(
            response.status_code,
            400,
        )
        response = self.client.patch(
            f"{self.URL}{self.comment.pk}",
            {
                "payload": "",
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_success(self):

        self.client.force_login(self.owner)
        TEXT = "updated"
        response = self.client.patch(
            f"{self.URL}{self.comment.pk}",
            {
                "payload": TEXT,
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
            self.owner.pk,
        )
        self.assertEqual(
            data["post"]["pk"],
            self.post.pk,
        )
        self.assertEqual(
            data["payload"],
            TEXT,
        )


class TestDeleteComment(APITestCase):

    def setUp(self):
        self.owner = factories.UserFactory()
        self.non_owner = factories.UserFactory()
        self.post = factories.PostFactory()
        self.comment = factories.CommentFactory(
            user=self.owner,
            post=self.post,
        )

        self.URL = f"/api/v1/posts/{self.post.pk}/comments/"

    def test_unauth(self):
        response = self.client.delete(f"{self.URL}999")
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_not_found(self):
        self.client.force_login(self.non_owner)
        response = self.client.delete(f"{self.URL}999")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_permission_denied(self):
        self.client.force_login(self.non_owner)
        response = self.client.delete(f"{self.URL}{self.comment.pk}")
        self.assertEqual(
            response.status_code,
            403,
        )

    def test_success(self):
        self.client.force_login(self.owner)
        response = self.client.delete(f"{self.URL}{self.comment.pk}")
        self.assertEqual(
            response.status_code,
            204,
        )
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=self.comment.pk)
