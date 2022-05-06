from django.urls import path

from . import views

urlpatterns = [
    path("admin/timetable/", views.CreateTimeTable.as_view()),
    path("student/university/", views.GetUniversity.as_view()),
    path("student/instByUnivid/<int:id>", views.GetInstitute.as_view()),
    path("student/groupByInstId/<int:id>", views.GetGroup.as_view()),
    path("student/blockByGroupId/<int:id>", views.GetBlock.as_view()),
    path("student/dop_courseByBlockId/<int:id>", views.GetDopCourse.as_view()),
    path("student/timetable/", views.GetTimetable.as_view()),
    path("dekanat/teacher/", views.AddTeacher.as_view()),
    path("dekanat/group/", views.AddGroup.as_view()),
    path("dekanat/block/", views.AddBlock.as_view()),
    path("dekanat/subject/", views.AddSubject.as_view()),
    path("dekanat/course/", views.GetCourse.as_view()),
    path("dekanat/account/", views.GetAccount.as_view()),
    path("dekanat/lesson/", views.GetLesson.as_view()),
    path("dekanat/table/", views.GetTable.as_view()),
    path("token/logout/", views.LogoutView.as_view()),
# редактирование и удаление групп, пар, блоков, изменений
]