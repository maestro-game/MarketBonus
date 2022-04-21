from django.urls import path

from . import views

urlpatterns = [
    path("timetable/", views.CreateTimeTable.as_view()),
    path("university/", views.GetUniversity.as_view()),
    path("instByUnivid/<int:id>", views.GetInstitute.as_view()),
    path("groupByInstId/<int:id>", views.GetGroup.as_view()),
    path("blockByGroupId/<int:id>", views.GetBlock.as_view()),
    path("courseByBlockId/<int:id>", views.GetCourse.as_view()),
    path("courseByBlockId/<int:id>", views.GetCourse.as_view()),
    path("addTeacher/", views.AddTeacher.as_view()),
    path("addGroup/", views.AddGroup.as_view()),
]