from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.text import gettext_lazy as _

from .models import Institute, University, Group, Block, Subject, Teacher, Lesson, Course, Director, Changes, days, \
    lesson_type, even_week, change_type


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

class PatchGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    course = serializers.IntegerField(required=False)
    group_number = serializers.CharField(required=False)

    class Meta:
        model = Group
        fields = ["id", "course", "group_number"]


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

class PatchSubjectSerializer(serializers.ModelSerializer):
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

class PatchTeacherSerializer(serializers.ModelSerializer):
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

class PatchLessonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    day_name = serializers.ChoiceField(choices=days, required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    type = serializers.ChoiceField(choices=lesson_type, required=False)
    is_even_week = serializers.ChoiceField(choices=even_week, required=False)
    teacher = serializers.IntegerField(required=False)
    subject = serializers.IntegerField(required=False)
    classroom = serializers.CharField(max_length=100, allow_null=True, required=False)
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

class PostCourseSerializer(serializers.ModelSerializer):
    course_number = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Course
        fields = ['course_number']

class PatchCourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    course_number = serializers.IntegerField(required=True)

    class Meta:
        model = Course
        fields = ["id", "course_number"]


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

class PatchChangeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    lesson = serializers.IntegerField(required=True)
    type = serializers.ChoiceField(choices=change_type, required=True)
    day_change = serializers.ChoiceField(choices=days, required=False, allow_null=True)
    time_change_start = serializers.TimeField(required=False, allow_null=True)
    time_change_end = serializers.TimeField(required=False, allow_null=True)
    teacher_change = serializers.IntegerField(required=False, allow_null=True)
    format_change = serializers.ChoiceField(choices=lesson_type, required=False, allow_null=True)
    comment = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Changes
        fields = ["id", "start_date", "end_date", "lesson", "type", "day_change", "time_change_start", "time_change_end", "teacher_change", "format_change", "comment"]


# Other

class CreateTimeTableSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    first_sem_start = serializers.DateField()
    second_sem_start = serializers.DateField()
    institute_name = serializers.CharField()
    institute_short_name = serializers.CharField(required=False)
    institute_site = serializers.CharField(required=False)
    university_name = serializers.CharField()
    university_short_name = serializers.CharField(required=False)
    university_site = serializers.CharField(required=False)

class DeleteSerializer(serializers.Serializer):
    id = serializers.ListField(child=serializers.IntegerField())

class GetTimeTableSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    dop_course_id = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)
    current_week = serializers.BooleanField(required=False)

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

class EvenWeekSerializer(serializers.Serializer):
    even_week = serializers.BooleanField()

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