"""Support for fetching Vulcan data."""
import datetime
from datetime import timedelta

from . import client


async def get_lesson_info(student=None, date_from=None, date_to=None, type_="dict"):
    if student is not None:
        client.student = student
    dict_ans = {}
    changes = {}
    list_ans = []
    async for Lesson in await client.data.get_changed_lessons(
        date_from=date_from, date_to=date_to
    ):
        temp_dict = {}
        id = str(Lesson.id)
        temp_dict["id"] = Lesson.id
        temp_dict["number"] = Lesson.time.position if Lesson.time is not None else None
        temp_dict["lesson"] = (
            Lesson.subject.name if Lesson.subject is not None else None
        )
        temp_dict["room"] = Lesson.room.code if Lesson.room is not None else None
        temp_dict["changes"] = Lesson.changes
        temp_dict["note"] = Lesson.note
        temp_dict["reason"] = Lesson.reason
        temp_dict["event"] = Lesson.event
        temp_dict["group"] = Lesson.group
        temp_dict["teacher"] = (
            Lesson.teacher.display_name if Lesson.teacher is not None else None
        )
        temp_dict["from_to"] = (
            Lesson.time.displayed_time if Lesson.time is not None else None
        )

        changes[str(id)] = temp_dict

    async for Lesson in await client.data.get_lessons(
        date_from=date_from, date_to=date_to
    ):
        temp_dict = {}
        temp_dict["id"] = Lesson.id
        temp_dict["number"] = Lesson.time.position
        temp_dict["time"] = Lesson.time
        temp_dict["date"] = Lesson.date.date
        lesson = str(Lesson.time.position)
        temp_dict["lesson"] = (
            Lesson.subject.name if Lesson.subject is not None else None
        )
        if Lesson.room is not None:
            temp_dict["room"] = Lesson.room.code
        else:
            temp_dict["room"] = "-"
        temp_dict["visible"] = Lesson.visible
        temp_dict["changes"] = Lesson.changes
        temp_dict["group"] = Lesson.group
        temp_dict["reason"] = None
        temp_dict["teacher"] = (
            Lesson.teacher.display_name if Lesson.teacher is not None else None
        )
        temp_dict["from_to"] = (
            Lesson.time.displayed_time if Lesson.time is not None else None
        )
        if temp_dict["changes"] == None:
            temp_dict["changes"] = ""
        elif temp_dict["changes"].type == 1:
            temp_dict["lesson"] = f"Lekcja odwołana ({temp_dict['lesson']})"
            temp_dict["changes_info"] = f"Lekcja odwołana ({temp_dict['lesson']})"
            temp_dict["reason"] = changes[str(temp_dict["changes"].id)]["reason"]
        elif temp_dict["changes"].type == 2:
            temp_dict["lesson"] = f"{temp_dict['lesson']} (Zastępstwo)"
            temp_dict["teacher"] = changes[str(temp_dict["changes"].id)]["teacher"]
            temp_dict["reason"] = changes[str(temp_dict["changes"].id)]["reason"]
        # elif temp_dict["changes"].type == 3:
        # temp_dict["lesson"] = f"Lekcja przeniesiona ({temp_dict['lesson']})"
        # temp_dict["reason"] = changes[str(temp_dict["changes"].id)]["reason"]
        elif temp_dict["changes"].type == 4:
            temp_dict["lesson"] = f"Lekcja odwołana ({temp_dict['lesson']})"
            temp_dict["reason"] = changes[str(temp_dict["changes"].id)]["reason"]
        if temp_dict["visible"] == True:
            if type_ == "dict":
                dict_ans[f"lesson_{lesson}"] = temp_dict
            elif type_ == "list":
                list_ans.append(temp_dict)

    if type_ == "dict":
        for num in range(10):
            if not f"lesson_{str(num + 1)}" in dict_ans:
                dict_ans[f"lesson_{str(num + 1)}"] = {
                    "number": num + 1,
                    "lesson": "-",
                    "room": "-",
                    "group": "-",
                    "teacher": "-",
                    "from_to": "-",
                    "changes": "-",
                    "reason": None,
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
            student_info[
                "full_name"
            ] = f"{student.pupil.first_name} {student.pupil.last_name}"
            student_info["id"] = student.pupil.id
            student_info["class"] = ""  # student.class_.name
            student_info["school"] = student.school.name
    return student_info


async def get_student_by_id(student_id):
    student_obj = None
    for student in await client.get_students():
        if student.pupil.id == student_id:
            student_obj = student
            break
    return student_obj


async def get_lucky_number(student=None):
    if student is not None:
        client.student = student
    lucky_number = {}
    number = await client.data.get_lucky_number()
    try:
        lucky_number["number"] = number.number
        lucky_number["date"] = number.date.strftime("%d.%m.%Y")
    except:
        lucky_number = {"number": "-", "date": "-"}
    return lucky_number


async def get_latest_attendance(student=None):
    if student is not None:
        client.student = student
    latest_attendance = {}
    async for attendance in await client.data.get_attendance():
        if attendance.presence_type != None:
            latest_attendance["content"] = attendance.presence_type.name
            latest_attendance["lesson_name"] = attendance.subject.name
            latest_attendance["lesson_number"] = attendance.time.position
            latest_attendance["lesson_date"] = str(attendance.date.date)
            latest_attendance[
                "lesson_time"
            ] = f"{attendance.time.from_.strftime('%H:%M')}-{attendance.time.to.strftime('%H:%M')}"
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


async def get_latest_grade(student=None):
    if student is not None:
        client.student = student
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


async def get_next_homework(student=None):
    if student is not None:
        client.student = student
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


async def get_next_exam(student=None):
    if student is not None:
        client.student = student
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
                    next_exam["description"] = f"{exam.type} {exam.subject.name}"
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


def get_latest_message(student=None):
    if student is not None:
        client.student = student
    for message in client.data.get_messages():
        latest_message = {}
        latest_message["title"] = message.title
        latest_message["content"] = message.content
        if message.sender is not None:
            latest_message["sender"] = message.sender.name
        else:
            latest_message["sender"] = "Nieznany"
        latest_message[
            "date"
        ] = f"{message.sent_date.strftime('%Y.%m.%d')} {message.sent_time.strftime('%H:%M')}"

    if latest_message == {}:
        latest_message = {
            "title": "-",
            "content": "-",
            "date": "-",
            "sender": "-",
        }

    return latest_message
