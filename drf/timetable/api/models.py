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
        ("1B", "1 курс балавриат"),
        ("2B", "2 курс балавриат"),
        ("3B", "3 курс балавриат"),
        ("4B", "4 курс балавриат"),
        ("1M", "1 курс магистратура"),
        ("2M", "2 курс магистратура"),
    )

    course = models.CharField(choices=courses, max_length=20)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    group_number = models.CharField(max_length=100)

class Block (models.Model):
    group = models.ManyToManyField(Group, blank=True, related_name='block')
    name = models.CharField(max_length=100, default="")

class Subject(models.Model):
    name = models.CharField(max_length=100)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

days = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
    )

class Lesson(models.Model):

    lesson_type = (
        ("Online", "Online"),
        ("Offline", "Offline"),
    )

    day_name = models.CharField(choices=days, max_length=15)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(choices=lesson_type, max_length=15)
    is_even_week = models.BooleanField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    links = ArrayField(models.CharField(max_length=200), blank=True)

class Changes(models.Model):
    change_type = (
        ("Cancel", "Cancel"),
        ("Day_change", "Day_change"),
        ("Time_change", "Time_change"),
        ("Teacher_change", "Teacher_change"),
        ("Format_change", "Format_change"),
    )

    start_date = models.DateField()
    end_date = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    type = models.CharField(choices=change_type, max_length=20)
    day_change = models.CharField(choices=days, max_length=15)
    time_change = models.TimeField()
    comment = models.CharField(max_length=200)
