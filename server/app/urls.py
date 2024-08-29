from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import GroupsList, GroupsLessonsView, WeekGroupsLessonsView, TeachersList, TeachersLessonsView, WeekTeachersLessonsView

urlpatterns = [
    path('get_groups/', GroupsList.as_view()),
    path('get_groups_data/', GroupsLessonsView.as_view()),
    path('get_week_data_by_group/<str:group>', WeekGroupsLessonsView.as_view()),

    path('get_teachers/', TeachersList.as_view()),
    path('get_teachers_data/', TeachersLessonsView.as_view()),
    path('get_week_data_by_teacher/<str:teacher>', WeekTeachersLessonsView.as_view()),
]
