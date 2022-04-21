from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser


class University(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, null=True, default=None)
    link = models.CharField(max_length=300, null=True, default=None)

class Institute(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, null=True, default=None)
    link = models.CharField(max_length=300, null=True, default=None)

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    profile_link = models.CharField(max_length=100, null=True, default=None)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, null=True)
    not_work_from = models.DateField(null=True, default=None)

class Director(AbstractUser):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, null=True)

class Group(models.Model):
    courses = (
        (1, "1 курс балавриат"),
        (2, "2 курс балавриат"),
        (3, "3 курс балавриат"),
        (4, "4 курс балавриат"),
        (5, "1 курс магистратура"),
        (6, "2 курс магистратура"),
    )

    course = models.IntegerField(choices=courses, default=None)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    group_number = models.CharField(max_length=100)

class Block (models.Model):
    group = models.ManyToManyField(Group, blank=True, related_name='block')
    name = models.CharField(max_length=100, default="")

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

class Lesson(models.Model):

    lesson_type = (
        (1, "Online"),
        (2, "Offline"),
    )

    day_name = models.IntegerField(choices=days)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.IntegerField(choices=lesson_type)
    is_even_week = models.BooleanField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    links = ArrayField(models.CharField(max_length=200), blank=True)

class Changes(models.Model):
    change_type = (
        (1, "Cancel"),
        (2, "Day_change "),
        (3, "Time_change"),
        (4, "Teacher_change"),
        (5, "Format_change"),
    )

    start_date = models.DateField()
    end_date = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    type = models.IntegerField(choices=change_type)
    day_change = models.IntegerField(choices=days)
    time_change = models.TimeField()
    comment = models.CharField(max_length=200)
