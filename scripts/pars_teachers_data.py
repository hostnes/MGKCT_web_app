import json
import os
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import requests


def fetch_html(url):
    with HTMLSession() as session:
        response = session.get(url)
        response.html.render()
        return response.html.html


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    main_lxml = soup.find("div", id="main-p")
    return main_lxml


def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {path}")
    else:
        print(f"Failed to download image: {url}")


def pars_teachers():
    url = 'https://mgkct.minskedu.gov.by/о-колледже/портфолио/педагогический-коллектив'
    html = fetch_html(url)
    content_lxml = parse_html(html)
    clean_data = []
    global_count = 1

    images_dir = 'images'
    os.makedirs(images_dir, exist_ok=True)

    for teacher in content_lxml.find_all("div", class_="item"):
        img_url = "https://mgkct.minskedu.gov.by" + teacher.find("div", class_="preview").find("img")['src']
        img_name = f"teacher_{global_count}.jpg"

        # download_image(img_url, f"teachers/{img_name}")

        name = teacher.find("h3").text
        clean_data.append(
            {
                "model": "app.teacher",
                "pk": global_count,
                "fields": {
                    "name": name,
                    "img_path": f"teachers/{img_name}"
                }
            },
        )
        global_count += 1

    file_path = 'data.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(clean_data, file, indent=4, ensure_ascii=False)


pars_teachers()
