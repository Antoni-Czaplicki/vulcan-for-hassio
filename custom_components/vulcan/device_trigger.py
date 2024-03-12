"""Provides device triggers for Uonet+ Vulcan."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN

TRIGGER_TYPES = {"new_message", "new_grade", "new_attendance", "new_homework"}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(hass, device_id):
    """Return a list of triggers."""

    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)

    triggers = []

    if device is None:
        return triggers
    if device.dict_repr["identifiers"][0][1].startswith("message"):
        triggers.append(
            {
                # Required fields of TRIGGER_BASE_SCHEMA
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: device_id,
                # Required fields of TRIGGER_SCHEMA
                CONF_TYPE: "new_message",
            }
        )
    elif device.dict_repr["identifiers"][0][1].startswith("grade"):
        triggers.append(
            {
                # Required fields of TRIGGER_BASE_SCHEMA
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: device_id,
                # Required fields of TRIGGER_SCHEMA
                CONF_TYPE: "new_grade",
            }
        )
    elif device.dict_repr["identifiers"][0][1].startswith("attendance"):
        triggers.append(
            {
                # Required fields of TRIGGER_BASE_SCHEMA
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: device_id,
                # Required fields of TRIGGER_SCHEMA
                CONF_TYPE: "new_attendance",
            }
        )
    elif device.dict_repr["identifiers"][0][1].startswith("homework"):
        triggers.append(
            {
                # Required fields of TRIGGER_BASE_SCHEMA
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: device_id,
                # Required fields of TRIGGER_SCHEMA
                CONF_TYPE: "new_homework",
            }
        )

    return triggers


async def async_attach_trigger(hass, config, action, trigger_info):
    """Attach a trigger."""
    event_config = event_trigger.TRIGGER_SCHEMA(
        {
            event_trigger.CONF_PLATFORM: "event",
            event_trigger.CONF_EVENT_TYPE: "vulcan_event",
            event_trigger.CONF_EVENT_DATA: {
                CONF_DEVICE_ID: config[CONF_DEVICE_ID],
                CONF_TYPE: config[CONF_TYPE],
            },
        }
    )
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )
