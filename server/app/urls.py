from django.urls import path

from .views import LessonsView

urlpatterns = [
    path('get_groups_data/', LessonsView.as_view()),
]