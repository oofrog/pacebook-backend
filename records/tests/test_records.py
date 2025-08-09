from rest_framework.test import APITestCase
from .factories import UserFactory


class TestPostRecord(APITestCase):

    URL = "/api/v1/records/"
    DURATION = 6521
    DISTANCE = 3251
    PACE = 532
    KCAL = 310
    ROUTE = "abcd"

    def setUp(self):
        self.user = UserFactory()
        self.valid_data = {
            "duration_sec": self.DURATION,
            "distance_m": self.DISTANCE,
            "pace": self.PACE,
            "kcal": self.KCAL,
            "route": self.ROUTE,
        }

    def test_unauth(self):
        response = self.client.post(self.URL, self.valid_data)
        print(response.json())
        self.assertEqual(
            response.status_code,
            401,
            "카카오로그인 인증 오류는 401",
        )

    def test_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.post(self.URL)
        self.assertEqual(
            response.status_code,
            400,
        )

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.URL,
            self.valid_data,
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        keys = ["owner", "duration_sec", "distance_m", "pace", "kcal", "route"]

        for key in keys:
            self.assertIn(
                key,
                data,
            )
        self.assertEqual(
            data["owner"]["pk"],
            self.user.pk,
        )
        self.assertEqual(
            data["duration_sec"],
            self.DURATION,
        )
        self.assertEqual(
            data["distance_m"],
            self.DISTANCE,
        )
        self.assertEqual(
            data["pace"],
            self.PACE,
        )
        self.assertEqual(
            data["kcal"],
            self.KCAL,
        )
        self.assertEqual(
            data["route"],
            self.ROUTE,
        )
