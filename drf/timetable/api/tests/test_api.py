from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import University, Institute, Teacher


class ApiTestCase(APITestCase):
    def setUp(self):
        university = University.objects.update_or_create(id=1, name="КАЗАНСКИЙ ПРИВОЛЖСКИЙ ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ", short_name="КФУ")[0]
        institute = Institute.objects.update_or_create(id=1 ,name="itis", university=university, short_name="itis", first_sem_start="2021-09-01",
                                 second_sem_start="2022-02-09")[0]
        Teacher.objects.update_or_create(id=1, name="Васильев Василий Висильевич", profile_link=None, institute=institute, not_work_from=None)

    def test_university(self):
        url = reverse("university")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_teacher(self):
        url = reverse("teacher")
        response = self.client.patch(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)