"""Constants for the Vulcan integration."""
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

DOMAIN = "vulcan"
CONF_MESSAGE_NOTIFY = "message_notify"
CONF_GRADE_NOTIFY = "grade_notify"
CONF_ATTENDANCE_NOTIFY = "attendance_notify"
SCAN_INTERVAL = timedelta(minutes=1)
DEFAULT_SCAN_INTERVAL = 5
PARALLEL_UPDATES = 1

SEND_MESSAGE_SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("teacher"): cv.positive_int,
        vol.Required("title"): cv.string,
        vol.Optional("content"): cv.string,
    }
)
