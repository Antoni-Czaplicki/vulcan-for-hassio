import asyncio
from homeassistant import config_entries
import homeassistant
from homeassistant.helpers import config_validation as cv, entity_platform, service
 
DOMAIN = "vulcan"

#def setup_platform(hass, config, add_devices, discovery_info=None):
#    """Set up the sensor platform."""
#    add_entities([ExampleSensor()])

def setup(hass, config):
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms
    hass.data[DOMAIN] = {
        'temperature': 23
    }

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True

async def async_setup_entry(hass, entry):
    """Set up the media player platform for Sonos."""

    platform = entity_platform.current_platform.get()

    # This will call Entity.set_sleep_timer(sleep_time=VALUE)
#    platform.async_register_entity_service(
#        SERVICE_UPDATE_DATA,
#        {
#            vol.Required('update_data'): str,
#        },
#        "update_data",
#    )

#self.hass.async_add_job(hass.config_entries.async_forward_entry_setup(
#    self.config_entry, 'sensor'))
