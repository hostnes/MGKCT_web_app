import os
import json
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView


class LessonsView(APIView):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'data', 'lessons.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
