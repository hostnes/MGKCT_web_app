from celery import shared_task
import os
from requests_html import HTMLSession
from django.conf import settings
from bs4 import BeautifulSoup
import json


def fetch_html(url):
    with HTMLSession() as session:
        response = session.get(url)
        response.html.render()
        return response.html.html


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    main_lxml = soup.find("div", id="main-p")
    return main_lxml.find("div", class_="content")


@shared_task
def pars_students_html():
    url = 'https://mgkct.minskedu.gov.by/персоналии/учащимся/расписание-занятий-на-неделю'
    html = fetch_html(url)
    content_lxml = parse_html(html)

    teachers = [i.text.split("-")[-1].strip() for i in content_lxml.find_all("h2")]
    clean_data = []

    global_teacher_count = 0
    for teacher in content_lxml.find_all("div"):
        teacher_week_lxml = content_lxml.find_all("div")[global_teacher_count].find_all("tr")
        week_data = []

        for day_count in range(1, 6):  # Assuming 5 days of the week
            day_data = {}
            info = {
                'week_day': teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[0].split(",")[0],
                'day': teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[-1]
            }
            day_data["info"] = info
            lessons = []

            for lesson_count in range(2, 8):  # Assuming 6 lessons per day
                lesson = {}
                lesson_cells = teacher_week_lxml[lesson_count].find_all("td")[0::2]
                for table_lessons, lesson_cell in enumerate(lesson_cells):
                    lesson["number_lesson"] = lesson_count - 1
                    lesson["title"] = lesson_cell.text.partition("-")[2].strip()
                    lesson["cabinet"] = lesson_cell.find_next_sibling("td").text.strip() or "-"
                    lessons.append(lesson)

            day_data["lessons"] = lessons
            week_data.append(day_data)

        clean_teacher_data = {teachers[global_teacher_count]: week_data}
        clean_data.append(clean_teacher_data)
        global_teacher_count += 1

    file_path = os.path.join(settings.BASE_DIR, 'data', 'students_week_lessons.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)


@shared_task
def pars_teachers_week():
    url = 'https://mgkct.minskedu.gov.by/персоналии/преподавателям/расписание-занятий-на-неделю'
    html = fetch_html(url)
    content_lxml = parse_html(html)

    teachers = [i.text.split("-")[-1].strip() for i in content_lxml.find_all("h2")]
    clean_data = []

    global_teacher_count = 0
    for teacher in content_lxml.find_all("div"):
        teacher_week_lxml = content_lxml.find_all("div")[global_teacher_count].find_all("tr")
        week_data = []

        for day_count in range(1, 6):  # Assuming 5 days of the week
            day_data = {}
            info = {
                'week_day': teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[0].split(",")[0],
                'day': teacher_week_lxml[0].find_all("th")[day_count].text.split(" ")[-1]
            }
            day_data["info"] = info
            lessons = []

            for lesson_count in range(2, 8):  # Assuming 6 lessons per day
                lesson = {}
                lesson_cells = teacher_week_lxml[lesson_count].find_all("td")[0::2]
                for table_lessons, lesson_cell in enumerate(lesson_cells):
                    lesson["number_lesson"] = lesson_count - 1
                    lesson["title"] = lesson_cell.text
                    lesson["cabinet"] = lesson_cell.find_next_sibling("td").text.strip() or "-"
                    lesson["group"] = lesson_cell.text.split("-")[0]
                    lessons.append(lesson)

            day_data["lessons"] = lessons
            week_data.append(day_data)

        clean_teacher_data = {teachers[global_teacher_count]: week_data}
        clean_data.append(clean_teacher_data)
        global_teacher_count += 1

    file_path = os.path.join(settings.BASE_DIR, 'data', 'teachers_week_lessons.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)
