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
    CONF_STUDENT_NAME,
)

def get_students_list():
    with open('vulcan.json') as f:
        certificate = json.load(f)
    client = Vulcan(certificate)
    students_list = {'0': '* Default'}
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
        error = None

        if user_input is not None:
            error = register.reg(user_input['token'], user_input['symbol'], user_input['pin'])
            if not error: 
                persistent_notification.async_create(self.hass, 'Integration has been installed, to complete the configuration add the "vulcan" key in the configuration.yaml file. Optionally, you can also set up groups there and select a student.',
                                                 "Uonet+ Vulcan")
                return self.async_create_entry(title=user_input['symbol'],
                                           data=user_input)
            CONF_SYMBOL = user_input['symbol']

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required('token'): str,
                vol.Required('symbol'): str,
                vol.Required('pin'): str,
            }),
            description_placeholders={
                'error_text': "\nERROR: " + error if error else ''
            }
        )
    

class VulcanOptionsFlowHandler(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self._servers = {}

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
#            server_name = user_input[CONF_STUDENT_NAME]
            return self.async_create_entry(title="", data=user_input)

        self._servers = get_students_list()

 
        options = {
            vol.Optional(
                CONF_STUDENT_NAME,
                default=self.config_entry.options.get(CONF_STUDENT_NAME, self._servers['0']),
            ): vol.In(self._servers),
            vol.Optional(
                CONF_NOTIFY, default=self.config_entry.options.get(CONF_NOTIFY, False)
            ): bool,
        }

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(options), errors=errors
        )
