import json
from vulcan import Vulcan
import logging
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
       
        
DOMAIN = "vulcan"

def setup(hass, config):
    hass.states.set("vulcan.test", "Sing in successfully")

    # Return boolean to indicate that initialization was successful.
    return True

#class Lessons(device):
#    @property
#    def device_info(self) -> Dict[str, Any]:
#        return {
#            "identifiers": {
#                (DOMAIN, config_entry.symbol)
#            },
#            "name": "Lessons",
#            "manufacturer": "Uonet+",
#            "sw_version": "0.1.0",
#            "entry_type": "service",
#        }
