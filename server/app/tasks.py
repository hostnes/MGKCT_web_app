from celery import shared_task
import datetime
import os
from requests_html import HTMLSession

from django.conf import settings

from bs4 import BeautifulSoup
import json


@shared_task
def pars_students_html():
    session = HTMLSession()
    response = session.get('https://mgkct.minskedu.gov.by/персоналии/учащимся/расписание-занятий-на-неделю')
    response.html.render()
    soup = BeautifulSoup(response.html.html, 'lxml')
    main_lxml = soup.find("div", id="main-p")
    content_lxml = main_lxml.find("div", class_="content")
    teachers = []
    global_teacher_count = 0
    for i in content_lxml.find_all("h2"):
        teachers.append(i.text.split("-")[-1].strip())
    clean_data = []
    for teacher in content_lxml.find_all("div"):
        teacher_week_lxml = content_lxml.find_all("div")[global_teacher_count].find_all("tr")
        lessons = []
        day_count = 1
        count = 2
        week_data = []
        day_data = {}
        lessons_count = 1
        info = {}
        clean_teacher_data = {}
        table_lessons = 0
        for i in range(2, 8):
            info['week_day'] = teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[0].split(",")[0]
            info['day'] = teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[-1]
            day_data["info"] = info
            lesson = {}
            try :
                for lesson_lxml in teacher_week_lxml[i].find_all("td")[0::2]:
                    lesson["number_lesson"] = lessons_count
                    lesson["title"] = str(
                        teacher_week_lxml[count].find_all("td")[table_lessons].text.partition("-")[2].strip())
                    if " " == str(teacher_week_lxml[count].find_all("td")[table_lessons + 1].text):
                        lesson["cabinet"] = "-"
                    else:
                        lesson["cabinet"] = str(teacher_week_lxml[count].find_all("td")[table_lessons + 1].text)
                    lessons.append(lesson)
                    lessons_count += 1
                    count += 1
                    lesson = {}
            except:
                for lesson_lxml in range(0, 5):
                    lesson["number_lesson"] = lessons_count
                    lesson["title"] = "-"
                    lesson["cabinet"] = "-"

                    lessons.append(lesson)
                    lessons_count += 1
                    count += 1
                    lesson = {}
            finally:
                count = 2
                day_data["lessons"] = lessons
                week_data.append(day_data)
                day_data = {}
                info = {}
                lessons_count = 1
                day_count += 1
                lessons = []
                table_lessons += 2

        clean_teacher_data[teachers[global_teacher_count]] = week_data
        clean_data.append(clean_teacher_data)
        global_teacher_count += 1
    file_path = os.path.join(settings.BASE_DIR, 'data', 'students_week_lessons.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)


@shared_task
def pars_teachers_week():
    session = HTMLSession()

    response = session.get('https://mgkct.minskedu.gov.by/персоналии/преподавателям/расписание-занятий-на-неделю')
    response.html.render()
    soup = BeautifulSoup(response.html.html, 'lxml')
    main_lxml = soup.find("div", id="main-p")
    content_lxml = main_lxml.find("div", class_="content")
    teachers = []
    global_teacher_count = 0
    for i in content_lxml.find_all("h2"):
        teachers.append(i.text.split("-")[-1].strip())
    clean_data = []
    for teacher in content_lxml.find_all("div"):
        teacher_week_lxml = content_lxml.find_all("div")[global_teacher_count].find_all("tr")
        lessons = []
        day_count = 1
        count = 2
        week_data = []
        day_data = {}
        lessons_count = 1
        info = {}
        clean_teacher_data = {}
        table_lessons = 0
        for i in range(2, 8):
            info['week_day'] = teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[0].split(",")[0]
            info['day'] = teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[-1]
            day_data["info"] = info
            lesson = {}
            for lesson_lxml in teacher_week_lxml[i].find_all("td")[0::2]:
                lesson["number_lesson"] = lessons_count
                lesson["title"] = str(teacher_week_lxml[count].find_all("td")[table_lessons].text.partition("-")[2].strip())
                if " " == str(teacher_week_lxml[count].find_all("td")[table_lessons + 1].text):
                    lesson["cabinet"] = "-"
                else:
                            lesson["cabinet"] = str(teacher_week_lxml[count].find_all("td")[table_lessons + 1].text)
                lesson["group"] = str(teacher_week_lxml[count].find_all("td")[table_lessons].text.split("-")[0])

                lessons.append(lesson)
                lessons_count += 1
                count += 1
                lesson = {}

            count = 2
            day_data["lessons"] = lessons
            week_data.append(day_data)
            day_data = {}
            info = {}
            lessons_count = 1
            day_count += 1
            lessons = []
            table_lessons += 2

        clean_teacher_data[teachers[global_teacher_count]] = week_data
        clean_data.append(clean_teacher_data)
        global_teacher_count += 1
    file_path = os.path.join(settings.BASE_DIR, 'data', 'teachers_week_lessons.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)