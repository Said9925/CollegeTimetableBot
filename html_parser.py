from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from config import SCHEDULE_TABLE, URL
from info_week import week_info


number_week = int(week_info[2][0])
day_week = week_info[1]


def fetch_schedule(gruppa):
    response = requests.post(URL, json={"gruppa": gruppa.upper()})
    subjects = {}

    days_week = {
        "Понедельник": [],
        "Вторник": [],
        "Среда": [],
        "Четверг": [],
        "Пятница": [],
        "Суббота": [],
    }

    if response.status_code == HTTPStatus.OK:
        response_html = response.text
        soup = BeautifulSoup(response_html, "html.parser")

        gruppa = soup.find_all("div", class_="gruppa") + soup.find_all("div", class_="gruppaPoOdnoyNedele")
        for el in gruppa:
            subjects[int(el["trnum"])] = [
                " ".join(el.text.strip().split()),
                SCHEDULE_TABLE[int(el["trnum"]) - (int(el["trnum"]) // 20) * 20],
                int(el["nedel"]),
            ]

    for number in sorted(subjects):
        if 0 < number <= 20:
            days_week["Понедельник"].append(subjects[number])
        elif 20 < number <= 40:
            days_week["Вторник"].append(subjects[number])
        elif 40 < number <= 60:
            days_week["Среда"].append(subjects[number])
        elif 60 < number <= 80:
            days_week["Четверг"].append(subjects[number])
        elif 80 < number <= 100:
            days_week["Пятница"].append(subjects[number])
        elif 100 < number <= 120:
            days_week["Суббота"].append(subjects[number])

    return days_week


def day_schedule(gruppa):
    days_week = fetch_schedule(gruppa)
    message = ""
    week_information = ""
    for week in week_info:
        week_information += week + "\n"

    for day in days_week[day_week]:
        if day[2] in (number_week, 3):
            message += f"{day[0]}\n{day[1]}\n"
        message += "\n"

    if message:
        return f"{week_information} \n{message}"
    else:
        return "Группа не найдена"


def week_schedule(gruppa):
    days_week = fetch_schedule(gruppa)
    message = ""
    for day_week in days_week:
        message += f"{day_week}\n"
        for day in days_week[day_week]:
            if day[-1] in (number_week, 3):
                message += f"{day[0]}\n{day[1]}\n"
            message += "\n"

    if len(message.split()) > 6:
        return message
    else:
        return "Группа не найдена"
