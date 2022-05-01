from django.db import models
from rest_framework import serializers

from .models import Institute, University, Group, Block, Subject, Teacher, Lesson, Course, Director, Changes, days


class CreateTimeTableSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    institute_name = serializers.CharField()
    institute_short_name = serializers.CharField()
    institute_site = serializers.CharField()
    university_name = serializers.CharField()
    university_short_name = serializers.CharField()
    university_site = serializers.CharField()

class GetUniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = "__all__"

class GetInstituteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institute
        fields = "__all__"

class GetFullInstituteSerializer(serializers.ModelSerializer):
    university = GetUniversitySerializer()

    class Meta:
        model = Institute
        fields = "__all__"

    depth = 1

class GetGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"

class GetBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = "__all__"

class GetDopCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ["id", "name", "profile_link", "not_work_from"]

class GroupSerializer(serializers.ModelSerializer):
    course = serializers.IntegerField()

    class Meta:
        model = Group
        fields = "__all__"

class BlockSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()

    class Meta:
        model = Block
        fields = ["id", "name", "course_id"]

class SubjectSerializer(serializers.ModelSerializer):
    block_id = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = ["id", "name", "block_id"]

class GetTimeTableSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    dop_course_id = serializers.ListField(child=serializers.IntegerField(), required=False)

class TimeTableSerializer(serializers.ModelSerializer):
    is_changed = serializers.BooleanField(required=True)

    class Meta:
        model = Lesson
        fields = ["id", "day_name", "start_time", "end_time", "type", "is_even_week", "teacher", "subject", "classroom", "group", "links", "is_changed"]

class DirectorTimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"

class DirectorSerializer(serializers.ModelSerializer):
    institute = GetFullInstituteSerializer()

    class Meta:
        model = Director
        fields = ["username", "first_name", "institute"]



class ChangesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Changes
        fields = "__all__"


class DBSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    groups = GetGroupSerializer(many=True)
    blocks = GetBlockSerializer(many=True)
    subjects = GetDopCourseSerializer(many=True)
    teachers = TeacherSerializer(many=True)
    lessons = DirectorTimeTableSerializer(many=True)
    changes = ChangesSerializer(many=True)

class MessageSerializer(serializers.Serializer):
    text = serializers.CharField()

