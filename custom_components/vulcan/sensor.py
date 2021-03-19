"""Support for Vulcan sensors."""
import datetime
from datetime import timedelta

from homeassistant.components import persistent_notification
from homeassistant.const import CONF_SCAN_INTERVAL

from . import DOMAIN, VulcanEntity
from .const import (
    CONF_ATTENDANCE_NOTIFY,
    CONF_GRADE_NOTIFY,
    CONF_MESSAGE_NOTIFY,
    DEFAULT_SCAN_INTERVAL,
    PARALLEL_UPDATES,
)
from .fetch_data import (
    get_latest_attendance,
    get_latest_grade,
    get_latest_message,
    get_lesson_info,
    get_lucky_number,
    get_next_exam,
    get_next_homework,
    get_student_info,
)

SCAN_INTERVAL = timedelta(minutes=DEFAULT_SCAN_INTERVAL)


async def async_setup_entry(hass, config_entry, async_add_entities):
    global SCAN_INTERVAL
    SCAN_INTERVAL = (
        timedelta(minutes=config_entry.options.get(CONF_SCAN_INTERVAL))
        if config_entry.options.get(CONF_SCAN_INTERVAL) is not None
        else SCAN_INTERVAL
    )
    client = hass.data[DOMAIN][config_entry.entry_id]
    data = {
        "student_info": await get_student_info(
            client, config_entry.data.get("student_id")
        ),
        "students_number": hass.data[DOMAIN]["students_number"],
        "lessons": await get_lesson_info(client),
        "lessons_t": await get_lesson_info(
            client, date_from=datetime.date.today() + timedelta(days=1)
        ),
        "grade": await get_latest_grade(client),
        "lucky_number": await get_lucky_number(client),
        "attendance": await get_latest_attendance(client),
        "homework": await get_next_homework(client),
        "exam": await get_next_exam(client),
        "notify": {
            CONF_MESSAGE_NOTIFY: config_entry.options.get(CONF_MESSAGE_NOTIFY),
            CONF_GRADE_NOTIFY: config_entry.options.get(CONF_GRADE_NOTIFY),
            CONF_ATTENDANCE_NOTIFY: config_entry.options.get(CONF_ATTENDANCE_NOTIFY),
        },
    }
    entities = [
        LatestGrade(client, data),
        LuckyNumber(client, data),
        LatestAttendance(client, data),
        NextHomework(client, data),
        NextExam(client, data),
    ]
    for i in range(10):
        entities.append(VulcanLessonEntity(client, data, i + 1))
    for i in range(10):
        entities.append(VulcanLessonEntity(client, data, i + 1, True))

    async_add_entities(entities)


class VulcanLessonEntity(VulcanEntity):
    def __init__(self, client, data, number, _tomorrow=False):
        self.client = client
        self.student_info = data["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])

        if data["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = f" - {self.student_info['full_name']}"
            self.device_student_name = f"{self.student_info['full_name']}: "

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

        self.lesson = data[f"lessons{tomorrow}"][f"lesson_{self.number}"]
        self._state = self.lesson["lesson"]

        self._name = f"Lesson{space}{self.number}{name_tomorrow}{name}"
        self._unique_id = f"lesson_{tomorrow}{self.number}_{self.student_id}"
        self._icon = "mdi:timetable"

    @property
    def device_state_attributes(self):
        lesson_info = self.lesson
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["from_to"],
            # "changes": lesson_info["changes"],
            "reason": lesson_info["reason"],
        }
        return atr

    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, f"{self.tomorrow_device_id}timetable_{self.student_id}")
            },
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": f"{self.device_student_name}{self.device_name_tomorrow}Timetable",
            "entry_type": "service",
        }

    async def async_update(self):
        try:
            self.lesson_data = await get_lesson_info(
                self.client,
                date_from=datetime.date.today() + self.num_tomorrow,
            )
        except:
            self.lesson_data = await get_lesson_info(
                self.client,
                date_from=datetime.date.today() + self.num_tomorrow,
            )
        self.lesson = self.lesson_data[f"lesson_{self.number}"]
        self._state = self.lesson["lesson"]


class LatestAttendance(VulcanEntity):
    def __init__(self, client, data):
        self.client = client
        self.student_info = data["student_info"]
        self.student_id = str(self.student_info["id"])
        self.latest_attendance = data["attendance"]
        self.notify = data["notify"][CONF_ATTENDANCE_NOTIFY]
        self.old_att = self.latest_attendance["datetime"]
        self._state = self.latest_attendance["content"]

        if data["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = f" - {self.student_info['full_name']}"
            self.device_student_name = f"{self.student_info['full_name']}: "
        self._name = f"Latest Attendance{name}"
        self._unique_id = f"attendance_latest_{self.student_id}"
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
            "identifiers": {(DOMAIN, f"attendance{self.student_id}")},
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": f"{self.device_student_name}Attendance",
            "entry_type": "service",
        }

    async def async_update(self):
        try:
            self.latest_attendance = await get_latest_attendance(self.client)
        except:
            self.latest_attendance = await get_latest_attendance(self.client)
        latest_attendance = self.latest_attendance
        if self.notify == True:
            if (
                self.latest_attendance["content"] != "obecność"
                and self.latest_attendance["content"] != "-"
                and self.old_att < self.latest_attendance["datetime"]
            ):
                persistent_notification.async_create(
                    self.hass,
                    f"{self.latest_attendance['lesson_time']}, {self.latest_attendance['lesson_date']}\n{self.latest_attendance['content']}",
                    f"{self.device_student_name}Vulcan: Nowy wpis frekwencji na lekcji {self.latest_attendance['lesson_name']}",
                )
                self.old_att = self.latest_attendance["datetime"]
        self._state = latest_attendance["content"]


class LatestMessage(VulcanEntity):
    def __init__(self, client, data):
        self.client = client
        self.student_info = data["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.latest_message = get_latest_message()
        self.notify = data["notify"][CONF_MESSAGE_NOTIFY]
        self.old_msg = self.latest_message["content"]
        self._state = self.latest_message["title"][0:250]

        if data["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = f" - {self.student_info['full_name']}"
            self.device_student_name = f"{self.student_info['full_name']}: "
        self._name = f"Latest Message{name}"
        self._unique_id = f"message_latest_{self.student_id}"
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
            "identifiers": {(DOMAIN, f"message{self.student_id}")},
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": f"{self.device_student_name}Messages",
            "entry_type": "service",
        }

    def update(self):
        try:
            self.latest_message = get_latest_message(self.client)
        except:
            self.latest_message = get_latest_message(self.client)
        message_latest = self.latest_message
        if self.notify == True:
            if self.old_msg != self.latest_message["content"]:
                persistent_notification.async_create(
                    self.hass,
                    f"{self.latest_message['sender']}, {self.latest_message['date']}\n{self.latest_message['content']}",
                    f"Vulcan: {self.latest_message['title']}",
                )
                self.old_msg = self.latest_message["content"]
        self._state = message_latest["title"][0:250]


class LatestGrade(VulcanEntity):
    def __init__(self, client, data):
        self.client = client
        self.student_info = data["student_info"]
        self.latest_grade = data["grade"]
        self._state = self.latest_grade["content"]
        self.student_id = str(self.student_info["id"])
        self.notify = data["notify"][CONF_GRADE_NOTIFY]
        self.old_state = f"{self.latest_grade['content']}_{self.latest_grade['subject']}_{self.latest_grade['date']}_{self.latest_grade['description']}"

        if data["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = f" - {self.student_info['full_name']}"
            self.device_student_name = f"{self.student_info['full_name']}: "

        self._name = f"Latest grade{name}"
        self._unique_id = f"grade_latest_{self.student_id}"
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
            "identifiers": {(DOMAIN, f"grade{self.student_id}")},
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": f"{self.device_student_name}Grades",
            "entry_type": "service",
        }

    async def async_update(self):
        try:
            self.latest_grade = await get_latest_grade(self.client)
        except:
            self.latest_grade = await get_latest_grade(self.client)
        if self.notify == True:
            if (
                self.latest_grade["content"] != "-"
                and self.old_state
                != f"{self.latest_grade['content']}_{self.latest_grade['subject']}_{self.latest_grade['date']}_{self.latest_grade['description']}"
            ):
                persistent_notification.async_create(
                    self.hass,
                    f"Nowa ocena {self.latest_grade['content']} z {self.latest_grade['subject']} została wystawiona {self.latest_grade['date']} przez {self.latest_grade['teacher']}.",
                    f"{self.device_student_name}Vulcan: Nowa ocena z {self.latest_grade['subject']}: {self.latest_grade['content']}",
                )
                self.old_state = f"{self.latest_grade['content']}_{self.latest_grade['subject']}_{self.latest_grade['date']}_{self.latest_grade['description']}"
        self._state = self.latest_grade["content"]


class NextHomework(VulcanEntity):
    def __init__(self, client, data):
        self.client = client
        self.student_info = data["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.next_homework = data["homework"]
        self._state = self.next_homework["description"][0:250]

        if data["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = f" - {self.student_info['full_name']}"
            self.device_student_name = f"{self.student_info['full_name']}: "

        self._name = f"Next Homework{name}"
        self._unique_id = f"homework_next_{self.student_id}"
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
            "identifiers": {(DOMAIN, f"homework{self.student_id}")},
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": f"{self.device_student_name}Homeworks",
            "entry_type": "service",
        }

    async def async_update(self):
        try:
            self.next_homework = await get_next_homework(self.client)
        except:
            self.next_homework = await get_next_homework(self.client)
        self._state = self.next_homework["description"][0:250]


class NextExam(VulcanEntity):
    def __init__(self, client, data):
        self.client = client
        self.student_info = data["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.next_exam = data["exam"]
        self._state = self.next_exam["description"][0:250]

        if data["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = f" - {self.student_info['full_name']}"
            self.device_student_name = f"{self.student_info['full_name']}: "

        self._name = f"Next Exam{name}"
        self._unique_id = f"exam_next_{self.student_id}"
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
            "identifiers": {(DOMAIN, f"exam{self.student_id}")},
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": f"{self.device_student_name}Exam",
            "entry_type": "service",
        }

    async def async_update(self):
        try:
            self.next_exam = await get_next_exam(self.client)
        except:
            self.next_exam = await get_next_exam(self.client)
        self._state = self.next_exam["description"][0:250]


class LuckyNumber(VulcanEntity):
    def __init__(self, client, data):
        self.client = client
        self.student_info = data["student_info"]
        self.student_name = self.student_info["full_name"]
        self.student_id = str(self.student_info["id"])
        self.lucky_number = data["lucky_number"]
        self._state = self.lucky_number["number"]

        if data["students_number"] == 1:
            name = ""
            self.device_student_name = ""
        else:
            name = f" - {self.student_info['full_name']}"
            self.device_student_name = f"{self.student_info['full_name']}: "

        self._name = f"Lucky Number{name}"
        self._unique_id = f"lucky_number_{self.student_id}"
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
            "identifiers": {(DOMAIN, f"lucky_number{self.student_id}")},
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": f"{self.device_student_name}Lucky Number",
            "entry_type": "service",
        }

    async def async_update(self):
        try:
            self.lucky_number = await get_lucky_number(self.client)
        except:
            self.lucky_number = await get_lucky_number(self.client)
        self._state = self.lucky_number["number"]
