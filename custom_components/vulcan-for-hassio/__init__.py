#This Integration uses unofficial Vulcan-api https://github.com/kapi2289/vulcan-api
import asyncio
from homeassistant import config_entries
import homeassistant
import json
from vulcan import Vulcan
import voluptuous as vol
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import config_validation as cv, entity_platform, service
from .const import ( 
    CONF_STUDENT_NAME,
    CONF_GROUPS,
    DOMAIN,
)
with open('vulcan.json') as f:
    certificate = json.load(f)
client = Vulcan(certificate)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_GROUPS, default={}): {
            cv.positive_int: vol.Schema({
                vol.Optional('test'): cv.string,
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
    for student in client.get_students():
        if student.name == config[DOMAIN][CONF_STUDENT_NAME]:
            client.set_student(student)
            break

    hass.data[DOMAIN] = {
        'student_name': config[DOMAIN][CONF_STUDENT_NAME],
        'groups': config[DOMAIN][CONF_GROUPS],
    }
    
    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
    return True

async def async_setup_entry(hass, entry):
    platform = entity_platform.current_platform.get()
    return True
