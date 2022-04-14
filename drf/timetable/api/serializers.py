from rest_framework import serializers


class CreateTimeTableSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    institute_name = serializers.CharField()
    institute_site = serializers.CharField()
    university_name = serializers.CharField()
    university_site = serializers.CharField()
