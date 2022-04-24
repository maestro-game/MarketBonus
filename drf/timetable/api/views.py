from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Institute, University, Director, Group, Subject, Teacher
from .serializers import CreateTimeTableSerializer, GetUniversitySerializer, GetFullInstituteSerializer, \
    GetInstituteSerializer, GetGroupSerializer, GetBlockSerializer, GetCourseSerializer, TeacherSerializer, \
    GroupSerializer, MessageSerializer


class CreateTimeTable(APIView):
    """
    get:Список зарегистрированных институтов
    post:Зарегистрировать институт и директора
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(responses={200: GetFullInstituteSerializer(many=True)})
    def get(self, request):
        serialize = Institute.objects.all()
        result = GetFullInstituteSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=CreateTimeTableSerializer(), responses={200: GetFullInstituteSerializer(many=True)})
    def post(self, request):
        review = CreateTimeTableSerializer(data=request.data)
        if review.is_valid():
            try:
                pass
            except KeyError:
                return Response({"error": "incorrect data"})
        else:
            return Response({"error": "incorrect data"})
        data = request.data
        if Director.objects.filter(username=data.get('login')).exists():
            return Response("Account with this name already exist")
        if Institute.objects.filter(name__iexact=data.get('institute_name')).exists():
            return Response("Timetabe already exists")
        if University.objects.filter(name__iexact=data.get('university_name')).exists():
            univ = University.objects.get(name__iexact=data.get('university_name'))
            inst = Institute(university=univ, name=data.get('institute_name'), link=data.get('institute_site'),short_name=data.get('institute_short_name'))
            inst.save()
            director = Director(username=data.get('login'), first_name=data.get('name'),institute=inst)
            director.set_password(data.get('password'))
            director.save()
            return Response("Successfully")

        univ = University(name=data.get('university_name'), link=data.get('university_site'), short_name=data.get('university_short_name'))
        univ.save()
        inst = Institute(university=univ, name=data.get('institute_name'), link=data.get('institute_site'), short_name=data.get('institute_short_name'))
        inst.save()
        director = Director(username=data.get('login'), first_name=data.get('name'),
                            institute=inst)
        director.set_password(data.get('password'))
        director.save()
        return Response('Successfully')

class GetUniversity(APIView):
    """
    get:Список университетов
    """

    @swagger_auto_schema(responses={200: GetUniversitySerializer(many=True)})
    def get(self, request):
        serialize = University.objects.all()
        result = GetUniversitySerializer(serialize, many=True).data
        return Response(result)

class GetInstitute(APIView):
    """
    get:Список институтов по id университета
    """

    @swagger_auto_schema(responses={200: GetInstituteSerializer(many=True)})
    def get(self, request, id):
        serialize = Institute.objects.filter(university_id=id)
        result = GetInstituteSerializer(serialize, many=True).data
        return Response(result)

class GetGroup(APIView):
    """
    get:Список групп по id института
    """

    @swagger_auto_schema(responses={200: GetGroupSerializer(many=True)})
    def get(self, request, id):
        serialize = Group.objects.filter(institute_id=id)
        result = GetGroupSerializer(serialize, many=True).data
        return Response(result)

class GetBlock(APIView):
    """
    get:Список учебных блоков по id группы
    """

    @swagger_auto_schema(responses={200: GetBlockSerializer(many=True)})
    def get(self, request, id):
        if Group.objects.filter(id=id).exists():
            serialize = Group.objects.get(id=id).block.all()
            print(serialize)
            result = GetBlockSerializer(serialize, many=True).data
        else:
            result = []
        return Response(result)

class GetCourse(APIView):
    """
    get:Список доп курсов по id блока
    """

    @swagger_auto_schema(responses={200: GetCourseSerializer(many=True)})
    def get(self, request, id):
        serialize = Subject.objects.filter(block_id=id)
        result = GetCourseSerializer(serialize, many=True).data
        return Response(result)

class AddTeacher(APIView):
    """
    post:Добавление преподавателей в массиве
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=TeacherSerializer(many=True), responses={200: TeacherSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        review = TeacherSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        review.save(institute_id=institute_id)
        serialize = Teacher.objects.filter(institute_id=institute_id)
        result = TeacherSerializer(serialize, many=True).data
        return Response(result)

class AddGroup(APIView):
    """
    post:Добавление групп в массиве
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=GroupSerializer(many=True), responses={200: GroupSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        review = GroupSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        review.save(institute_id=institute_id)
        serialize = Group.objects.filter(institute_id=institute_id)
        result = GroupSerializer(serialize, many=True).data
        return Response(result)