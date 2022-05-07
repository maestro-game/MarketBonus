from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.text import gettext_lazy as _

from .models import Institute, University, Group, Block, Subject, Teacher, Lesson, Course, Director, Changes, days, \
    lesson_type, even_week



# University

class GetUniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = "__all__"


# Institute

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



# Group

class GetGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    course = serializers.IntegerField()

    class Meta:
        model = Group
        fields = "__all__"


# Block

class GetBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = "__all__"

class BlockSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()

    class Meta:
        model = Block
        fields = ["id", "name", "course_id"]


# Subject

class GetDopCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    block_id = serializers.IntegerField()

    class Meta:
        model = Subject
        fields = ["id", "name", "block_id"]

class PutSubjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=50, required=False)
    block_id = serializers.IntegerField(required=False)

    class Meta:
        model = Subject
        fields = ["id", "name", "block_id"]




# Teacher

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ["id", "name", "profile_link", "not_work_from"]

class PutTeacherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Teacher
        fields = ["id", "name", "profile_link", "not_work_from"]




# Lesson

class TimeTableSerializer(serializers.ModelSerializer):
    is_changed = serializers.BooleanField(required=True)

    class Meta:
        model = Lesson
        fields = ["id", "day_name", "start_time", "end_time", "type", "is_even_week", "teacher", "subject", "classroom", "group", "links", "is_changed"]

class DirectorTimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"

class PutLessonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    day_name = serializers.ChoiceField(choices=days, required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    type = serializers.ChoiceField(choices=lesson_type, required=False)
    is_even_week = serializers.ChoiceField(choices=even_week, required=False)
    teacher = serializers.IntegerField(required=False)
    subject = serializers.IntegerField(required=False)
    classroom = serializers.CharField(max_length=100, required=False)
    group = serializers.IntegerField(required=False)
    links = serializers.ListField(child=serializers.CharField(max_length=200), required=False)

    class Meta:
        model = Lesson
        fields = ["id", "day_name", "start_time", "end_time", "type", "is_even_week", "teacher", "subject", "classroom", "group", "links"]



# Course

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"



# Director

class DirectorSerializer(serializers.ModelSerializer):
    institute = GetFullInstituteSerializer()

    class Meta:
        model = Director
        fields = ["username", "first_name", "institute"]



# Changes

class ChangesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Changes
        fields = "__all__"



# Other

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

class DeleteSerializer(serializers.Serializer):
    id = serializers.ListField(child=serializers.IntegerField())

class GetTimeTableSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    dop_course_id = serializers.ListField(child=serializers.IntegerField(), required=False)

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

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')