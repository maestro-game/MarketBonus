from rest_framework import serializers

from .models import Institute, University, Group, Block, Subject, Teacher


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

class GetCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ["name", "profile_link", "not_work_from"]

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["group_number", "course"]

class MessageSerializer(serializers.Serializer):
    text = serializers.CharField()