"""Support for fetching Vulcan data."""
import datetime
from datetime import timedelta


async def get_lessons(client, date_from=None, date_to=None, type_="dict"):
    """Support for fetching Vulcan lessons."""
    dict_ans = {}
    changes = {}
    list_ans = []
    async for lesson in await client.data.get_changed_lessons(
        date_from=date_from, date_to=date_to
    ):
        temp_dict = {}
        _id = str(lesson.id)
        temp_dict["id"] = lesson.id
        temp_dict["number"] = lesson.time.position if lesson.time is not None else None
        temp_dict["lesson"] = (
            lesson.subject.name if lesson.subject is not None else None
        )
        temp_dict["room"] = lesson.room.code if lesson.room is not None else None
        temp_dict["changes"] = lesson.changes
        temp_dict["note"] = lesson.note
        temp_dict["reason"] = lesson.reason
        temp_dict["event"] = lesson.event
        temp_dict["group"] = lesson.group
        temp_dict["teacher"] = (
            lesson.teacher.display_name if lesson.teacher is not None else None
        )
        temp_dict["from_to"] = (
            lesson.time.displayed_time if lesson.time is not None else None
        )

        changes[str(_id)] = temp_dict

    async for lesson in await client.data.get_lessons(
        date_from=date_from, date_to=date_to
    ):
        temp_dict = {}
        temp_dict["id"] = lesson.id
        temp_dict["number"] = lesson.time.position
        temp_dict["time"] = lesson.time
        temp_dict["date"] = lesson.date.date
        temp_dict["lesson"] = (
            lesson.subject.name if lesson.subject is not None else None
        )
        if lesson.room is not None:
            temp_dict["room"] = lesson.room.code
        else:
            temp_dict["room"] = "-"
        temp_dict["visible"] = lesson.visible
        temp_dict["changes"] = lesson.changes
        temp_dict["group"] = lesson.group
        temp_dict["reason"] = None
        temp_dict["teacher"] = (
            lesson.teacher.display_name if lesson.teacher is not None else None
        )
        temp_dict["from_to"] = (
            lesson.time.displayed_time if lesson.time is not None else None
        )
        if temp_dict["changes"] is None:
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
        if temp_dict["visible"]:
            if type_ == "dict":
                dict_ans[f"lesson_{lesson.time.position}"] = temp_dict
            elif type_ == "list":
                list_ans.append(temp_dict)

    if type_ == "dict":
        for num in range(10):
            if not f"lesson_{str(num + 1)}" in dict_ans:
                dict_ans[f"lesson_{str(num + 1)}"] = {
                    "number": num + 1,
                    "lesson": "-",
                    "room": "-",
                    "date": date_from,
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


async def get_student_info(client, student_id):
    """Support for fetching Student info by student id."""
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
            student_info["class"] = student.class_
            student_info["school"] = student.school.name
    return student_info


async def get_lucky_number(client):
    lucky_number = {}
    number = await client.data.get_lucky_number()
    try:
        lucky_number["number"] = number.number
        lucky_number["date"] = number.date.strftime("%d.%m.%Y")
    except:
        lucky_number = {"number": "-", "date": "-"}
    return lucky_number


async def get_latest_attendance(client):
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


async def get_latest_grade(client):
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


async def get_next_homework(client):
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


async def get_next_exam(client):
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


async def get_latest_message(client):
    async for message in await client.data.get_messages():
        latest_message = {}
        latest_message["id"] = message.id
        latest_message["title"] = message.subject
        latest_message["content"] = message.content
        if message.sender is not None:
            latest_message["sender"] = message.sender.address_name
        else:
            latest_message["sender"] = "Nieznany"
        latest_message[
            "date"
        ] = f"{message.sent_date.time.strftime('%H:%M')} {message.sent_date.date.strftime('%d.%m.%Y')}"

    if latest_message == {}:
        latest_message = {
            "id": 0,
            "title": "-",
            "content": "-",
            "date": "-",
            "sender": "-",
        }

    return latest_message
