import logging
import json
from vulcan import Vulcan
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from . import DOMAIN, register

_LOGGER = logging.getLogger(__name__)


class vulcanFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        """GUI > Configuration > Integrations > Plus > Uonet+ Vulcan for Home Assistant"""
        error = None

        if user_input is not None:
            return self.async_create_entry(title=user_input['symbol'],
                                           data=user_input)
            register.reg(user_input['token'], user_input['symbol'], user_input['pin'])
        

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
