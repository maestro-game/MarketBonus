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
    DirectorTimeTableSerializer, DBSerializer, RefreshTokenSerializer, DeleteSerializer, PatchTeacherSerializer, \
    PatchSubjectSerializer, PatchLessonSerializer, PatchGroupSerializer, PatchChangeSerializer, EvenWeekSerializer, \
    PostCourseSerializer, PatchCourseSerializer


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
        if not review.is_valid():
            return Response({"error": "incorrect data"}, status=400)
        data = request.data
        if Director.objects.filter(username=data.get('login')).exists():
            return Response("Account with this name already exist")
        if Institute.objects.filter(name__iexact=data.get('institute_name')).exists():
            return Response("Timetabe already exists")
        if University.objects.filter(name__iexact=data.get('university_name')).exists():
            univ = University.objects.get(name__iexact=data.get('university_name'))
            inst = Institute(university=univ, name=data.get('institute_name'), link=data.get('institute_site'), short_name=data.get('institute_short_name'))
            inst.save()
            director = Director(username=data.get('login'), first_name=data.get('name'),institute=inst)
            director.set_password(data.get('password'))
            director.save()
            return Response("Successfully")

        univ = University(name=data.get('university_name'), link=data.get('university_site'), short_name=data.get('university_short_name'))
        univ.save()
        inst = Institute(university=univ, name=data.get('institute_name'), link=data.get('institute_site'), short_name=data.get('institute_short_name'), first_sem_start=data.get('first_sem_start'), second_sem_start=data.get('second_sem_start'))
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
    patch:Обновить данные преподавателей в массиве\n
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

    @swagger_auto_schema(request_body=PatchTeacherSerializer(many=True), responses={204: "", 400: MessageSerializer()})
    def patch(self, request):
        institute_id = request.user.institute_id
        review = PatchTeacherSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for teacher_data in review.data:
            if not Teacher.objects.filter(id=teacher_data.get('id'), institute_id=institute_id).exists():
                return Response({"text": "Teacher id does not exist"}, status=400)
        for teacher_data in request.data:
            keys = teacher_data.keys()
            try:
                teacher = Teacher.objects.get(id=teacher_data.get('id'))
                if 'name' in keys:
                    teacher.name = teacher_data.get('name')
                if 'profile_link' in keys:
                    teacher.profile_link = teacher_data.get('profile_link')
                if 'not_work_from' in keys:
                    teacher.not_work_from = teacher_data.get('not_work_from')
            except:
                return Response({"text": "incorrect data"}, status=400)
            teacher.save()
        return Response(status=204)

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
    patch:Обновить данные групп в массиве\n
    Обновить данные групп в массиве
    delete:Удалить группы в массиве\n
    Удалить группы в массиве
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

    @swagger_auto_schema(request_body=PatchGroupSerializer(many=True), responses={204: "", 400: MessageSerializer()})
    def patch(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        review = PatchGroupSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for group_data in review.data:
            if not Group.objects.filter(id=group_data.get('id'), course__in=course).exists():
                return Response({"text": "Group id does not exist"}, status=400)
        for group_data in request.data:
            keys = group_data.keys()
            try:
                group = Group.objects.get(id=group_data.get('id'))
                if 'course' in keys:
                    group.course_id = group_data.get('course')
                if 'group_number' in keys:
                    group.group_number = group_data.get('group_number')
                group.save()
            except:
                return Response({"text": "incorrect data"}, status=400)
        return Response(status=204)

    @swagger_auto_schema(request_body=DeleteSerializer(), responses={200: GetGroupSerializer(many=True), 400: MessageSerializer()})
    def delete(self, request):
        institute_id = request.user.institute_id
        courses = Course.objects.filter(institute_id=institute_id)
        review = DeleteSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for id in review.data.get('id'):
            if not Group.objects.filter(id=id, course__in=courses).exists():
                return Response({"text": "Group id does not exist"}, status=400)
        for id in review.data.get('id'):
            Group.objects.filter(id=id, course__in=courses).delete()
        serialize = Group.objects.filter(course__in=courses)
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
    patch:Обновить данные предметов в массиве\n
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

    @swagger_auto_schema(request_body=PatchSubjectSerializer(many=True), responses={204: "", 400: MessageSerializer()})
    def patch(self, request):
        institute_id = request.user.institute_id
        review = PatchSubjectSerializer(data=request.data, many=True)
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
            if 'block_id' in keys:
                block = Block.objects.filter(id=subject_data.get('block_id'))
                if not block.exists():
                    return Response({"text": "Block_id does not exist"}, status=400)
                subject.block_id = subject_data.get('block_id')
            subject.save()
        return Response(status=204)

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
    is_even_week {\n1: \"ODD_WEEK\",\n 2: \"EVEN_WEEK\",\n 3: \"ALL_WEEKS\"\n}
    type {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n

post:Добавление занятий(экземпляров) в массиве\n
    is_even_week {\n1: \"ODD_WEEK\",\n 2: \"EVEN_WEEK\",\n 3: \"ALL_WEEKS\"\n}
    type {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n

patch:Обновить данные занятий(экземпляров) в массиве\n
    is_even_week {\n1: \"ODD_WEEK\",\n 2: \"EVEN_WEEK\",\n 3: \"ALL_WEEKS\"\n}
    type {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n

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

    @swagger_auto_schema(request_body=PatchLessonSerializer(many=True), responses={204: "", 400: MessageSerializer()})
    def patch(self, request):
        institute_id = request.user.institute_id
        review = PatchLessonSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        courses = Course.objects.filter(institute_id=institute_id)
        blocks = Block.objects.filter(course__in=courses)
        subjects = Subject.objects.filter(block__in=blocks)
        for lesson_data in review.data:
            if not Lesson.objects.filter(id=lesson_data.get('id'), subject__in=subjects).exists():
                return Response({"text": "Lesson id does not exist"}, status=400)
        for lesson_data in request.data:
            keys = lesson_data.keys()
            lesson = Lesson.objects.get(id=lesson_data.get('id'))
            try:
                if 'day_name' in keys:
                    lesson.day_name = lesson_data.get('day_name')
                if 'start_time' in keys:
                    lesson.start_time = lesson_data.get('start_time')
                if 'end_time' in keys:
                    lesson.end_time = lesson_data.get('end_time')
                if 'type' in keys:
                    lesson.type = lesson_data.get('type')
                if 'is_even_week' in keys:
                    lesson.is_even_week = lesson_data.get('type')
                if 'teacher' in keys:
                    if Teacher.objects.filter(id=lesson_data.get('teacher'), institute_id=institute_id).exists():
                        lesson.teacher_id = lesson_data.get('teacher')
                    else:
                        return Response({"text": "incorrect teacher"}, status=400)
                if 'subject' in keys:
                    if Subject.objects.filter(id=lesson_data.get('subject'), block__in=blocks).exists():
                        lesson.subject_id = lesson_data.get('subject')
                    else:
                        return Response({"text": "incorrect subject"}, status=400)
                if 'classroom' in keys:
                    lesson.classroom = lesson_data.get('classroom')
                if 'group' in keys:
                    if Group.objects.filter(id=lesson_data.get('group'), course__in=courses).exists():
                        lesson.group_id = lesson_data.get('group')
                    else:
                        return Response({"text": "incorrect group"}, status=400)
                if 'links' in keys:
                    lesson.links = lesson_data.get('links')
            except:
                return Response({"text": "Some data is incorrect"}, status=400)
            lesson.save()
        return Response(status=204)

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


class GetCurrentWeek(APIView):
    """
    get: Получить четность текущей недели
    Получить четность текущей недели
    """

    @swagger_auto_schema(responses={200: EvenWeekSerializer(), 400: MessageSerializer()})
    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return Response({"text": "Group_id does not exist"}, status=400)
        cur_week = datetime.now().isocalendar()[1]
        first_sem_start = Group.objects.get(id=group_id).course.institute.first_sem_start
        second_sem_start = Group.objects.get(id=group_id).course.institute.second_sem_start
        if datetime.now().date() < second_sem_start:
            start = first_sem_start.isocalendar()[1]
        else:
            start = second_sem_start.isocalendar()[1]
        is_even_week = True if ((cur_week - start + 1) % 2 == 0) else False
        result = {"even_week": is_even_week}
        return Response(result)


class GetTimetable(APIView):
    """
    post:Получить рассписание

    is_even_week : {\n1: \"ODD_WEEK\",\n 2: \"EVEN_WEEK\",\n 3: \"ALL_WEEKS\"\n}
    type : {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n
    """

    @swagger_auto_schema(request_body=GetTimeTableSerializer(), responses={200: TimeTableSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        cur_week = datetime.now().isocalendar()[1]
        review = GetTimeTableSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        if not Group.objects.filter(id = review.data.get("group_id")).exists():
            return Response({"text": "group does not exists"}, status=400)
        course_id = Group.objects.get(id = review.data.get("group_id")).course_id
        block_id = Block.objects.get(course_id=course_id, name=None).id
        group_subjects = Subject.objects.filter(block_id=block_id)

        first_sem_start = Group.objects.get(id=review.data.get("group_id")).course.institute.first_sem_start
        second_sem_start = Group.objects.get(id=review.data.get("group_id")).course.institute.second_sem_start
        if datetime.now().date() < second_sem_start:
            start = first_sem_start.isocalendar()[1]
        else:
            start = second_sem_start.isocalendar()[1]
        is_even_week = True if ((cur_week-start+1) % 2 == 0) else False
        if review.data.get("current_week") == None:
            if is_even_week:
                weeks = [2, 3]
            else:
                weeks = [1, 3]
        else:
            if review.data.get("current_week"):
                if is_even_week:
                    weeks = [2, 3]
                else:
                    weeks = [1, 3]
            else:
                if is_even_week:
                    weeks = [1, 3]
                else:
                    weeks = [2, 3]
        if not review.data.get("dop_course_id"):
            serialize = Lesson.objects.filter(group_id=review.data.get("group_id"), subject__in=group_subjects, is_even_week__in=weeks)
        else:
            for i in review.data.get("dop_course_id"):
                if not Subject.objects.filter(id=i).exists():
                    return Response({"text": "extra course does not exists"}, status=400)

            serialize = Lesson.objects.filter(Q(group_id=review.data.get("group_id"), subject_id__in=review.data.get("dop_course_id"), is_even_week__in=weeks) |
                                              Q(group_id=review.data.get("group_id"), subject__in=group_subjects, is_even_week__in=weeks))

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
    post:Добавление курсов в массиве\n
    Добавление курсов в массиве
    patch:Обновить данные курсов в массиве\n
    Обновить данные курсов в массиве
    delete:Удалить курсы в массиве\n
    Удалить курсы в массиве
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: CourseSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        serialize = Course.objects.filter(institute_id=institute_id)
        result = CourseSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=PostCourseSerializer(), responses={200: CourseSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        review = PostCourseSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for course_number in review.data.get("course_number"):
            if Course.objects.filter(institute_id=institute_id, course_number=course_number).exists():
                return Response({"text": "Course already exist"}, status=400)
        for course_number in review.data.get("course_number"):
            Course(institute_id=institute_id, course_number=course_number).save()
        serialize = Course.objects.filter(institute_id=institute_id)
        result = CourseSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=PatchCourseSerializer(many=True), responses={204: "", 400: MessageSerializer()})
    def patch(self, request):
        institute_id = request.user.institute_id
        review = PatchCourseSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for course_data in review.data:
            if not Course.objects.filter(id=course_data.get('id'), institute_id=institute_id).exists():
                return Response({"text": "Course id does not exist"}, status=400)
        for course_data in request.data:
            course = Course.objects.get(id=course_data.get("id"))
            course.course_number = course_data.get("course_number")
            course.save()
        return Response(status=204)

    @swagger_auto_schema(request_body=DeleteSerializer(), responses={200: CourseSerializer(many=True), 400: MessageSerializer()})
    def delete(self, request):
        institute_id = request.user.institute_id
        review = DeleteSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for id in review.data.get('id'):
            if not Course.objects.filter(id=id, institute_id=institute_id).exists():
                return Response({"text": "Course id does not exist"}, status=400)
        for id in review.data.get('id'):
            Course.objects.get(id=id).delete()
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


class GetChange(APIView):
    """
get: Получить изменения\n
    type {\n1: \"CANCEL\",\n 2: \"DAY_CHANGE\",\n 3: \"TIME_CHANGE\",\n 4: \"TEACHER_CHANGE\",\n 5: \"FORMAT_CHANGE\"\n}
    format_change {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n

post:Добавление изменений в массиве\n
    type {\n1: \"CANCEL\",\n 2: \"DAY_CHANGE\",\n 3: \"TIME_CHANGE\",\n 4: \"TEACHER_CHANGE\",\n 5: \"FORMAT_CHANGE\"\n}
    format_change {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n

patch:Обновить изменения в массиве\n
    type {\n1: \"CANCEL\",\n 2: \"DAY_CHANGE\",\n 3: \"TIME_CHANGE\",\n 4: \"TEACHER_CHANGE\",\n 5: \"FORMAT_CHANGE\"\n}
    format_change {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n

delete:Удалить изменения в массиве\n
    type {\n1: \"CANCEL\",\n 2: \"DAY_CHANGE\",\n 3: \"TIME_CHANGE\",\n 4: \"TEACHER_CHANGE\",\n 5: \"FORMAT_CHANGE\"\n}
    format_change {\n1: \"ONLINE_PRACTICE\",\n 2: \"OFFLINE_PRACTICE\",\n 3: \"ONLINE_LECTURE\",\n 4: \"OFFLINE_LECTURE\",\n 5: \"CANCELED\"\n}\n
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ChangesSerializer(many=True), 400: MessageSerializer()})
    def get(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        subject = Subject.objects.filter(block__in=block)
        lesson = Lesson.objects.filter(subject__in=subject)
        serialize = Changes.objects.filter(lesson__in=lesson)
        result = ChangesSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=ChangesSerializer(many=True), responses={200: ChangesSerializer(many=True), 400: MessageSerializer()})
    def post(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        subject = Subject.objects.filter(block__in=block)
        lesson = Lesson.objects.filter(subject__in=subject)
        review = ChangesSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        review.save()
        serialize = Changes.objects.filter(lesson__in=lesson)
        result = ChangesSerializer(serialize, many=True).data
        return Response(result)

    @swagger_auto_schema(request_body=PatchChangeSerializer(many=True), responses={204: "", 400: MessageSerializer()})
    def patch(self, request):
        institute_id = request.user.institute_id
        review = PatchChangeSerializer(data=request.data, many=True)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        courses_id = Course.objects.filter(institute_id=institute_id)
        blocks = Block.objects.filter(course_id__in=courses_id)
        subject = Subject.objects.filter(block__in=blocks)
        lesson = Lesson.objects.filter(subject__in=subject)
        for changes_data in review.data:
            if not Changes.objects.filter(id=changes_data.get('id'), lesson__in=lesson).exists():
                return Response({"text": "Change id does not exist"}, status=400)
        for changes_data in request.data:
            keys = changes_data.keys()
            changes = Changes.objects.get(id=changes_data.get('id'))
            try:
                if 'start_date' in keys:
                    changes.start_date = changes_data.get('start_date')
                if 'end_date' in keys:
                    changes.end_date = changes_data.get('end_date')
                if 'lesson' in keys:
                    changes.lesson_id = changes_data.get('lesson')
                if 'type' in keys:
                    changes.type = changes_data.get('type')
                if 'day_change' in keys:
                    changes.day_change = changes_data.get('day_change')
                if 'time_change_start' in keys:
                    changes.time_change_start = changes_data.get('time_change_start')
                if 'time_change_end' in keys:
                    changes.time_change_end = changes_data.get('time_change_end')
                if 'teacher_change' in keys:
                    changes.teacher_change_id = changes_data.get('teacher_change')
                if 'format_change' in keys:
                    changes.format_change = changes_data.get('format_change')
                if 'comment' in keys:
                    changes.comment = changes_data.get('comment')
            except:
                return Response({"text": "incorrect data"}, status=400)
            changes.save()
        return Response(status=204)

    @swagger_auto_schema(request_body=DeleteSerializer(), responses={200: ChangesSerializer(many=True), 400: MessageSerializer()})
    def delete(self, request):
        institute_id = request.user.institute_id
        course = Course.objects.filter(institute_id=institute_id)
        block = Block.objects.filter(course__in=course)
        subject = Subject.objects.filter(block__in=block)
        lesson = Lesson.objects.filter(subject__in=subject)
        review = DeleteSerializer(data=request.data)
        if not review.is_valid():
            return Response({"text": "incorrect data"}, status=400)
        for id in review.data.get('id'):
            if not Changes.objects.filter(id=id, lesson__in=lesson).exists():
                return Response({"text": "Change id does not exist"}, status=400)
        for id in review.data.get('id'):
            Changes.objects.filter(id=id).delete()
        serialize = Changes.objects.filter(lesson__in=lesson)
        result = ChangesSerializer(serialize, many=True).data
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
