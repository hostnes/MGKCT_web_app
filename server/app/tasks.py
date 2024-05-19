from celery import shared_task
import asyncio
import datetime
import os
from requests_html import HTMLSession

import requests
from django.conf import settings

import time
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

week_days = (
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',
)


number_week_days = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'понедельник',
}


@shared_task
def week_task():
    print('start')
    groups = []
    file_path = os.path.join(settings.BASE_DIR, 'data', 'day.html')
    with open(file_path) as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    group_lxml = soup.find('div', id="wrapperTables").find_all('div')
    for item in group_lxml[::2]:
        groups.append(item.text.strip().split(' ')[0])
    driver = webdriver.Remote('http://selenium:4444', desired_capabilities=DesiredCapabilities.CHROME)
    for i in groups:
        print(i)
        try:
            driver.get(url=f'https://mgkct.minskedu.gov.by/персоналии/учащимся/расписание-занятий-на-неделю?group={i}')
            with open('service/templates/week.html', 'w') as file:
                file.write(driver.page_source)
            driver.get(url=f"http://{os.environ['WEB_APP_HOST']}:8000/api/week/")
            driver.set_window_size(1900, 920)
            elements = driver.find_elements(By.CLASS_NAME, 'content')
            file_path = os.path.join(settings.BASE_DIR, 'data', '{}.png'.format(i))
            elements[-1].screenshot(file_path)
        except:
            pass
    driver.quit()


@shared_task
def pars_html():
    session = HTMLSession()

    groups = []
    data = {}
    global_lessons = {}
    file_path = os.path.join(settings.BASE_DIR, 'data', 'lessons.json')
    # file_path = "data/lessons.json"
    with open(file_path) as file:
        test = json.load(file)
    file_path = os.path.join(settings.BASE_DIR, 'data', 'day.html')
    # file_path = 'data/day.html'

    response = session.get('https://mgkct.minskedu.gov.by/персоналии/учащимся/расписание-занятий-на-день')
    response.html.render()
    with open(file_path, 'w') as file:
        file.write(response.html.html)
    print(123)
    with open(file_path) as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    group_lxml = soup.find('div', id="wrapperTables").find_all('div')
    week_day_today = group_lxml[0].text.strip().split(' ')[-1]
    if week_day_today != test['info']['week_day']:
        for item in group_lxml[::2]:
            groups.append(item.text.strip().split(' ')[0])
        if datetime.date.weekday(datetime.date.today()) == 5:
            datetime_now = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%d.%m.%y')
        else:
            datetime_now = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%y')
        data['info'] = {
            'day': datetime_now,
            'week_day': week_day_today
        }
        for group_number in groups:
            lessons = []
            group_obj = soup.find('div', string=f'{group_number} - {week_day_today}').find_next().find_all('tr')
            if len(group_obj) != 0:
                for i in range(0, len(group_obj[0].find_all('th'))):
                    lesson = {}
                    lesson['number_lesson'] = group_obj[0].find_all('th')[i].text.split('№')[-1]
                    lesson['title'] = group_obj[1].find_all('td')[i].text.strip()
                    try:
                        test_cab = []
                        test_cab_str = ''
                        for i in group_obj[2].find_all('td')[i]:
                            test_cab.append(i.text)
                        for i in test_cab:
                            if i == '':
                                test_cab_str += " "
                            test_cab_str += i
                        lesson['cabinet'] = test_cab_str
                    except:
                        lesson['cabinet'] = "-"
                    lessons.append(lesson)
                global_lessons[group_number] = lessons
            else:
                global_lessons[group_number] = [{
                    'number_lesson': None,
                    'title': None,
                    'cabinet': None,
                    }]
        data['lessons'] = global_lessons
        file_path = os.path.join(settings.BASE_DIR, 'data', 'lessons.json')
        # file_path = "data/lessons.json"
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)