import datetime
from datetime import timedelta

from vulcan import Vulcan

from homeassistant.components import persistent_notification

from . import DOMAIN, VulcanEntity
from .const import CONF_ATTENDANCE_NOTIFY, CONF_NOTIFY, PARALLEL_UPDATES, SCAN_INTERVAL
from .get_data import (
    get_latest_attendance,
    get_latest_grade,
    get_latest_message,
    get_lesson_info,
    get_lucky_number,
    get_next_exam,
    get_next_homework,
    get_student_info,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    hass.data[DOMAIN][CONF_NOTIFY] = config_entry.options.get(CONF_NOTIFY)
    hass.data[DOMAIN][CONF_ATTENDANCE_NOTIFY] = config_entry.options.get(
        CONF_ATTENDANCE_NOTIFY
    )
    hass.data[DOMAIN]["student_info"] = await get_student_info(
        config_entry.data.get("student_id")
    )
    hass.data[DOMAIN]["students_number"] = config_entry.data.get("students_number")
    hass.data[DOMAIN]["lessons"] = await get_lesson_info(
        student_id=config_entry.data.get("student_id")
    )
    hass.data[DOMAIN]["lessons_t"] = await get_lesson_info(
        student_id=config_entry.data.get("student_id"),
        date_from=datetime.date.today() + timedelta(days=1),
    )
    hass.data[DOMAIN]["grade"] = await get_latest_grade(
        config_entry.data.get("student_id")
    )
    hass.data[DOMAIN]["lucky_number"] = await get_lucky_number()
    hass.data[DOMAIN]["attendance"] = await get_latest_attendance(
        config_entry.data.get("student_id")
    )
    hass.data[DOMAIN]["homework"] = await get_next_homework(
        config_entry.data.get("student_id")
    )
    hass.data[DOMAIN]["exam"] = await get_next_exam(config_entry.data.get("student_id"))
    async_add_entities([VulcanLessonEntity(hass, 1)])
    async_add_entities([VulcanLessonEntity(hass, 2)])
    async_add_entities([VulcanLessonEntity(hass, 3)])
    async_add_entities([VulcanLessonEntity(hass, 4)])
    async_add_entities([VulcanLessonEntity(hass, 5)])
    async_add_entities([VulcanLessonEntity(hass, 6)])
    async_add_entities([VulcanLessonEntity(hass, 7)])
    async_add_entities([VulcanLessonEntity(hass, 8)])
    async_add_entities([VulcanLessonEntity(hass, 9)])
    async_add_entities([VulcanLessonEntity(hass, 10)])
    async_add_entities([LatestGrade(hass)])
    # async_add_entities([LatestMessage(hass)])
    async_add_entities([LatestAttendance(hass)])
    async_add_entities([LuckyNumber(hass)])
    async_add_entities([NextHomework(hass)])
    async_add_entities([NextExam(hass)])
    async_add_entities([VulcanLessonEntity(hass, 1, True)])
    async_add_entities([VulcanLessonEntity(hass, 2, True)])
    async_add_entities([VulcanLessonEntity(hass, 3, True)])
    async_add_entities([VulcanLessonEntity(hass, 4, True)])
    async_add_entities([VulcanLessonEntity(hass, 5, True)])
    async_add_entities([VulcanLessonEntity(hass, 6, True)])
    async_add_entities([VulcanLessonEntity(hass, 7, True)])
    async_add_entities([VulcanLessonEntity(hass, 8, True)])
    async_add_entities([VulcanLessonEntity(hass, 9, True)])
    async_add_entities([VulcanLessonEntity(hass, 10, True)])


class VulcanLessonEntity(VulcanEntity):
    def __init__(self, hass, number, _tomorrow=False):
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = " - " + self.student_info["full_name"]
            self.device_student_name = self.student_info["full_name"] + ": "

        self.number = str(number)
        if _tomorrow == True:
            tomorrow = "_t"
            name_tomorrow = " (Tomorrow)"
            self.tomorrow_device_id = "tomorrow_"
            self.device_name_tomorrow = "Tomorrow "
            self.num_tomorrow = timedelta(days=1)
        else:
            tomorrow = ""
            name_tomorrow = " "
            self.tomorrow_device_id = ""
            self.device_name_tomorrow = ""
            self.num_tomorrow = timedelta(days=0)

        if number == 10:
            space = chr(160)
        else:
            space = " "

        self.lesson = hass.data[DOMAIN]["lessons" + tomorrow]["lesson_" + self.number]
        self._state = self.lesson["lesson"]

        self._name = "Lesson" + space + self.number + name_tomorrow + name
        self._unique_id = "lesson_" + tomorrow + self.number + "_" + self.student_id
        self._icon = "mdi:timetable"

    @property
    def device_state_attributes(self):
        lesson_info = self.lesson
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, self.tomorrow_device_id + "timetable_" + self.student_id)
            },
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": self.device_student_name + self.device_name_tomorrow + "Timetable",
            "entry_type": "service",
        }

    async def async_update(self):
        try:
            self.lesson_data = await get_lesson_info(
                student_id=self.student_id,
                date_from=datetime.date.today() + self.num_tomorrow,
            )
        except:
            self.lesson_data = await get_lesson_info(
                student_id=self.student_id,
                date_from=datetime.date.today() + self.num_tomorrow,
            )
        self.lesson = self.lesson_data["lesson_" + self.number]
        self._state = self.lesson["lesson"]


class LatestAttendance(VulcanEntity):
    def __init__(self, hass):
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = str(self.student_info["id"])
        self.latest_attendance = hass.data[DOMAIN]["attendance"]
        self.att_notify = hass.data[DOMAIN][CONF_ATTENDANCE_NOTIFY]
        self.old_att = self.latest_attendance["datetime"]
        self._state = self.latest_attendance["content"]

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = " - " + self.student_info["full_name"]
            self.device_student_name = self.student_info["full_name"] + ": "
        self._name = "Latest Attendance" + name
        self._unique_id = "attendance_latest_" + self.student_id
        self._icon = "mdi:account-check-outline"

    @property
    def device_state_attributes(self):
        att_info = self.latest_attendance
        atr = {
            "Lesson": att_info["lesson_name"],
            "Lesson number": att_info["lesson_number"],
            "Lesson date": att_info["lesson_date"],
            "Lesson time": att_info["lesson_time"],
        }

        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "attendance" + self.student_id)},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": self.device_student_name + "Attendance",
            "entry_type": "service",
        }

    async def async_update(self):
        self.latest_attendance = await get_latest_attendance(self.student_id)
        latest_attendance = self.latest_attendance
        if self.att_notify == True:
            if (
                self.latest_attendance["content"] != "obecność"
                and self.latest_attendance["content"] != "-"
                and self.old_att < self.latest_attendance["datetime"]
            ):
                persistent_notification.async_create(
                    self.hass,
                    self.latest_attendance["lesson_time"]
                    + ", "
                    + self.latest_attendance["lesson_date"]
                    + "\n"
                    + self.latest_attendance["content"],
                    "Vulcan: Nowy wpis frekwencji w "
                    + self.latest_attendance["lesson_name"],
                )
                self.old_att = self.latest_attendance["datetime"]
        self._state = latest_attendance["content"]


class LatestMessage(VulcanEntity):
    def __init__(self, hass):
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.latest_message = get_latest_message(self)
        self.notify = hass.data[DOMAIN][CONF_NOTIFY]
        self.old_msg = self.latest_message["content"]
        self._state = self.latest_message["title"]

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = " - " + self.student_info["full_name"]
            self.device_student_name = self.student_info["full_name"] + ": "
        self._name = "Latest Message" + name
        self._unique_id = "message_latest_" + self.student_id
        self._icon = "mdi:message-arrow-left-outline"

    @property
    def device_state_attributes(self):
        msg_info = self.latest_message
        atr = {
            "Sender": msg_info["sender"],
            "Date": msg_info["date"],
            "Content": msg_info["content"],
        }

        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "message" + self.student_id)},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": self.device_student_name + "Messages",
            "entry_type": "service",
        }

    def update(self):
        self.latest_message = get_latest_message(self)
        message_latest = self.latest_message
        if self.notify == True:
            if self.old_msg != self.latest_message["content"]:
                persistent_notification.async_create(
                    self.hass,
                    self.latest_message["sender"]
                    + ", "
                    + self.latest_message["date"]
                    + "\n"
                    + self.latest_message["content"],
                    "Vulcan: " + self.latest_message["title"],
                )
                self.old_msg = self.latest_message["content"]
        self._state = message_latest["title"]


class LatestGrade(VulcanEntity):
    def __init__(self, hass):
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.latest_grade = hass.data[DOMAIN]["grade"]
        self._state = self.latest_grade["content"]
        self.student_id = str(self.student_info["id"])

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = " - " + self.student_info["full_name"]
            self.device_student_name = self.student_info["full_name"] + ": "

        self._name = "Latest grade" + name
        self._unique_id = "grade_latest_" + self.student_id
        self._icon = "mdi:school-outline"

    @property
    def device_state_attributes(self):
        grade_info = self.latest_grade
        atr = {
            "subject": grade_info["subject"],
            "weight": grade_info["weight"],
            "teacher": grade_info["teacher"],
            "date": grade_info["date"],
            "description": grade_info["description"],
        }
        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "grade" + self.student_id)},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": self.device_student_name + "Grades",
            "entry_type": "service",
        }

    async def async_update(self):
        self.latest_grade = await get_latest_grade(self.student_id)
        self._state = self.latest_grade["content"]


class NextHomework(VulcanEntity):
    def __init__(self, hass):
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.next_homework = hass.data[DOMAIN]["homework"]
        self._state = self.next_homework["description"]

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = " - " + self.student_info["full_name"]
            self.device_student_name = self.student_info["full_name"] + ": "

        self._name = "Next Homework" + name
        self._unique_id = "homework_next_" + self.student_id
        self._icon = "mdi:pen"

    @property
    def device_state_attributes(self):
        atr = {
            "subject": self.next_homework["subject"],
            "teacher": self.next_homework["teacher"],
            "date": self.next_homework["date"],
        }
        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "homework" + self.student_id)},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": self.device_student_name + "Homeworks",
            "entry_type": "service",
        }

    async def async_update(self):
        self.next_homework = await get_next_homework(self.student_id)
        self._state = self.next_homework["description"]


class NextExam(VulcanEntity):
    def __init__(self, hass):
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.next_exam = hass.data[DOMAIN]["exam"]
        self._state = self.next_exam["description"]

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = " - " + self.student_info["full_name"]
            self.device_student_name = self.student_info["full_name"] + ": "

        self._name = "Next Exam" + name
        self._unique_id = "exam_next_" + self.student_id
        self._icon = "mdi:format-list-checks"

    @property
    def device_state_attributes(self):
        atr = {
            "subject": self.next_exam["subject"],
            "type": self.next_exam["type"],
            "teacher": self.next_exam["teacher"],
            "date": self.next_exam["date"],
        }
        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "exam" + self.student_id)},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": self.device_student_name + "Exam",
            "entry_type": "service",
        }

    async def async_update(self):
        self.next_exam = await get_next_exam(self.student_id)
        self._state = self.next_exam["description"]


class LuckyNumber(VulcanEntity):
    def __init__(self, hass):
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.lucky_number = hass.data[DOMAIN]["lucky_number"]
        self._state = self.lucky_number["number"]

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = " - " + self.student_info["full_name"]
            self.device_student_name = self.student_info["full_name"] + ": "

        self._name = "Lucky Number" + name
        self._unique_id = "lucky_number_" + self.student_id
        self._icon = "mdi:ticket-confirmation-outline"

    @property
    def device_state_attributes(self):
        atr = {
            "date": self.lucky_number["date"],
        }
        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "lucky_number" + self.student_id)},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": self.device_student_name + "Lucky Number",
            "entry_type": "service",
        }

    async def async_update(self):
        self.lucky_number = await get_lucky_number()
        self._state = self.lucky_number["number"]
