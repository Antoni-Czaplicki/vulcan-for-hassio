import asyncio
import datetime
from datetime import timedelta
import json

from vulcan import Account, Keystore, Vulcan, VulcanHebe

from homeassistant.helpers import config_validation as cv, entity_platform, service
from homeassistant.helpers.entity import Entity

from . import DOMAIN
from .const import CONF_STUDENT_NAME

with open(".vulcan/keystore.json") as f:
    keystore = Keystore.load(f)
with open(".vulcan/account.json") as f:
    account = Account.load(f)
client = VulcanHebe(keystore, account)


async def get_lesson_info(student_id, date_from=None, date_to=None, type_="dict"):
    await client.select_student()
    for student in await client.get_students():
        if student.pupil.id == student_id:
            client.student = student
            break
    dict_ans = {}
    list_ans = []
    async for Lesson in await client.data.get_lessons(
        date_from=date_from, date_to=date_to
    ):
        temp_dict = {}
        temp_dict["number"] = Lesson.time.position
        lesson = str(Lesson.time.position)
        temp_dict["lesson"] = Lesson.subject.name
        temp_dict["room"] = Lesson.room.code
        temp_dict["visible"] = Lesson.visible
        temp_dict["changes"] = Lesson.changes
        temp_dict["group"] = Lesson.group
        temp_dict["teacher"] = Lesson.teacher.name
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
    await client.select_student()
    for student in await client.get_students():
        if student.pupil.id == student_id:
            client.student = student
            break
    student_info = {}
    for student in await client.get_students():
        if student.pupil.id == student_id:
            student_info["first_name"] = student.pupil.first_name
            if student.pupil.second_name:
                student_info["second_name"] = student.pupil.second_name
            student_info["last_name"] = student.pupil.last_name
            student_info["full_name"] = student.full_name
            student_info["id"] = student.pupil.id
            student_info["class"] = ""  # student.class_.name
            student_info["school"] = student.school.name
    return student_info


async def get_latest_attendance(student_id):
    await client.select_student()
    for student in await client.get_students():
        if student.pupil.id == student_id:
            client.student = student
            break
    latest_attendance = {}

    async for attendance in await client.data.get_attendance():
        latest_attendance = {}
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
    await client.select_student()
    for student in await client.get_students():
        if student.pupil.id == student_id:
            client.student = student
            break
    latest_grade = {}

    async for grade in await client.data.get_grades():
        latest_grade = {}
        latest_grade["content"] = grade.content
        latest_grade["weight"] = grade.column.weight
        latest_grade["description"] = grade.column.name
        latest_grade["value"] = grade.value
        latest_grade["teacher"] = grade.teacher_created.display_name
        latest_grade["subject"] = grade.column.subject.name
        latest_grade["date"] = grade.date_created.date.strftime("%Y.%m.%d")

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
    await client.select_student()
    for student in await client.get_students():
        if student.pupil.id == student_id:
            client.student = student
            break
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
                next_homework["teacher"] = homework.creator.name
                next_homework["date"] = homework.deadline.date.strftime("%d.%m.%Y")
                if exam.content != None:
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
    await client.select_student()
    for student in await client.get_students():
        if student.pupil.id == student_id:
            client.student = student
            break
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
                next_exam["teacher"] = exam.creator.name
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
            "content": "-",
            "date": "-",
            "weight": "-",
            "description": "-",
            "subkect": "-",
            "teacher": "-",
            "value": 0,
        }

    return self.latest_message
