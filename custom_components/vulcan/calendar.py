"""Support for Vulcan Calendar platform."""

from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from aiohttp import ClientConnectorError
from homeassistant.components.calendar import (
    ENTITY_ID_FORMAT,
    CalendarEntity,
    CalendarEvent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from vulcan import UnauthorizedCertificateException

from . import DOMAIN
from .fetch_data import get_exams_list, get_homework_list, get_lessons, get_student_info

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform for entity."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    data = {
        "student_info": await get_student_info(
            client, config_entry.data.get("student_id")
        ),
        "students_number": hass.data[DOMAIN]["students_number"],
    }
    async_add_entities(
        [
            VulcanLessonsCalendarEntity(
                client,
                data,
                generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"vulcan_calendar_{data['student_info']['full_name']}",
                    hass=hass,
                ),
            ),
            VulcanExamsCalendarEntity(
                client,
                data,
                generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"vulcan_exams_calendar_{data['student_info']['full_name']}",
                    hass=hass,
                ),
            ),
            VulcanHomeworkCalendarEntity(
                client,
                data,
                generate_entity_id(
                    ENTITY_ID_FORMAT,
                    f"vulcan_homework_calendar_{data['student_info']['full_name']}",
                    hass=hass,
                ),
            ),
        ],
    )


class VulcanLessonsCalendarEntity(CalendarEntity):
    """A calendar entity."""

    _attr_has_entity_name = True
    _attr_translation_key = "calendar"

    def __init__(self, client, data, entity_id) -> None:
        """Create the Calendar entity."""
        self._event: CalendarEvent | None = None
        self.client = client
        self.entity_id = entity_id
        student_info = data["student_info"]
        if data["students_number"] == 1:
            self._attr_name = "Lessons"
            device_name = "Vulcan Calendar"
        else:
            self._attr_name = f"Lessons - {student_info['full_name']}"
            device_name = f"{student_info['full_name']}: Calendar"
        self._attr_unique_id = f"vulcan_calendar_{student_info['id']}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"calendar_{student_info['id']}")},
            entry_type=DeviceEntryType.SERVICE,
            name=device_name,
            model=(
                f"{student_info['full_name']} -"
                f" {student_info['class']} {student_info['school']}"
            ),
            manufacturer="Uonet +",
            configuration_url=(
                f"https://uonetplus.vulcan.net.pl/{student_info['symbol']}"
            ),
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        return self._event

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        try:
            events = await get_lessons(
                self.client,
                date_from=start_date,
                date_to=end_date,
                type_="list",
            )
        except UnauthorizedCertificateException as err:
            raise ConfigEntryAuthFailed(
                "The certificate is not authorized, please authorize integration again"
            ) from err
        except ClientConnectorError as err:
            if self.available:
                _LOGGER.warning(
                    "Connection error - please check your internet connection: %s", err
                )
            events = []

        event_list = []
        for item in events:
            try:
                event = CalendarEvent(
                    start=datetime.combine(item["date"], item["time"].from_).replace(
                        tzinfo=ZoneInfo("Europe/Warsaw")
                    ),
                    end=datetime.combine(item["date"], item["time"].to).replace(
                        tzinfo=ZoneInfo("Europe/Warsaw")
                    ),
                    summary=item["lesson"],
                    location=item["room"],
                    description=item["teacher"],
                )
            except Exception as err:
                _LOGGER.error("Error: %s", err)
                continue
            event_list.append(event)

        return event_list

    async def async_update(self) -> None:
        """Get the latest data."""

        try:
            events = await get_lessons(self.client, type_="list")

            if not self.available:
                _LOGGER.info("Restored connection with API")
                self._attr_available = True

            if events == []:
                events = await get_lessons(
                    self.client,
                    date_to=date.today() + timedelta(days=7),
                    type_="list",
                )
                if events == []:
                    self._event = None
                    return
        except UnauthorizedCertificateException as err:
            raise ConfigEntryAuthFailed(
                "The certificate is not authorized, please authorize integration again"
            ) from err
        except ClientConnectorError as err:
            if self.available:
                _LOGGER.warning(
                    "Connection error - please check your internet connection: %s", err
                )
                self._attr_available = False
            return

        new_event = min(
            events,
            key=lambda d: (
                datetime.combine(d["date"], d["time"].to) < datetime.now(),
                abs(datetime.combine(d["date"], d["time"].to) - datetime.now()),
            ),
        )
        self._event = CalendarEvent(
            start=datetime.combine(
                new_event["date"], new_event["time"].from_
            ).astimezone(ZoneInfo("Europe/Warsaw")),
            end=datetime.combine(new_event["date"], new_event["time"].to).astimezone(
                ZoneInfo("Europe/Warsaw")
            ),
            summary=new_event["lesson"],
            location=new_event["room"],
            description=new_event["teacher"],
        )


class VulcanExamsCalendarEntity(CalendarEntity):
    """A calendar entity."""

    _attr_has_entity_name = True
    _attr_translation_key = "calendar"

    def __init__(self, client, data, entity_id) -> None:
        """Create the Calendar entity."""
        self._event: CalendarEvent | None = None
        self.client = client
        self.entity_id = entity_id
        student_info = data["student_info"]
        if data["students_number"] == 1:
            self._attr_name = "Exams"
            device_name = "Vulcan Calendar"
        else:
            self._attr_name = f"Exams - {student_info['full_name']}"
            device_name = f"{student_info['full_name']}: Calendar"
        self._attr_unique_id = f"vulcan_exams_calendar_{student_info['id']}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"calendar_{student_info['id']}")},
            entry_type=DeviceEntryType.SERVICE,
            name=device_name,
            model=(
                f"{student_info['full_name']} -"
                f" {student_info['class']} {student_info['school']}"
            ),
            manufacturer="Uonet +",
            configuration_url=(
                f"https://uonetplus.vulcan.net.pl/{student_info['symbol']}"
            ),
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        return self._event

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        try:
            events = await get_exams_list(
                self.client,
                date_from=start_date,
                date_to=end_date,
            )
        except UnauthorizedCertificateException as err:
            raise ConfigEntryAuthFailed(
                "The certificate is not authorized, please authorize integration again"
            ) from err
        except ClientConnectorError as err:
            if self.available:
                _LOGGER.warning(
                    "Connection error - please check your internet connection: %s", err
                )
            events = []

        event_list = []
        for item in events:
            event = CalendarEvent(
                start=datetime.combine(
                    item["date"], item["time"].from_ if item["time"] else time(0, 0)
                ).replace(tzinfo=ZoneInfo("Europe/Warsaw")),
                end=datetime.combine(
                    item["date"], item["time"].to if item["time"] else time(0, 0)
                ).replace(tzinfo=ZoneInfo("Europe/Warsaw")),
                summary=f"{item['title']} - {item['subject']} ({item['type']})",
                description=f"{item['title']}\nPrzedmiot: {item['subject']}\nTyp: {item['type']}\nNauczyciel: {item['teacher']}",
            )

            event_list.append(event)

        return event_list

    async def async_update(self) -> None:
        """Get the latest data."""

        try:
            events = await get_exams_list(self.client)

            if not self.available:
                _LOGGER.info("Restored connection with API")
                self._attr_available = True

            if events == []:
                self._event = None
                return
        except UnauthorizedCertificateException as err:
            raise ConfigEntryAuthFailed(
                "The certificate is not authorized, please authorize integration again"
            ) from err
        except ClientConnectorError as err:
            if self.available:
                _LOGGER.warning(
                    "Connection error - please check your internet connection: %s", err
                )
                self._attr_available = False
            return

        new_event = min(
            events,
            key=lambda d: (
                datetime.combine(d["date"], d["time"].to if d["time"] else time(0, 0))
                < datetime.now(),
                abs(
                    datetime.combine(
                        d["date"], d["time"].to if d["time"] else time(0, 0)
                    )
                    - datetime.now()
                ),
            ),
        )
        self._event = CalendarEvent(
            start=datetime.combine(
                new_event["date"],
                new_event["time"].from_ if new_event["time"] else time(0, 0),
            ).replace(tzinfo=ZoneInfo("Europe/Warsaw")),
            end=datetime.combine(
                new_event["date"],
                new_event["time"].to if new_event["time"] else time(0, 0),
            ).replace(tzinfo=ZoneInfo("Europe/Warsaw")),
            summary=f"{new_event['title']} - {new_event['subject']} ({new_event['type']})",
            description=f"{new_event['title']}\nPrzedmiot: {new_event['subject']}\nTyp: {new_event['type']}\nNauczyciel: {new_event['teacher']}",
        )


class VulcanHomeworkCalendarEntity(CalendarEntity):
    """A calendar entity."""

    _attr_has_entity_name = True
    _attr_translation_key = "calendar"

    def __init__(self, client, data, entity_id) -> None:
        """Create the Calendar entity."""
        self._event: CalendarEvent | None = None
        self.client = client
        self.entity_id = entity_id
        student_info = data["student_info"]
        if data["students_number"] == 1:
            self._attr_name = "Homework"
            device_name = "Vulcan Calendar"
        else:
            self._attr_name = f"Homework - {student_info['full_name']}"
            device_name = f"{student_info['full_name']}: Calendar"
        self._attr_unique_id = f"vulcan_homework_calendar_{student_info['id']}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"calendar_{student_info['id']}")},
            entry_type=DeviceEntryType.SERVICE,
            name=device_name,
            model=(
                f"{student_info['full_name']} -"
                f" {student_info['class']} {student_info['school']}"
            ),
            manufacturer="Uonet +",
            configuration_url=(
                f"https://uonetplus.vulcan.net.pl/{student_info['symbol']}"
            ),
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        return self._event

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Get all events in a specific time frame."""
        try:
            events = await get_homework_list(
                self.client,
                date_from=start_date,
                date_to=end_date,
            )
        except UnauthorizedCertificateException as err:
            raise ConfigEntryAuthFailed(
                "The certificate is not authorized, please authorize integration again"
            ) from err
        except ClientConnectorError as err:
            if self.available:
                _LOGGER.warning(
                    "Connection error - please check your internet connection: %s", err
                )
            events = []

        event_list = []
        for item in events:
            event = CalendarEvent(
                start=datetime.combine(item["date"], time(0, 0)).replace(
                    tzinfo=ZoneInfo("Europe/Warsaw")
                ),
                end=datetime.combine(item["date"], time(0, 0)).replace(
                    tzinfo=ZoneInfo("Europe/Warsaw")
                ),
                summary=f"Zadanie domowe: {item['subject']}",
                description=item["description"],
            )

            event_list.append(event)

        return event_list

    async def async_update(self) -> None:
        """Get the latest data."""

        try:
            events = await get_homework_list(self.client)

            if not self.available:
                _LOGGER.info("Restored connection with API")
                self._attr_available = True

            if events == []:
                self._event = None
                return
        except UnauthorizedCertificateException as err:
            raise ConfigEntryAuthFailed(
                "The certificate is not authorized, please authorize integration again"
            ) from err
        except ClientConnectorError as err:
            if self.available:
                _LOGGER.warning(
                    "Connection error - please check your internet connection: %s", err
                )
                self._attr_available = False
            return

        new_event = min(
            events,
            key=lambda d: (
                datetime.combine(d["date"], time(0, 0)) < datetime.now(),
                abs(datetime.combine(d["date"], time(0, 0)) - datetime.now()),
            ),
        )
        self._event = CalendarEvent(
            start=datetime.combine(new_event["date"], time(0, 0)).replace(
                tzinfo=ZoneInfo("Europe/Warsaw")
            ),
            end=datetime.combine(new_event["date"], time(0, 0)).replace(
                tzinfo=ZoneInfo("Europe/Warsaw")
            ),
            summary=new_event["subject"],
            description=new_event["description"],
        )
