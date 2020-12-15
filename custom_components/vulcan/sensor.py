from homeassistant.helpers.entity import Entity
import json
from vulcan import Vulcan
from homeassistant.core import ServiceCall
from homeassistant.components import persistent_notification
from datetime import datetime
from homeassistant import config_entries
from datetime import timedelta
from .get_data import (
    get_lesson_info,
    get_id,
    get_latest_grade,
    get_latest_message,
    get_latest_attendance,
    get_student_info,
)
from homeassistant.helpers import config_validation as cv, entity_platform, service
from .const import (
    CONF_STUDENT_NAME,
    CONF_NOTIFY,
    SEND_MESSAGE_SERVICE_SCHEMA,
)
from .__init__ import client
from . import DOMAIN

try:
    vulcan_error = False
    with open("vulcan.json") as f:
        certificate = json.load(f)
    client = Vulcan(certificate)
except:
    vulcan_error = True


async def async_setup_entry(hass, config_entry, async_add_entities):
    hass.data[DOMAIN]["student_id"] = get_id()
    hass.data[DOMAIN]["student_info"] = get_student_info(
        hass.data[DOMAIN]["student_name"]
    )
    async_add_entities([Lesson1(hass)])
    async_add_entities([Lesson2(hass)])
    async_add_entities([Lesson3(hass)])
    async_add_entities([Lesson4(hass)])
    async_add_entities([Lesson5(hass)])
    async_add_entities([Lesson6(hass)])
    async_add_entities([Lesson7(hass)])
    async_add_entities([Lesson8(hass)])
    async_add_entities([Lesson9(hass)])
    async_add_entities([Lesson10(hass)])
    async_add_entities([LatestGrade(hass)])
    async_add_entities([LatestMessage(hass)])
    async_add_entities([LatestAttendance(hass)])
    async_add_entities([Lesson_t_1(hass)])
    async_add_entities([Lesson_t_2(hass)])
    async_add_entities([Lesson_t_3(hass)])
    async_add_entities([Lesson_t_4(hass)])
    async_add_entities([Lesson_t_5(hass)])
    async_add_entities([Lesson_t_6(hass)])
    async_add_entities([Lesson_t_7(hass)])
    async_add_entities([Lesson_t_8(hass)])
    async_add_entities([Lesson_t_9(hass)])
    async_add_entities([Lesson_t_10(hass)])
    #vs = VulcanServices(hass)
    #hass.services.async_register(DOMAIN, "send_message", vs.send_message)


class VulcanServices:
    def __init__(self, hass):
        self._hass = hass
        x = 0

    def send_message(self, call):
        message_data = call.data
        SEND_MESSAGE_SERVICE_SCHEMA
        persistent_notification.async_create(
            self._hass,
            "Id: "
            + str(call.data.get("teacher"))
            + ", Title: "
            + call.data.get("title")
            + ", Content: "
            + call.data.get("content"),
            "Vulcan: testing",
        )
        return


class LatestAttendance(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.latest_attendance = get_latest_attendance(self)
        self.att_notify = hass.data[DOMAIN]["att_notify"]
        self.old_att = self.latest_attendance["datetime"]
        self._state = None

    @property
    def name(self):
        return "Latest Attendance"

    @property
    def icon(self):
        return "mdi:account-check-outline"

    @property
    def unique_id(self):
        id = self.student_id
        return "attendance_latest_" + id

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "attendance" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Attendance",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.latest_attendance = get_latest_attendance(self)
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


class LatestMessage(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.latest_message = get_latest_message(self)
        self.notify = hass.data[DOMAIN]["notify"]
        self.old_msg = self.latest_message["content"]
        self._state = None

    @property
    def name(self):
        return "Latest Message"

    @property
    def icon(self):
        return "mdi:message-arrow-left-outline"

    @property
    def unique_id(self):
        id = self.student_id
        return "message_latest_" + id

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
    def state(self):
        self._state = self.latest_message["title"]
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "message" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Messages",  #: ' + self.student_info["name"],
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


class LatestGrade(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.latest_grade = get_latest_grade(self)
        self._state = self.latest_grade["content"]

    @property
    def name(self):
        return "Latest Grade"

    @property
    def icon(self):
        return "mdi:school-outline"

    @property
    def unique_id(self):
        id = self.student_id
        return "grade_latest_" + id

    @property
    def device_state_attributes(self):
        grade_info = self.latest_grade
        atr = {
            "weight": grade_info["weight"],
            "teacher": grade_info["teacher"],
            "date": grade_info["date"],
            "description": grade_info["description"],
        }
        return atr

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "grade" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Grades",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.latest_grade = get_latest_grade(self)
        self._state = self.latest_grade["content"]


class Lesson1(Entity):
    def __init__(self, hass):
        hass.data[DOMAIN]["lessons"] = get_lesson_info(self)
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_1"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 1"

    @property
    def icon(self):
        return "mdi:timetable"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_1_" + id

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_1"]
        self._state = self.lesson["lesson"]


class Lesson2(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_2"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 2"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_2_" + id

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
    def icon(self):
        return "mdi:timetable"

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_2"]
        self._state = self.lesson["lesson"]


class Lesson3(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_3"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 3"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_3_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_3"]
        self._state = self.lesson["lesson"]


class Lesson4(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_4"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 4"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_4_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_4"]
        self._state = self.lesson["lesson"]


class Lesson5(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_5"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 5"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_5_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_5"]
        self._state = self.lesson["lesson"]


class Lesson6(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_6"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 6"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_6_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_6"]
        self._state = self.lesson["lesson"]


class Lesson7(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_7"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 7"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_7_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_7"]
        self._state = self.lesson["lesson"]


class Lesson8(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_8"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 8"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_8_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_8"]
        self._state = self.lesson["lesson"]


class Lesson9(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_9"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 9"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_9_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_9"]
        self._state = self.lesson["lesson"]


class Lesson10(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons"]["lesson_10"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson" + chr(160) + "10"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_10_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self)["lesson_10"]
        self._state = self.lesson["lesson"]


class Lesson_t_1(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        hass.data[DOMAIN]["lessons_t"] = get_lesson_info(self, 1)
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_1"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 1 (Tomorrow)"

    @property
    def icon(self):
        return "mdi:timetable"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_1_" + id

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_1"]
        self._state = self.lesson["lesson"]


class Lesson_t_2(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_2"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 2  (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_2_" + id

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
    def icon(self):
        return "mdi:timetable"

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_2"]
        self._state = self.lesson["lesson"]


class Lesson_t_3(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_3"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 3  (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_3_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_3"]
        self._state = self.lesson["lesson"]


class Lesson_t_4(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_4"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 4 (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_4_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_4"]
        self._state = self.lesson["lesson"]


class Lesson_t_5(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_5"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 5 (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_5_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_5"]
        self._state = self.lesson["lesson"]


class Lesson_t_6(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_6"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 6 (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_6_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_6"]
        self._state = self.lesson["lesson"]


class Lesson_t_7(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_7"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 7 (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_7_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_7"]
        self._state = self.lesson["lesson"]


class Lesson_t_8(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_8"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 8  (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_8_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_8"]
        self._state = self.lesson["lesson"]


class Lesson_t_9(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_9"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson 9 (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_9_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_9"]
        self._state = self.lesson["lesson"]


class Lesson_t_10(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_info = hass.data[DOMAIN]["student_info"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson = hass.data[DOMAIN]["lessons_t"]["lesson_10"]
        self._state = self.lesson["lesson"]

    @property
    def name(self):
        return "Lesson" + chr(160) + "10 (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_10_" + id

    @property
    def icon(self):
        return "mdi:timetable"

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
    def state(self):
        return self._state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "tomorrow_timetable_" + str(self.student_id))},
            "manufacturer": "Uonet +",
            "model": self.student_info["class"] + " " + self.student_info["school"],
            "name": "Vulcan Tomorrow Timetable",  #: ' + self.student_info["name"],
            "entry_type": "service",
        }

    def update(self):
        self.lesson = get_lesson_info(self, 1)["lesson_10"]
        self._state = self.lesson["lesson"]
