"""Constants for the Vulcan integration."""
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

DOMAIN = "vulcan"
CONF_NOTIFY = "notify"
CONF_ATTENDANCE_NOTIFY = "attendance_notify"
SCAN_INTERVAL = timedelta(minutes=10)
PARALLEL_UPDATES = 1

SEND_MESSAGE_SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("teacher"): cv.positive_int,
        vol.Required("title"): cv.string,
        vol.Optional("content"): cv.string,
    }
)
