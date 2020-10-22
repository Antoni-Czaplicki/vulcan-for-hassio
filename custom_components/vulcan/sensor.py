from homeassistant.helpers.entity import Entity
import json
from vulcan import Vulcan
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
)
from homeassistant.helpers import config_validation as cv, entity_platform, service
from .const import (
    CONF_STUDENT_NAME,
    CONF_NOTIFY,
)
from .__init__ import client
from . import DOMAIN


def setup_platform(hass, config, add_entities, discovery_info=None):
    if discovery_info is None:
        return
    hass.data[DOMAIN]["student_id"] = get_id()
    add_entities([Lesson1(hass)])
    add_entities([Lesson2(hass)])
    add_entities([Lesson3(hass)])
    add_entities([Lesson4(hass)])
    add_entities([Lesson5(hass)])
    add_entities([Lesson6(hass)])
    add_entities([Lesson7(hass)])
    add_entities([Lesson8(hass)])
    add_entities([Lesson9(hass)])
    add_entities([Lesson10(hass)])
    add_entities([LatestGrade(hass)])
    add_entities([LatestMessage(hass)])
    add_entities([LatestAttendance(hass)])
    add_entities([Lesson_t_1(hass)])
    add_entities([Lesson_t_2(hass)])
    add_entities([Lesson_t_3(hass)])
    add_entities([Lesson_t_4(hass)])
    add_entities([Lesson_t_5(hass)])
    add_entities([Lesson_t_6(hass)])
    add_entities([Lesson_t_7(hass)])
    add_entities([Lesson_t_8(hass)])
    add_entities([Lesson_t_9(hass)])
    add_entities([Lesson_t_10(hass)])


class LatestAttendance(Entity):
    def __init__(self, hass):
        self.student_name = hass.data[DOMAIN]["student_name"]
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
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.latest_attendance = get_latest_attendance(self)
        latest_attendance = self.latest_attendance
        if self.att_notify == True:
            if (
                self.latest_attendance["content"] != "obecność"
                self.latest_attendance["content"] != "-"
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
        """Return the state of the sensor."""
        return self._state

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
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]
        self.student_id = hass.data[DOMAIN]["student_id"]
        self.latest_grade = get_latest_grade(self)
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.latest_grade = get_latest_grade(self)
        grade_latest = self.latest_grade

        self._state = grade_latest["content"]


class Lesson1(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        hass.data[DOMAIN]["lessons"] = get_lesson_info(self)
        self.student_id = hass.data[DOMAIN]["student_id"]
        self._state = None
        self.lesson_1 = hass.data[DOMAIN]["lessons"]["lesson_1"]

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_1
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_1 = get_lesson_info(self)["lesson_1"]
        self._state = self.lesson_1["lesson"]


class Lesson2(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_2 = hass.data[DOMAIN]["lessons"]["lesson_2"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Lesson 2"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_2_" + id

    @property
    def device_state_attributes(self):
        lesson_info = self.lesson_2
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
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_2 = get_lesson_info(self)["lesson_2"]
        self._state = self.lesson_2["lesson"]


class Lesson3(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_3 = hass.data[DOMAIN]["lessons"]["lesson_3"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_3
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_3 = get_lesson_info(self)["lesson_3"]
        self._state = self.lesson_3["lesson"]


class Lesson4(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_4 = hass.data[DOMAIN]["lessons"]["lesson_4"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_4
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_4 = get_lesson_info(self)["lesson_4"]
        self._state = self.lesson_4["lesson"]


class Lesson5(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_5 = hass.data[DOMAIN]["lessons"]["lesson_5"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_5
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_5 = get_lesson_info(self)["lesson_5"]
        self._state = self.lesson_5["lesson"]


class Lesson6(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_6 = hass.data[DOMAIN]["lessons"]["lesson_6"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_6
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_6 = get_lesson_info(self)["lesson_6"]
        self._state = self.lesson_6["lesson"]


class Lesson7(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_7 = hass.data[DOMAIN]["lessons"]["lesson_7"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_7
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_7 = get_lesson_info(self)["lesson_7"]
        self._state = self.lesson_7["lesson"]


class Lesson8(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_8 = hass.data[DOMAIN]["lessons"]["lesson_8"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_8
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_8 = get_lesson_info(self)["lesson_8"]
        self._state = self.lesson_8["lesson"]


class Lesson9(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_9 = hass.data[DOMAIN]["lessons"]["lesson_9"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_9
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_9 = get_lesson_info(self)["lesson_9"]
        self._state = self.lesson_9["lesson"]


class Lesson10(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_10 = hass.data[DOMAIN]["lessons"]["lesson_10"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Lesson 10"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_10_" + id

    @property
    def icon(self):
        return "mdi:timetable"

    @property
    def device_state_attributes(self):
        lesson_info = self.lesson_10
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_10 = get_lesson_info(self)["lesson_10"]
        self._state = self.lesson_10["lesson"]


class Lesson_t_1(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        hass.data[DOMAIN]["lessons_t"] = get_lesson_info(self, 1)
        self.lesson_t_1 = hass.data[DOMAIN]["lessons_t"]["lesson_1"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_1
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_1 = get_lesson_info(self, 1)["lesson_1"]
        self._state = self.lesson_t_1["lesson"]


class Lesson_t_2(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_2 = hass.data[DOMAIN]["lessons_t"]["lesson_2"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Lesson 2  (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_2_" + id

    @property
    def device_state_attributes(self):
        lesson_info = self.lesson_t_2
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
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_2 = get_lesson_info(self, 1)["lesson_2"]
        self._state = self.lesson_t_2["lesson"]


class Lesson_t_3(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_3 = hass.data[DOMAIN]["lessons_t"]["lesson_3"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_3
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_3 = get_lesson_info(self, 1)["lesson_3"]
        self._state = self.lesson_t_3["lesson"]


class Lesson_t_4(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_4 = hass.data[DOMAIN]["lessons_t"]["lesson_4"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_4
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_4 = get_lesson_info(self, 1)["lesson_4"]
        self._state = self.lesson_t_4["lesson"]


class Lesson_t_5(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_5 = hass.data[DOMAIN]["lessons_t"]["lesson_5"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_5
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_5 = get_lesson_info(self, 1)["lesson_5"]
        self._state = self.lesson_t_5["lesson"]


class Lesson_t_6(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_6 = hass.data[DOMAIN]["lessons_t"]["lesson_6"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_6
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_6 = get_lesson_info(self, 1)["lesson_6"]
        self._state = self.lesson_t_6["lesson"]


class Lesson_t_7(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_7 = hass.data[DOMAIN]["lessons_t"]["lesson_7"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_7
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_7 = get_lesson_info(self, 1)["lesson_7"]
        self._state = self.lesson_t_7["lesson"]


class Lesson_t_8(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_8 = hass.data[DOMAIN]["lessons_t"]["lesson_8"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_8
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_8 = get_lesson_info(self, 1)["lesson_8"]
        self._state = self.lesson_t_8["lesson"]


class Lesson_t_9(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_9 = hass.data[DOMAIN]["lessons_t"]["lesson_9"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
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
        lesson_info = self.lesson_t_9
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_9 = get_lesson_info(self, 1)["lesson_9"]
        self._state = self.lesson_t_9["lesson"]


class Lesson_t_10(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass):
        """Initialize the sensor."""
        self.student_name = hass.data[DOMAIN]["student_name"]

        self.student_id = hass.data[DOMAIN]["student_id"]
        self.lesson_t_10 = hass.data[DOMAIN]["lessons_t"]["lesson_10"]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Lesson 10 (Tomorrow)"

    @property
    def unique_id(self):
        id = self.student_id
        return "lesson_t_10_" + id

    @property
    def icon(self):
        return "mdi:timetable"

    @property
    def device_state_attributes(self):
        lesson_info = self.lesson_t_10
        atr = {
            "room": lesson_info["room"],
            "teacher": lesson_info["teacher"],
            "time": lesson_info["time"],
            "changes": lesson_info["changes"],
        }
        return atr

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        self.lesson_t_10 = get_lesson_info(self, 1)["lesson_10"]
        self._state = self.lesson_t_10["lesson"]
