from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Institute, University, Director, Group, Subject, Teacher, Block, Course, Lesson
from .serializers import CreateTimeTableSerializer, GetUniversitySerializer, GetFullInstituteSerializer, \
    GetInstituteSerializer, GetGroupSerializer, GetBlockSerializer, TeacherSerializer, \
    GroupSerializer, MessageSerializer, BlockSerializer, SubjectSerializer, GetDopCourseSerializer, \
    GetTimeTableSerializer, TimeTableSerializer, CourseSerializer


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
        course = Course.objects.filter(institute_id=id)
        serialize = Group.objects.filter(course__in=course)
        result = GetGroupSerializer(serialize, many=True).data
        return Response(result)

class GetBlock(APIView):
    """
    get:Список учебных блоков по id группы
    """

    @swagger_auto_schema(responses={200: GetBlockSerializer(many=True)})
    def get(self, request, id):
        if Group.objects.filter(id=id).exists():
            course = Group.objects.get(id=id).course
            serialize = Block.objects.filter(course=course).exclude(name__isnull=True)
            result = GetBlockSerializer(serialize, many=True).data
        else:
            result = []
        return Response(result)

class GetDopCourse(APIView):
    """
    get:Список доп курсов по id блока
    """

    @swagger_auto_schema(responses={200: GetDopCourseSerializer(many=True)})
    def get(self, request, id):
        serialize = Subject.objects.filter(block_id=id)
        result = GetDopCourseSerializer(serialize, many=True).data
        return Response(result)

class AddTeacher(APIView):
    """
    get:Список всех преподавателей интитута
    post:Добавление преподавателей в массиве
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: TeacherSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        serialize = Teacher.objects.filter(institute_id=institute_id)
        result = TeacherSerializer(serialize, many=True).data
        return Response(result)

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
    get:Список всех групп интитута
    post:Добавление групп в массиве
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: GroupSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        serialize = Group.objects.filter(course__in=course)
        result = GetGroupSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=GroupSerializer(many=True), responses={200: GroupSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        review = GroupSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        try:
            for i in review.initial_data:
                course = Course.objects.update_or_create(course_number=i.get("course"), institute_id=institute_id)
                Block.objects.update_or_create(name=None, course=course[0])
                Group.objects.update_or_create(group_number=i.get("group_number"), course=course[0])
        except:
            return Response({"text": "incorrect data"}, status=400)
        course = Course.objects.filter(institute_id=institute_id)
        serialize = Group.objects.filter(course__in=course)
        result = GetGroupSerializer(serialize, many=True).data
        return Response(result)

class AddBlock(APIView):
    """
    get:Список всех блоков интитута
    post:Добавление доп курсов в массиве
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: BlockSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        serialize = Block.objects.filter(course__in=Course.objects.filter(institute_id=institute_id)).distinct('id')
        result = BlockSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=BlockSerializer(many=True), responses={200: BlockSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        review = BlockSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for i in review.initial_data:
            if not Course.objects.filter(institute_id=institute_id, id=i.get("course_id")).exists():
                return Response({"text": "incorrect data"}, status=400)
        for i in review.initial_data:
            Block.objects.update_or_create(course=Course.objects.get(institute_id=institute_id, id=i.get("course_id")), name=i.get("name"))
        serialize = Block.objects.filter(course__in=Course.objects.filter(institute_id=institute_id)).distinct('id').exclude(name__isnull=True)
        result = BlockSerializer(serialize, many=True).data
        return Response(result)

class AddSubject(APIView):
    """
    get:Список всех предметов интитута
    post:Добавление доп курсов в массиве
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: SubjectSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        serialize = Subject.objects.filter(block__in=block)
        result = SubjectSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=SubjectSerializer(many=True), responses={200: SubjectSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        review = SubjectSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for i in review.initial_data:
            if not block.filter(id=i.get("block_id")).exists():
                return Response({"text": "incorrect data"}, status=400)
        for i in review.initial_data:
            Subject.objects.update_or_create(block_id=i.get("block_id"), name=i.get("name"))

        serialize = Subject.objects.filter(block__in=block)
        result = SubjectSerializer(serialize, many=True).data
        return Response(result)


class GetTimetable(APIView):
    """
    post:Получить рассписание
    """

    @swagger_auto_schema(request_body=GetTimeTableSerializer(), responses={200: TimeTableSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        review = request.data
        if not Group.objects.filter(id = review.get("group_id")).exists() or not Subject.objects.filter(id=review.get("dop_course_id")).exists():
            return Response({"text": "incorrect data"}, status=400)
        serialize = Lesson.objects.filter(Q(group_id=review.get("group_id")) | Q(subject_id=review.get("dop_course_id")))
        result = TimeTableSerializer(serialize, many=True).data
        return Response(result)

class GetCourse(APIView):
    """
    post:Получить список курсов интитута
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: CourseSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        serialize = Course.objects.filter(institute_id=institute_id)
        result = CourseSerializer(serialize, many=True).data
        return Response(result)
