from rest_framework.test import APITestCase
from .factories import UserFactory, PostFactory, LikeFactory
from community.models import Like


class TestGetLikes(APITestCase):

    URL = "/api/v1/posts/"
    NUM = 3

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()
        LikeFactory.create_batch(self.NUM, post=self.post)

    def test_not_found(self):
        response = self.client.get(f"{self.URL}999/likes")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_success(self):
        response = self.client.get(f"{self.URL}{self.post.pk}/likes")
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
        for like in data:
            self.assertEqual(
                like["post"]["pk"],
                self.post.pk,
            )


class TestPostLike(APITestCase):
    URL = "/api/v1/posts/"

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()

    def test_unauth(self):
        response = self.client.post(f"{self.URL}{self.post.pk}/likes")
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_not_found(self):
        self.client.force_login(self.user)
        response = self.client.post(f"{self.URL}999/likes")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.post(f"{self.URL}{self.post.pk}/likes")
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        keys = ["user", "post"]
        for key in keys:
            self.assertIn(key, data)
        self.assertEqual(
            data["user"]["pk"],
            self.user.pk,
        )
        self.assertEqual(
            data["post"]["pk"],
            self.post.pk,
        )


class TestDeleteLike(APITestCase):

    URL = "/api/v1/posts/"

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()
        self.like = LikeFactory(
            user=self.user,
            post=self.post,
        )

    def test_unauth(self):
        response = self.client.delete(f"{self.URL}{self.post.pk}/likes")
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_post_not_found(self):
        self.client.force_login(self.user)
        response = self.client.delete(f"{self.URL}999/likes")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_like_not_found(self):
        new_user = UserFactory()
        self.client.force_login(new_user)
        response = self.client.delete(f"{self.URL}{self.post.pk}/likes")
        self.assertEqual(
            response.status_code,
            404,
        )

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.delete(f"{self.URL}{self.post.pk}/likes")
        self.assertEqual(
            response.status_code,
            204,
        )
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(
                user=self.user,
                post=self.post,
            )
