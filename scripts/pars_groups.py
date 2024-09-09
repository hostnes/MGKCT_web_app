import json
import os
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from conf import DATA_DIR


def fetch_html(url):
    with HTMLSession() as session:
        response = session.get(url)
        response.html.render(timeout=60)
        return response.html.html


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    main_lxml = soup.find("div", id="main-p")
    return main_lxml


def pars_teachers():
    url = 'https://mgkct.minskedu.gov.by/персоналии/учащимся/расписание-занятий-на-неделю'
    html = fetch_html(url)
    content_lxml = parse_html(html)
    clean_data = []
    groups_lxml = content_lxml.find("div", class_="content")
    for group in groups_lxml.find_all("h2"):
        clean_data.append(group.text.split(" ")[-1])

    file_path = os.path.join(DATA_DIR, 'groups.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)


pars_teachers()
