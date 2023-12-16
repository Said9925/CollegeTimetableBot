from http import HTTPStatus

from bs4 import BeautifulSoup
import requests

from config import SCHEDULE_TABLE, URL, PERMANENT_ITEM, COLUMN_COUNT, NUMBER_DAYS_WEEK
from info_week import week_info


number_week = int(week_info[2][0])
day_week = week_info[1]


subject_week = -1
subject_information = 0
subject_time = 1

def fetch_schedule(gruppa):
    json_data = {"gruppa": gruppa.upper()}
    response = requests.post(URL, json=json_data)
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
                SCHEDULE_TABLE[int(el["trnum"]) - (int(el["trnum"]) // COLUMN_COUNT) * COLUMN_COUNT],
                int(el["nedel"]),
            ]

    for number in sorted(subjects):
        subject = subjects[number]
        if 0 < number <= 20:
            days_week["Понедельник"].append(subject)
        elif 20 < number <= 40:
            days_week["Вторник"].append(subject)
        elif 40 < number <= 60:
            days_week["Среда"].append(subject)
        elif 60 < number <= 80:
            days_week["Четверг"].append(subject)
        elif 80 < number <= 100:
            days_week["Пятница"].append(subject)
        elif 100 < number <= 120:
            days_week["Суббота"].append(subject)

    return days_week


def day_schedule(gruppa):
    days_week = fetch_schedule(gruppa)
    message = ""
    week_information = ""
    for week in week_info:
        week_information += f"{week} \n"

    for day in days_week[day_week]:
        
        if day[subject_week] in (number_week, PERMANENT_ITEM):
            message += f"{day[subject_information]}\n{day[subject_time]}\n"
        message += "\n"

    if message:
        return f"{week_information} \n{message}"
    return "Группа не найдена"


def week_schedule(gruppa):
    days_week = fetch_schedule(gruppa)
    message = ""
    for day_week in days_week:
        message += f"{day_week}\n"
        
        for day in days_week[day_week]:
            
            if day[subject_week] in (number_week, PERMANENT_ITEM):
                message += f"{day[subject_information]}\n{day[subject_time]}\n"
                
            message += "\n"

    if len(message.split()) > NUMBER_DAYS_WEEK:
        return message
    return "Группа не найдена"
