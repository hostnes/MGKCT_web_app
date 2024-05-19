from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LessonsView, LessonsByGroupView, GetTeachersView, TeachersList

urlpatterns = [
    path('get_groups_data/', LessonsView.as_view()),
    path('get_data_by_group/<str:pk>', LessonsByGroupView.as_view()),
    path('get_teachers/', TeachersList.as_view()),
]
