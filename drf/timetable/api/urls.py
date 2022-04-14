from django.urls import path

from . import views

urlpatterns = [
    path("timetable/", views.CreateTimeTable.as_view()),
]