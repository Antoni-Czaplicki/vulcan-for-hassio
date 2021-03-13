"""Support for Vulcan Calendar Search binary sensors."""
import copy
from datetime import date, datetime, timedelta
import logging

from homeassistant.components.calendar import (
    ENTITY_ID_FORMAT,
    CalendarEventDevice,
    get_date,
)
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_ENTITIES,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
)
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.template import DATE_STR_FORMAT
from homeassistant.util import Throttle, dt

from . import DOMAIN
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=DEFAULT_SCAN_INTERVAL)

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
    """Set up the calendar platform for event devices."""
    global MIN_TIME_BETWEEN_UPDATES
    MIN_TIME_BETWEEN_UPDATES = (
        timedelta(minutes=config_entry.options.get(CONF_SCAN_INTERVAL))
        if config_entry.options.get(CONF_SCAN_INTERVAL) is not None
        else MIN_TIME_BETWEEN_UPDATES
    )
    student_info = await get_student_info(config_entry.data.get("student_id"))
    async_add_entities(
        [
            VulcanCalendarEventDevice(
                hass,
                student_info,
                generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"vulcan_calendar_{student_info['full_name']}",
                    hass=hass,
                ),
            )
        ],
    )


class VulcanCalendarEventDevice(CalendarEventDevice):
    """A calendar event device."""

    def __init__(self, hass, student_info, entity_id):
        """Create the Calendar event device."""
        self.student_info = student_info
        self.data = VulcanCalendarData(
            student_info,
        )
        self._event = None
        self.entity_id = entity_id
        self._unique_id = f"vulcan_calendar_{student_info['id']}"

        if hass.data[DOMAIN]["students_number"] == 1:
            name = ""
            self.device_name = "Calendar"
        else:
            name = f" - {student_info['full_name']}"
            self.device_name = f"{student_info['full_name']}: Calendar"
        self._name = f"Vulcan calendar{name}"

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"calendar_{self.student_info['id']}")},
            "manufacturer": "Uonet +",
            "model": f"{self.student_info['class']} {self.student_info['school']}",
            "name": self.device_name,
            "entry_type": "service",
        }

    @property
    def event(self):
        """Return the next upcoming event."""
        return self._event

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    async def async_get_events(self, hass, start_date, end_date):
        """Get all events in a specific time frame."""
        return await self.data.async_get_events(hass, start_date, end_date)

    async def async_update(self):
        """Update event data."""
        await self.data.async_update()
        event = copy.deepcopy(self.data.event)
        if event is None:
            self._event = event
            return
        event["start"] = {
            "dateTime": datetime.combine(event["date"], event["time"].from_)
            .astimezone(dt.DEFAULT_TIME_ZONE)
            .isoformat()
        }
        event["end"] = {
            "dateTime": datetime.combine(event["date"], event["time"].to)
            .astimezone(dt.DEFAULT_TIME_ZONE)
            .isoformat()
        }
        self._event = event


class VulcanCalendarData:
    """Class to utilize calendar service object to get next event."""

    def __init__(self, student_info):
        """Set up how we are going to search the Vulcan calendar."""
        self.student_info = student_info
        self.event = None

    async def async_get_events(self, hass, start_date, end_date):
        """Get all events in a specific time frame."""

        events = await get_lesson_info(
            student_id=self.student_info["id"],
            date_from=start_date,
            date_to=end_date,
            type_="list",
        )

        event_list = []
        for item in events:
            event = {
                "uid": item["id"],
                "start": {
                    "dateTime": datetime.combine(
                        item["date"], item["time"].from_
                    ).strftime(DATE_STR_FORMAT)
                },
                "end": {
                    "dateTime": datetime.combine(
                        item["date"], item["time"].to
                    ).strftime(DATE_STR_FORMAT)
                },
                "summary": item["lesson"],
                "location": item["room"],
                "description": item["teacher"],
            }

            event_list.append(event)

        return event_list

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Get the latest data."""

        events = await get_lesson_info(student_id=self.student_info["id"], type_="list")
        if events == []:
            events = await get_lesson_info(
                student_id=self.student_info["id"],
                date_to=date.today() + timedelta(days=7),
                type_="list",
            )
        new_event = None
        for item in events:
            item["start_date"] = datetime.combine(item["date"], item["time"].from_)
            new_event = item
            break
        self.event = {
            "uid": new_event["id"],
            "date": new_event["date"],
            "time": new_event["time"],
            "summary": new_event["lesson"],
            "location": new_event["room"],
            "description": new_event["teacher"],
        }
