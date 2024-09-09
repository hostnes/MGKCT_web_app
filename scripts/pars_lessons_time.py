import json
import os
from conf import DATA_DIR


def pars_lessons_time():
    clean_data = [
        {
            "info":
              {
                "week_day": 0
              },
            "lessons": {
                "1": "9:00 - 10:40",
                "2": "10:50 - 12:40",
                "3": "13:00 - 14:40",
                "4": "14:50 - 16:30",
                "5": "16:40 - 18:20"
              }
        },
        {
            "info":
              {
                "week_day": 1
              },
            "lessons": {
                "1": "9:00 - 10:40",
                "2": "10:50 - 12:40",
                "3": "13:00 - 14:40",
                "4": "14:50 - 16:30",
                "5": "16:40 - 18:20"
              }
        },
        {
            "info":
              {
                "week_day": 2
              },
            "lessons": {
                "1": "9:00 - 10:40",
                "2": "10:50 - 12:40",
                "3": "13:00 - 14:40",
                "4": "14:50 - 16:30",
                "5": "16:40 - 18:20"
              }
        },
        {
            "info":
              {
                "week_day": 3
              },
            "lessons": {
                "1": "9:00 - 10:40",
                "2": "10:50 - 12:40",
                "3": "13:00 - 14:40",
                "4": "14:50 - 16:30",
                "5": "16:40 - 18:20"
              }
        },
        {
            "info":
              {
                "week_day": 4
              },
            "lessons": {
                "1": "9:00 - 10:40",
                "2": "10:50 - 12:40",
                "3": "13:00 - 14:40",
                "4": "14:50 - 16:30",
                "5": "16:40 - 18:20"
              }
        },
        {
            "info":
              {
                "week_day": 5
              },
            "lessons": {
                "1": "9:00 - 10:40",
                "2": "10:50 - 12:40",
                "3": "13:00 - 14:40",
                "4": "14:50 - 16:30",
                "5": "16:40 - 18:20"
              }
        }
    ]
    file_path = os.path.join(DATA_DIR, "lessons_time.json")
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)
    print("Lessons time update successfully!")

pars_lessons_time()