import logging
import json
from vulcan import Vulcan
import voluptuous as vol
from homeassistant import config_entries
#from homeassistant.core import callback
from . import DOMAIN, register


_LOGGER = logging.getLogger(__name__)


class vulcanFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        """GUI > Configuration > Integrations > Plus > Uonet+ Vulcan for Home Assistant"""
        error = None

        if user_input is not None:
            error = register.reg(user_input['token'], user_input['symbol'], user_input['pin'])
            if not error: 
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
