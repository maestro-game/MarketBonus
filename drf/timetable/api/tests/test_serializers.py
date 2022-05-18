from rest_framework.test import APITestCase

from ..models import University, Institute, Teacher
from ..serializers import GetUniversitySerializer, GetInstituteSerializer, AllTeacherSerializer


class SerializerTestCase(APITestCase):
    def setUp(self):
        university = University.objects.update_or_create(id=1, name="КАЗАНСКИЙ ПРИВОЛЖСКИЙ ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ", short_name="КФУ")[0]
        institute = Institute.objects.update_or_create(id=1 ,name="itis", university=university, short_name="itis", first_sem_start="2021-09-01",
                                 second_sem_start="2022-02-09")[0]
        Teacher.objects.update_or_create(id=1, name="Васильев Василий Висильевич", profile_link=None, institute=institute, not_work_from=None)

    def test_university(self):
        university = University.objects.get(id=1)
        serialized_data = GetUniversitySerializer(university).data
        expected_data = {'id': 1, 'name': "КАЗАНСКИЙ ПРИВОЛЖСКИЙ ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ", "short_name": "КФУ", 'link': None}
        self.assertEqual(serialized_data, expected_data)

    def test_institute(self):
        institute = Institute.objects.get(id=1)
        serialized_data = GetInstituteSerializer(institute).data
        expected_data = {'id': 1, 'name': 'itis', 'first_sem_start': '2021-09-01', 'short_name': 'itis', 'second_sem_start': '2022-02-09', 'link': None, 'university': 1}
        self.assertEqual(serialized_data, expected_data)

    def test_teacher(self):
        teacher = Teacher.objects.get(id=1)
        serialized_data = AllTeacherSerializer(teacher).data
        expected_data = {'id': 1, 'name': 'Васильев Василий Висильевич', 'profile_link': None, 'institute': 1, 'not_work_from': None}
        self.assertEqual(serialized_data, expected_data)
