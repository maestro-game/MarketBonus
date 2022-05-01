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
    path("dekanat/addTeacher/", views.AddTeacher.as_view()),
    path("dekanat/addGroup/", views.AddGroup.as_view()),
    path("dekanat/addBlock/", views.AddBlock.as_view()),
    path("dekanat/addSubject/", views.AddSubject.as_view()),
    path("dekanat/getCourse/", views.GetCourse.as_view()),
    path("dekanat/getAccount/", views.GetAccount.as_view()),
    path("dekanat/GetTable/", views.GetTable.as_view()),
]