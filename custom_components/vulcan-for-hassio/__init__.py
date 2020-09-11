import asyncio
from homeassistant import config_entries
import homeassistant
import voluptuous as vol
from homeassistant.helpers import config_validation as cv, entity_platform, service
from .const import (  # pylint: disable=unused-import
    CONF_STUDENT_NAME,
    CONF_GROUPS,
    DOMAIN,
)



CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_GROUPS): {
            cv.string: vol.Schema({
                vol.Optional('angielski'): cv.string,
            }, extra=vol.ALLOW_EXTRA),
        },
        vol.Optional(CONF_STUDENT_NAME, default=''): cv.string,
    }, extra=vol.ALLOW_EXTRA),
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config) -> bool:
    vulcan: Optional[ConfigType] = config.get(DOMAIN)
    hass.data.setdefault(DOMAIN, {})

    if not vulcan:
        return True
    
    hass.data[DOMAIN] = {
        'student_name': config[DOMAIN][CONF_STUDENT_NAME],
    }
    
    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
    return True

async def async_setup_entry(hass, entry):
    platform = entity_platform.current_platform.get()
    return True
