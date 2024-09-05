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
        file_path = os.path.join(settings.BASE_DIR, 'data', 'students_week_lessons.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


class TeachersLessonsView(APIView):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'teachers_week_lessons.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


class TeachersList(generics.ListAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.all().order_by('name')



class GroupsList(APIView):
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
        file_path = os.path.join(settings.BASE_DIR, 'data', 'students_week_lessons.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(data)
        for day in data:
            if group in day:
                #return JsonResponse(day, safe=False, json_dumps_params={'ensure_ascii': False})
                return Response(day)
        # Возвращаем сообщение об ошибке, если группа не найдена
        return JsonResponse({'error': 'Group not found'}, status=404, json_dumps_params={'ensure_ascii': False})

#class WeekGroupsLessonsView(APIView):
#    def get(self, request, group):
#        clean_data = []
#        clean_dict = {}
#        file_path = os.path.join(settings.BASE_DIR, 'data', 'students_week_lessons.json')
#        with open(file_path, 'r') as file:
#            data = json.load(file)
#
#        for day in data:
#            if group in day:
#                return JsonResponse(day, safe=False, json_dumps_params={'ensure_ascii': False})


class WeekTeachersLessonsView(APIView):
    def get(self, request, teacher):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'teachers_week_lessons.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        for item in data:
            for key, value in item.items():
                if key.split(" ")[0] == teacher:
                    return JsonResponse(value, safe=False, json_dumps_params={'ensure_ascii': False})

        return JsonResponse([], safe=False, json_dumps_params={'ensure_ascii': False})




