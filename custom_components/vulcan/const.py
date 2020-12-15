"""Constants for the Vulcan integration."""
from datetime import timedelta
import voluptuous as vol
import homeassistant.helpers.config_validation as cv


DOMAIN = "vulcan"
CONF_STUDENT_NAME = "student_name"
CONF_GROUPS = "groups"
CONF_NOTIFY = "notify"
CONF_ATTENDANCE_NOTIFY = "attendance_notify"
CONF_SCAN_INTERVAL = timedelta(minutes=1)

SEND_MESSAGE_SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("teacher"): cv.positive_int,
        vol.Required("title"): cv.string,
        vol.Optional("content"): cv.string,
    }
)
