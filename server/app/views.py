import os
import json
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.views import APIView
from app.models import Teacher
from app.serializers import TeacherSerializer
from rest_framework.response import Response


class GroupsLessonsView(APIView):
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


class GroupsList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        numbers = ["160*", "162*", "163*", "164*", "165*", "166*",
                   "8", "49", "50", "51", "52", "53", "54", "55",
                   "56", "57", "58", "59*", "60", "61", "62", "63",
                   "64", "65", "66", "67", "68", "69", "70", "71",
                   "72", "73", "74", "75", "76", "77", "78", "79",
                   "80", "81", "82", "83", "84"]
        return Response(numbers)


class WeekGroupsLessonsView(APIView):
    def get(self, request, group):
        clean_data = []
        clean_dict = {}
        file_path = os.path.join(settings.BASE_DIR, 'data', 'week_lessons.json')
        with open(file_path, 'r') as file:
            data = json.load(file)

        for day in data:
            clean_dict["info"] = day["info"]
            clean_dict[str(group)] = day["lessons"][group]
            clean_data.append(clean_dict)
            clean_dict = {}
        return JsonResponse(clean_data, safe=False, json_dumps_params={'ensure_ascii': False})



