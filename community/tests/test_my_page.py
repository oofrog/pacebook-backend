from rest_framework.test import APITestCase
from .factories import UserFactory, PostFactory


class TestGetMyPage(APITestCase):

    URL = "/api/v1/posts/my-page"
    NUM = 3

    def setUp(self):
        self.owner = UserFactory()
        self.empty_owner = UserFactory()
        self.posts = PostFactory.create_batch(self.NUM, owner=self.owner)

    def test_unauth(self):
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_success(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.URL)
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
        self.assertEqual(
            data[0]["owner"],
            self.owner.pk,
        )
        
    def test_empty(self):
        self.client.force_login(self.empty_owner)
        response = self.client.get(self.URL)
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
            0,
        )
