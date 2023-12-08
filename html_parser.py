from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from info_week import week_info


number_week = int(week_info[2][0])
day_week = week_info[1]


Schedule_table = {
    1: "(Начало- 9:00 | Конец - 10:00)",
    2: "(Начало- 9:00 | Конец - 10:00)",
    3: "(Начало- 10:10 | Конец - 11:10)",
    4: "(Начало- 10:10 | Конец - 11:10)",
    5: "(Начало - 11:20 | Конец - 12:20)",
    6: "(Начало - 11:20 | Конец - 12:20)",
    7: "(Начало - 13:00 | Конец - 14:00)",
    8: "(Начало - 13:00 | Конец - 14:00)",
    9: "(Начало - 14:10 | Конец - 15:10)",
    10: "(Начало - 14:10 | Конец - 15:10)",
    11: "(Начало - 15:20 | Конец - 16:20)",
    12: "(Начало - 15:20 | Конец - 16:20)",
    13: "(Начало - 16:30 | Конец - 17:30)",
    14: "(Начало - 16:30 | Конец - 17:30)",
    15: "(Начало - 17:40 | Конец - 18:40)",
    16: "(Начало - 17:40 | Конец - 18:40)",
}


def fetch_schedule(gruppa):
    url = "https://timetable.gstou.ru/User/TimeTablePartial"
    response = requests.post(url, json={"gruppa": gruppa.upper()})
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
                Schedule_table[int(el["trnum"]) - (int(el["trnum"]) // 20) * 20],
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
        week_information += week + '\n'

    for day in days_week[day_week]:
        if day[2] in (number_week, 3):
            for subject in range(2):
                message += day[subject]
                message += '\n'
            message += '\n'

    if message:
        return week_information + '\n' + message
    else:
        return "Группа не найдена"


def week_schedule(gruppa):
    days_week = fetch_schedule(gruppa)
    message = ""
    for day_week in days_week:
        message += f"{day_week}\n"
        for day in days_week[day_week]:
            if day[-1] in (number_week, 3):
                for subject in range(2):
                    message += day[subject]
                    message += '\n'
                message += '\n'
        message += '\n'

    if len(message.split()) > 6:
        return message
    else:
        return "Группа не найдена"


if __name__ == "__main__":
    day_schedule("your_group_name")
    week_schedule("your_group_name")