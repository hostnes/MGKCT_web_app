import time
from datetime import datetime

from celery import shared_task
import os
from requests_html import HTMLSession
from django.conf import settings
from bs4 import BeautifulSoup
import json


def fetch_html(url, timeout=60, retries=3):
    session = HTMLSession()
    response = session.get(url)
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to render {url}")
            response.html.render(timeout=timeout)
            print(f"Successfully rendered {url}")
            break
        except:
            print(f"Timeout exceeded, attempt {attempt + 1} of {retries}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(5)
            else:
                raise
    return response.html.html

def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    main_lxml = soup.find("div", id="main-p")
    return main_lxml.find("div", class_="content")


def calculate_students_lesson_title(data):
    lessons = ""
    total_count = 1
    count = 0
    for i in data:
        if count < 2:
            lessons += i
            lessons += ' '
            count += 1
        else:
            lessons += i
            lessons += ' '
            count += 1
            if len(data) != total_count:
                lessons += "\n"
            count = 0
        total_count += 1
    return lessons

def calculate_students_cabinets_title(data):
    cabinets = ""
    count = 0
    for i in data:
        cabinets += i
        cabinets += ' '
        count += 1
    return cabinets


@shared_task
def pars_students_week():
    url = 'https://mgkct.minskedu.gov.by/персоналии/учащимся/расписание-занятий-на-неделю'
    html = fetch_html(url)
    content_lxml = parse_html(html)

    groups = []
    global_students_count = 0
    for i in content_lxml.find_all("h2"):
        groups.append(i.text.split("-")[-1].strip())
    clean_data = []
    for student in content_lxml.find_all("div"):
        student_week_lxml = content_lxml.find_all("div")[global_students_count].find_all("tr")
        lessons = []
        day_count = 1
        count = 2
        week_data = []
        day_data = {}
        lessons_count = 1
        info = {}
        clean_student_data = {}
        table_lessons = 0
        for i in range(2, 8):
            info['week_day'] = student_week_lxml[0].find_all("th")[day_count].text.split(" ")[0].split(",")[0]
            info['day'] = student_week_lxml[0].find_all("th")[day_count].text.split(" ")[-1]
            day_data["info"] = info
            lesson = {}
            try:
                for lesson_lxml in student_week_lxml[i].find_all("td")[0::2]:
                    lesson["number_lesson"] = lessons_count
                    if " " == str(student_week_lxml[count].find_all("td")[table_lessons].text):
                        lesson["title"] = "-"
                    else:
                        td_text = student_week_lxml[count].find_all("td")[table_lessons].get_text(separator="|")

                        td_elements = [elem.strip() for elem in td_text.split('|') if elem.strip()]
                        lesson["title"] = calculate_students_lesson_title(td_elements)
                    if " " == str(student_week_lxml[count].find_all("td")[table_lessons + 1].text):
                        lesson["cabinet"] = "-"
                    else:
                        td_text = student_week_lxml[count].find_all("td")[table_lessons + 1].get_text(separator="|")
                        td_elements = [elem.strip() for elem in td_text.split('|') if elem.strip()]
                        if len(td_elements) > 1:
                            cabiinets = ""
                        lesson["cabinet"] = calculate_students_cabinets_title(td_elements)
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

        clean_student_data[groups[global_students_count]] = week_data
        clean_data.append(clean_student_data)
        global_students_count += 1

    file_path = os.path.join(settings.BASE_DIR, 'data', 'students_week_lessons.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)


@shared_task
def pars_teachers_week():
    url = 'https://mgkct.minskedu.gov.by/персоналии/преподавателям/расписание-занятий-на-неделю'
    html = fetch_html(url)
    content_lxml = parse_html(html)

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

                if teacher_week_lxml[count].find_all("td")[table_lessons].text.partition("-")[2].strip() == "":
                    lesson["title"] = "-"
                    lesson["group"] = "-"
                else:
                    lesson["title"] = str(teacher_week_lxml[count].find_all("td")[table_lessons].text.partition("-")[2].strip())
                    lesson["group"] = str(teacher_week_lxml[count].find_all("td")[table_lessons].text.split("-")[0])
                if " " == str(teacher_week_lxml[count].find_all("td")[table_lessons + 1].text):
                    lesson["cabinet"] = "-"
                else:
                    lesson["cabinet"] = str(teacher_week_lxml[count].find_all("td")[table_lessons + 1].text)

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