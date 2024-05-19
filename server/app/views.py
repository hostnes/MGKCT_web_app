import os
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.views import APIView
from app.models import Teacher
from app.serializers import TeacherSerializer


class LessonsView(APIView):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'lessons1.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


class LessonsByGroupView(APIView):
    def get(self, request, group):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'lessons1.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        group_data = data['lessons'][str(group)]
        result = {}
        result['info'] = data['info']
        result['info']['group'] = group
        result['lessons'] = group_data
        return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})


class TeachersList(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class GetTeachersView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        print(teachers)
        return JsonResponse(teachers, safe=False, json_dumps_params={'ensure_ascii': False})

