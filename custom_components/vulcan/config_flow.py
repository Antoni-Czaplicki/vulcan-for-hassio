import logging
import json
from vulcan import Vulcan
from datetime import timedelta
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_SCAN_INTERVAL
from . import DOMAIN, register
from homeassistant.components import persistent_notification

_LOGGER = logging.getLogger(__name__)
from .const import (
    CONF_NOTIFY,
    CONF_ATTENDANCE_NOTIFY,
    CONF_STUDENT_NAME,
)


def get_students_list():
    with open("vulcan.json") as f:
        certificate = json.load(f)
    client = Vulcan(certificate)
    students_list = {}
    for student in client.get_students():
        students_list[str(student.id)] = student.name
    return students_list


class vulcanFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VulcanOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """GUI > Configuration > Integrations > Plus > Uonet+ Vulcan for Home Assistant"""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        error = None

        if user_input is not None:
            error = register.reg(
                user_input["token"], user_input["symbol"], user_input["pin"]
            )
            if not error:
                return self.async_create_entry(
                    title=user_input["symbol"], data=user_input
                )
            CONF_SYMBOL = user_input["symbol"]

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("token"): str,
                    vol.Required("symbol"): str,
                    vol.Required("pin"): str,
                }
            ),
            description_placeholders={
                "error_text": "\nERROR: " + error if error else ""
            },
        )


class VulcanOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self._students = {}

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        self._students = get_students_list()

        options = {
            vol.Optional(
                CONF_STUDENT_NAME,
            ): vol.In(self._students),
            vol.Optional(
                CONF_NOTIFY, 
                default=self.config_entry.options.get(CONF_NOTIFY, False),
            ): bool,
            vol.Optional(
                CONF_ATTENDANCE_NOTIFY,
                default=self.config_entry.options.get(CONF_ATTENDANCE_NOTIFY, False),
            ): bool,
        }

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(options), errors=errors
        )
