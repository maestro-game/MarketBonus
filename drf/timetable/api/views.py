from datetime import datetime

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Institute, University, Director, Group, Subject, Teacher, Block, Course, Lesson, Changes
from .serializers import CreateTimeTableSerializer, GetUniversitySerializer, GetFullInstituteSerializer, \
    GetInstituteSerializer, GetGroupSerializer, GetBlockSerializer, TeacherSerializer, \
    GroupSerializer, MessageSerializer, BlockSerializer, SubjectSerializer, GetDopCourseSerializer, \
    GetTimeTableSerializer, TimeTableSerializer, CourseSerializer, DirectorSerializer, ChangesSerializer, \
    DirectorTimeTableSerializer, DBSerializer, RefreshTokenSerializer, DeleteSerializer, PutTeacherSerializer, \
    PutSubjectSerializer, PutLessonSerializer


class CreateTimeTable(APIView):
    """
    get:Список зарегистрированных институтов\n
    Список зарегистрированных институтов
    post:Зарегистрировать институт и директора\n
    Зарегистрировать институт и директора
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
    get:Список университетов\n
    Список университетов
    """

    @swagger_auto_schema(responses={200: GetUniversitySerializer(many=True)})
    def get(self, request):
        serialize = University.objects.all()
        result = GetUniversitySerializer(serialize, many=True).data
        return Response(result)

class GetInstitute(APIView):
    """
    get:Список институтов по id университета\n
    Список институтов по id университета
    """

    @swagger_auto_schema(responses={200: GetInstituteSerializer(many=True)})
    def get(self, request, id):
        serialize = Institute.objects.filter(university_id=id)
        result = GetInstituteSerializer(serialize, many=True).data
        return Response(result)

class GetGroup(APIView):
    """
    get:Список групп по id института\n
    Список групп по id института
    """

    @swagger_auto_schema(responses={200: GetGroupSerializer(many=True)})
    def get(self, request, id):
        course = Course.objects.filter(institute_id=id)
        serialize = Group.objects.filter(course__in=course)
        result = GetGroupSerializer(serialize, many=True).data
        return Response(result)

class GetBlock(APIView):
    """
    get:Список учебных блоков по id группы\n
    Список учебных блоков по id группы
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
    get:Список доп курсов по id блока\n
    Список доп курсов по id блока
    """

    @swagger_auto_schema(responses={200: GetDopCourseSerializer(many=True)})
    def get(self, request, id):
        serialize = Subject.objects.filter(block_id=id)
        result = GetDopCourseSerializer(serialize, many=True).data
        return Response(result)

class AddTeacher(APIView):
    """
    get:Список всех преподавателей интитута\n
    Список всех преподавателей интитута
    post:Добавление преподавателей в массиве\n
    Добавление преподавателей в массиве
    put:Обновить данные преподавателей в массиве\n
    Обновить данные преподавателей в массиве
    delete:Удалить преподавателей в массиве\n
    Удалить преподавателей в массиве
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

    @swagger_auto_schema(request_body=PutTeacherSerializer(many=True), responses={200: TeacherSerializer(many=True), 400: MessageSerializer()})
    def put(self, request):
        institute_id = request.user.institute_id
        review = PutTeacherSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for teacher_data in review.data:
            if not Teacher.objects.filter(id=teacher_data.get('id'), institute_id=institute_id).exists():
                return Response({"text": "Teacher id does not exist"}, status=400)
        for teacher_data in request.data:
            keys = teacher_data.keys()
            teacher = Teacher.objects.get(id=teacher_data.get('id'))
            if 'name' in keys:
                teacher.name = teacher_data.get('name')
            if 'profile_link' in keys:
                teacher.profile_link = teacher_data.get('profile_link')
            if 'not_work_from' in keys:
                teacher.not_work_from = teacher_data.get('not_work_from')
            teacher.save()
        serialize = Teacher.objects.filter(institute_id=institute_id)
        result = TeacherSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=DeleteSerializer(), responses={200: TeacherSerializer(many=True), 400: MessageSerializer()})
    def delete(self, request):
        institute_id = request.user.institute_id
        review = DeleteSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for id in review.data.get('id'):
            if not Teacher.objects.filter(id=id, institute_id=institute_id).exists():
                return Response({"text": "Teacher id does not exist"}, status=400)
        for id in review.data.get('id'):
            Teacher.objects.filter(id=id).delete()
        serialize = Teacher.objects.filter(institute_id=institute_id)
        result = TeacherSerializer(serialize, many=True).data
        return Response(result)


class AddGroup(APIView):
    """
    get:Список всех групп интитута\n
    Список всех групп интитута
    post:Добавление групп в массиве\n
    Добавление групп в массиве
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
    get:Список всех блоков интитута\n
    Список всех блоков интитута
    post:Добавление доп курсов в массиве\n
    Добавление доп курсов в массиве
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
    get:Список всех предметов интитута\n
    Список всех предметов интитута
    post:Добавление предметов в массиве\n
    Добавление предметов в массиве
    put:Обновить данные предметов в массиве\n
    Обновить данные предметов в массиве
    delete:Удалить предметы в массиве\n
    Удалить предметы в массиве
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

    @swagger_auto_schema(request_body=PutSubjectSerializer(many=True), responses={200: SubjectSerializer(many=True), 400: MessageSerializer()})
    def put(self, request):
        institute_id = request.user.institute_id
        review = PutSubjectSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        courses_id = Course.objects.filter(institute_id=institute_id)
        blocks = Block.objects.filter(course_id__in=courses_id)
        for subject_data in review.data:
            if not Subject.objects.filter(id=subject_data.get('id'), block__in=blocks).exists():
                return Response({"text": "Subject id does not exist"}, status=400)
        for subject_data in request.data:
            keys = subject_data.keys()
            subject = Subject.objects.get(id=subject_data.get('id'))
            if 'name' in keys:
                subject.name = subject_data.get('name')
            block = Block.objects.filter(id=subject_data.get('block_id'))
            if not block.exists():
                return Response({"text": "Block_id does not exist"}, status=400)
            if 'block_id' in keys and block[0] in blocks:
                subject.block_id = subject_data.get('block_id')
            subject.save()
        serialize = Subject.objects.filter(block__in=blocks)
        result = SubjectSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=DeleteSerializer(), responses={200: SubjectSerializer(many=True), 400: MessageSerializer()})
    def delete(self, request):
        institute_id = request.user.institute_id
        courses_id = Course.objects.filter(institute_id=institute_id)
        blocks = Block.objects.filter(course_id__in=courses_id)
        review = DeleteSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for id in review.data.get('id'):
            if not Subject.objects.filter(id=id, block__in=blocks).exists():
                return Response({"text": "Subject id does not exist"}, status=400)
        for id in review.data.get('id'):
            Subject.objects.filter(id=id).delete()
        serialize = Subject.objects.filter(block__in=blocks)
        result = SubjectSerializer(serialize, many=True).data
        return Response(result)


class GetLesson(APIView):
    """
    get:Список всех занятий(экземпляров) интитута без изменений\n
    Список всех занятий(экземпляров) интитута
    post:Добавление занятий(экземпляров) в массиве\n
    Добавление предметов в массиве
    put:Обновить данные занятий(экземпляров) в массиве\n
    Обновить данные занятий(экземпляров) в массиве
    delete:Удалить данные занятий(экземпляров) в массиве\n
    Удалить данные занятий(экземпляров) в массиве
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DirectorTimeTableSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        subject = Subject.objects.filter(block__in=block)
        serialize = Lesson.objects.filter(subject__in=subject)
        result = DirectorTimeTableSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=DirectorTimeTableSerializer(many=True), responses={200: DirectorTimeTableSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        subject = Subject.objects.filter(block__in=block)
        review = DirectorTimeTableSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        review.save()
        serialize = Lesson.objects.filter(subject__in=subject)
        result = DirectorTimeTableSerializer(serialize, many=True).data
        return Response(result)

    # @swagger_auto_schema(request_body=PutLessonSerializer(many=True), responses={200: DirectorTimeTableSerializer(many=True), 400: MessageSerializer()})
    # def put(self, request):
    #     institute_id = request.user.institute_id
    #     review = PutLessonSerializer(data=request.data, many=True)
    #     if not review.is_valid():
    #         return Response({"text": "incorrect data"}, status=400)
    #     courses_id = Course.objects.filter(institute_id=institute_id)
    #     blocks = Block.objects.filter(course_id__in=courses_id)
    #     for subject_data in review.data:
    #         if not Subject.objects.filter(id=subject_data.get('id'), block__in=blocks).exists():
    #             return Response({"text": "Subject id does not exist"}, status=400)
    #     for subject_data in request.data:
    #         keys = subject_data.keys()
    #         subject = Subject.objects.get(id=subject_data.get('id'))
    #         if 'name' in keys:
    #             subject.name = subject_data.get('name')
    #         block = Block.objects.filter(id=subject_data.get('block_id'))
    #         if not block.exists():
    #             return Response({"text": "Block_id does not exist"}, status=400)
    #         if 'block_id' in keys and block[0] in blocks:
    #             subject.block_id = subject_data.get('block_id')
    #         subject.save()
    #     serialize = Subject.objects.filter(block__in=blocks)
    #     result = SubjectSerializer(serialize, many=True).data
    #     return Response(result)

    @swagger_auto_schema(request_body=DeleteSerializer(), responses={200: DirectorTimeTableSerializer(many=True), 400: MessageSerializer()})
    def delete(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        subject = Subject.objects.filter(block__in=block)
        review = DeleteSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for id in review.data.get('id'):
            if not Lesson.objects.filter(id=id, subject__in=subject).exists():
                return Response({"text": "Lesson id does not exist"}, status=400)
        for id in review.data.get('id'):
            Lesson.objects.filter(id=id).delete()
        serialize = Lesson.objects.filter(subject__in=subject)
        result = DirectorTimeTableSerializer(serialize, many=True).data
        return Response(result)



















class GetTimetable(APIView):
    """
    post:Получить рассписание

    is_even_week : {\n1: \"ODD_WEEK\",\n 2: \"EVEN_WEEK\",\n 3: \"ALL_WEEKS\"\n}
    type : {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n
    """

    @swagger_auto_schema(request_body=GetTimeTableSerializer(), responses={200: TimeTableSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        review = request.data
        if not Group.objects.filter(id = review.get("group_id")).exists():
            return Response({"text": "group does not exists"}, status=400)
        course_id = Group.objects.get(id = review.get("group_id")).course_id
        block_id = Block.objects.get(course_id=course_id, name=None).id
        group_subjects = Subject.objects.filter(block_id=block_id)
        if not review.get("dop_course_id"):
            serialize = Lesson.objects.filter(group_id=review.get("group_id"), subject__in=group_subjects)
        else:
            for i in review.get("dop_course_id"):
                if not Subject.objects.filter(id=i).exists():
                    return Response({"text": "extra course does not exists"}, status=400)

            serialize = Lesson.objects.filter(Q(group_id=review.get("group_id"), subject_id__in=review.get("dop_course_id")) |
                                              Q(group_id=review.get("group_id"), subject__in=group_subjects))

        for lesson in serialize:
            lesson.is_changed = False
            if Changes.objects.filter(lesson=lesson).exists():
                for change in Changes.objects.filter(lesson=lesson):
                    if change.start_date <= datetime.now().date() and datetime.now().date() <= change.end_date:
                        if change.type == 1:
                            lesson.is_changed = True
                            lesson.type = 5

                        elif change.type == 2:
                            lesson.is_changed = True
                            lesson.day_name = change.day_change

                        elif change.type == 3:
                            lesson.is_changed = True
                            lesson.start_time = change.time_change_start
                            lesson.end_time = change.time_change_end

                        elif change.type == 4:
                            lesson.is_changed = True
                            lesson.teacher = change.teacher_change

                        elif change.type == 5:
                            lesson.is_changed = True
                            lesson.type = change.format_change

        result = TimeTableSerializer(serialize, many=True).data
        return Response(result)

class GetCourse(APIView):
    """
    get:Получить список курсов интитута\n
    Получить список курсов интитута
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: CourseSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        serialize = Course.objects.filter(institute_id=institute_id)
        result = CourseSerializer(serialize, many=True).data
        return Response(result)


class GetAccount(APIView):
    """
    get: Получить данные деканата\n
    Получить данные деканата
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DirectorSerializer(), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        serialize = Director.objects.filter(institute_id=institute_id)[0]
        result = DirectorSerializer(serialize).data
        return Response(result)


class GetTable(APIView):
    """
    get:Получить все таблицы

    changes
    type : {\n1: \"CANCEL\",\n 2: \"DAY_CHANGE\",\n 3: \"TIME_CHANGE\",\n 4: \"TEACHER_CHANGE\",\n 5: \"FORMAT_CHANGE\"\n}
    -------------------------
    lessons
    is_even_week : {\n1: \"ODD_WEEK\",\n 2: \"EVEN_WEEK\",\n 3: \"ALL_WEEKS\"\n}
    type : {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DBSerializer(), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        courses = Course.objects.filter(institute_id=institute_id)
        groups = Group.objects.filter(course_id__in=courses)
        blocks = Block.objects.filter(course_id__in=courses)
        subjects = Subject.objects.filter(block_id__in=blocks)
        teachers = Teacher.objects.filter(institute_id=institute_id)
        lessons = Lesson.objects.filter(subject_id__in=subjects)
        changes = Changes.objects.filter(lesson_id__in=lessons)

        result = {"courses": CourseSerializer(courses, many=True).data,
                  "groups": GetGroupSerializer(groups, many=True).data,
                  "blocks": GetBlockSerializer(blocks, many=True).data,
                  "subjects": GetDopCourseSerializer(subjects, many=True).data,
                  "teachers": TeacherSerializer(teachers, many=True).data,
                  "lessons": DirectorTimeTableSerializer(lessons, many=True).data,
                  "changes": ChangesSerializer(changes, many=True).data
                  }
        return Response(result)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)




