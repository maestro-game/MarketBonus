from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser


class University(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, null=True, default=None, blank=True)
    link = models.CharField(max_length=300, null=True, default=None, blank=True)

class Institute(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    first_sem_start = models.DateField()
    second_sem_start = models.DateField()
    short_name = models.CharField(max_length=100, null=True, default=None, blank=True)
    link = models.CharField(max_length=300, null=True, default=None, blank=True)

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    profile_link = models.CharField(max_length=100, null=True, blank=True, default=None)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    not_work_from = models.DateField(null=True, default=None, blank=True)

class Director(AbstractUser):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, null=True, blank=True)

class Course(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    course_number = models.IntegerField()

class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group_number = models.CharField(max_length=100)

class Block (models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

days = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
)

lesson_type = (
    (1, "ONLINE_PRACTICE"),
    (2, "OFFLINE_PRACTICE"),
    (3, "ONLINE_LECTURE"),
    (4, "OFFLINE_LECTURE"),
    (5, "CANCELED"),
)

even_week = (
        (1, "ODD_WEEK"),
        (2, "EVEN_WEEK"),
        (3, "ALL_WEEKS"),
)


class Lesson(models.Model):

    day_name = models.IntegerField(choices=days)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.IntegerField(choices=lesson_type)
    is_even_week = models.IntegerField(choices=even_week)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=100, null=True, default=None, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    links = ArrayField(models.CharField(max_length=200), null=True, blank=True)

change_type = (
    (1, "CANCEL"),
    (2, "DAY_CHANGE"),
    (3, "TIME_CHANGE"),
    (4, "TEACHER_CHANGE"),
    (5, "FORMAT_CHANGE"),
)

class Changes(models.Model):

    start_date = models.DateField()
    end_date = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    type = models.IntegerField(choices=change_type)
    day_change = models.IntegerField(choices=days, null=True, blank=True)
    time_change_start = models.TimeField(null=True, blank=True)
    time_change_end = models.TimeField(null=True, blank=True)
    teacher_change = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    format_change = models.IntegerField(choices=lesson_type, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)