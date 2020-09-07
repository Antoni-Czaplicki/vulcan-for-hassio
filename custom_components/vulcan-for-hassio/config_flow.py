import logging
import json
from vulcan import Vulcan
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class vulcanFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        """GUI > Configuration > Integrations > Plus > Uonet+ Vulcan for Home Assistant"""
        error = None
        
        vulcan = 'test'

        if user_input is not None:
            error = vulcan + user_input['token'] + user_input['symbol'] + str(user_input['pin'])
            if not error:
                return self.async_create_entry(title='vulcan',
                                               data=user_input['symbol'])

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required('token'): str,
                vol.Required('symbol'): str,
                vol.Required('pin'): int,
            }),
            description_placeholders={
                'error_text': "\nERROR: " + error if error else ''
            }
        )
