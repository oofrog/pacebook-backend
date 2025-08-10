from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from .factories import UserFactory, RecordFactory
from records.models import Record


class TestGetMyRecords(APITestCase):

    URL = "/api/v1/records/me"
    NUM = 2
    TIME_GAP = 1
    TARGET_DATE = timezone.localtime(timezone.now()) - timedelta(days=TIME_GAP)
    TARGET_DATE_STR = str(timezone.localdate() - timedelta(days=TIME_GAP))

    def setUp(self):
        self.owner = UserFactory()
        self.today_records = RecordFactory.create_batch(
            self.NUM,
            owner=self.owner,
        )

    def test_unauth(self):
        response = self.client.get(self.URL)
        self.assertEqual(
            response.status_code,
            401,
        )

    def test_today_record(self):
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
        for record in data:
            self.assertEqual(
                record["owner"]["pk"],
                self.owner.pk,
            )

    def test_invalid_date(self):
        self.client.force_login(self.owner)
        response = self.client.get(f"{self.URL}?date=this-is-not-a-date")
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        today = str(timezone.localdate())

        for record in data:
            self.assertTrue(
                record["created_at"].startswith(today),
            )

    def test_another_date(self):
        self.client.force_login(self.owner)
        self.another_record = RecordFactory.create(owner=self.owner)
        Record.objects.filter(pk=self.another_record.pk).update(
            created_at=self.TARGET_DATE,
        )
        response = self.client.get(f"{self.URL}?date={self.TARGET_DATE_STR}")
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        for record in data:
            self.assertTrue(
                record["created_at"].startswith(self.TARGET_DATE_STR),
            )
