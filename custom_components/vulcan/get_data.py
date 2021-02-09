import asyncio
import datetime
import json
from datetime import timedelta

from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_platform, service
from homeassistant.helpers.entity import Entity
from vulcan import Account, Keystore, Vulcan, VulcanHebe

from . import DOMAIN, client


async def get_lesson_info(student_id, date_from=None, date_to=None, type_="dict"):
    dict_ans = {}
    list_ans = []
    async for Lesson in await client.data.get_lessons(
        date_from=date_from, date_to=date_to
    ):
        temp_dict = {}
        temp_dict["number"] = Lesson.time.position
        lesson = str(Lesson.time.position)
        temp_dict["lesson"] = Lesson.subject.name
        if Lesson.room is not None:
            temp_dict["room"] = Lesson.room.code
        else:
            temp_dict["room"] = "-"
        temp_dict["visible"] = Lesson.visible
        temp_dict["changes"] = Lesson.changes
        temp_dict["group"] = Lesson.group
        temp_dict["teacher"] = Lesson.teacher.display_name
        temp_dict["time"] = (
            Lesson.time.from_.strftime("%H:%M") + "-" + Lesson.time.to.strftime("%H:%M")
        )
        if temp_dict["changes"] == None:
            temp_dict["changes"] = ""
        if "przeniesiona na lekcję" in temp_dict["changes"]:
            temp_dict["lesson"] = "Lekcja przeniesiona (" + temp_dict["lesson"] + ")"
        elif "przeniesiona z lekcji" in temp_dict["changes"]:
            temp_dict["lesson"] = temp_dict["lesson"] + " " + temp_dict["changes"]
        elif (
            "odwołana" in temp_dict["changes"]
            or "Okienko" in temp_dict["changes"]
            or "nieobecność" in temp_dict["changes"]
            or "okienko" in temp_dict["changes"]
        ):
            temp_dict["lesson"] = "Lekcja odwołana (" + temp_dict["lesson"] + ")"
        if temp_dict["visible"] == True:
            if type_ == "dict":
                dict_ans["lesson_" + lesson] = temp_dict
            elif type_ == "list":
                list_ans.append(temp_dict)

    for num in range(10):
        if not "lesson_" + str(num + 1) in dict_ans:
            dict_ans["lesson_" + str(num + 1)] = {
                "number": num + 1,
                "lesson": "-",
                "room": "-",
                "group": "-",
                "teacher": "-",
                "time": "-",
                "changes": "-",
            }
    if type_ == "dict":
        return dict_ans
    elif type_ == "list":
        return list_ans


async def get_student_info(student_id):
    student_info = {}
    for student in await client.get_students():
        if str(student.pupil.id) == str(student_id):
            student_info["first_name"] = student.pupil.first_name
            if student.pupil.second_name:
                student_info["second_name"] = student.pupil.second_name
            student_info["last_name"] = student.pupil.last_name
            student_info["full_name"] = (
                student.pupil.first_name + " " + student.pupil.last_name
            )
            student_info["id"] = student.pupil.id
            student_info["class"] = ""  # student.class_.name
            student_info["school"] = student.school.name
    return student_info


async def get_lucky_number():
    lucky_number = {}
    number = await client.data.get_lucky_number()
    try:
        lucky_number["number"] = number.number
        lucky_number["date"] = number.date.strftime("%d.%m.%Y")
    except:
        lucky_number = {"number": "-", "date": "-"}
    return lucky_number


async def get_latest_attendance(student_id):
    latest_attendance = {}
    async for attendance in await client.data.get_attendance():
        if attendance.presence_type != None:
            latest_attendance["content"] = attendance.presence_type.name
            latest_attendance["lesson_name"] = attendance.subject.name
            latest_attendance["lesson_number"] = attendance.time.position
            latest_attendance["lesson_date"] = str(attendance.date.date)
            latest_attendance["lesson_time"] = (
                attendance.time.from_.strftime("%H:%M")
                + "-"
                + attendance.time.to.strftime("%H:%M")
            )
            latest_attendance["datetime"] = attendance.date_modified.date_time

    if latest_attendance == {}:
        latest_attendance = {
            "content": "-",
            "lesson_name": "-",
            "lesson_number": "-",
            "lesson_date": "-",
            "lesson_time": "-",
            "datetime": "-",
        }

    return latest_attendance


async def get_latest_grade(student_id):
    latest_grade = {}

    async for grade in await client.data.get_grades():
        latest_grade = {}
        latest_grade["content"] = grade.content
        latest_grade["weight"] = grade.column.weight
        latest_grade["description"] = grade.column.name
        latest_grade["value"] = grade.value
        latest_grade["teacher"] = grade.teacher_created.display_name
        latest_grade["subject"] = grade.column.subject.name
        latest_grade["date"] = grade.date_created.date.strftime("%d.%m.%Y")

    if latest_grade == {}:
        latest_grade = {
            "content": "-",
            "date": "-",
            "weight": "-",
            "description": "-",
            "subject": "-",
            "teacher": "-",
            "value": 0,
        }

    return latest_grade


async def get_next_homework(student_id):
    next_homework = {}
    async for homework in await client.data.get_homework():
        for i in range(7):
            if (
                homework.deadline.date >= datetime.date.today()
                and homework.deadline.date <= datetime.date.today() + timedelta(i)
            ):
                next_homework = {}
                next_homework["description"] = homework.content
                next_homework["subject"] = homework.subject.name
                next_homework["teacher"] = homework.creator.display_name
                next_homework["date"] = homework.deadline.date.strftime("%d.%m.%Y")
                if homework.content != None:
                    break

    if next_homework == {}:
        next_homework = {
            "description": "Brak zadań domowych",
            "subject": "w najbliższym tygodniu",
            "teacher": "-",
            "date": "-",
        }

    return next_homework


async def get_next_exam(student_id):
    next_exam = {}
    async for exam in await client.data.get_exams():
        for i in range(7):
            if (
                exam.deadline.date >= datetime.date.today()
                and exam.deadline.date <= datetime.date.today() + timedelta(i)
            ):
                next_exam = {}
                next_exam["description"] = exam.topic
                if exam.topic == "":
                    next_exam["description"] = exam.type + " " + exam.subject.name
                next_exam["subject"] = exam.subject.name
                next_exam["type"] = exam.type
                next_exam["teacher"] = exam.creator.display_name
                next_exam["date"] = exam.deadline.date.strftime("%d.%m.%Y")
                if exam.type != None:
                    break

    if next_exam == {}:
        next_exam = {
            "description": "Brak sprawdzianów",
            "subject": "w najbliższym tygodniu",
            "type": "-",
            "teacher": "-",
            "date": "-",
        }

    return next_exam


def get_latest_message(self):
    with open("vulcan.json") as f:
        certificate = json.load(f)
    self.latest_message = {}

    for message in Vulcan(certificate).get_messages():
        temp_dict = {}
        temp_dict["title"] = message.title
        temp_dict["content"] = message.content
        if message.sender is not None:
            temp_dict["sender"] = message.sender.name
        else:
            temp_dict["sender"] = "Nieznany"
        temp_dict["date"] = (
            message.sent_date.strftime("%Y.%m.%d")
            + " "
            + message.sent_time.strftime("%H:%M")
        )
        setattr(self, "latest_message", temp_dict)

    if self.latest_message == {}:
        self.latest_message = {
            "title": "-",
            "content": "-",
            "date": "-",
            "sender": "-",
        }

    return self.latest_message
