import asyncio
from homeassistant import config_entries
import homeassistant
from homeassistant.helpers import config_validation as cv, entity_platform, service
 
DOMAIN = "vulcan"



def setup(hass, config):


    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True

async def async_setup_entry(hass, entry):
    """Set up the media player platform for Sonos."""

    platform = entity_platform.current_platform.get()
    return True
