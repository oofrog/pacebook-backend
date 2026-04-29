from rest_framework.test import APITestCase
from .factories import UserFactory


class TestPutUserMe(APITestCase):

    URL = "/api/v1/users/me"
    NAME = "test name"
    GENDER = "male"
    BIRTH_DAY = "2003-11-13"

    def setUp(self):
        self.user = UserFactory()
        self.valid_data = {
            "name": self.NAME,
            "gender": self.GENDER,
            "birth_day": self.BIRTH_DAY,
        }

    def test_unauth(self):
        response = self.client.put(self.URL)
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.put(self.URL)
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.put(
            self.URL,
            self.valid_data,
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        keys = ["name", "gender", "birth_day"]

        for key in keys:
            self.assertIn(
                key,
                data,
            )
