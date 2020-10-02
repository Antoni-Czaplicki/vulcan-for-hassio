#This Integration uses unofficial Vulcan-api https://github.com/kapi2289/vulcan-api
import asyncio
from homeassistant import config_entries
import homeassistant
from homeassistant.components import persistent_notification
import json
from vulcan import Vulcan
import voluptuous as vol
import os
import logging
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import config_validation as cv, entity_platform, service
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import ( 
    CONF_STUDENT_NAME,
    CONF_GROUPS,
    DOMAIN,
    CONF_NOTIFY,
)

def get_students_list():
    with open('vulcan.json') as f:
        certificate = json.load(f)
    client = Vulcan(certificate)
    students_list = {'0': '* Default'}
    for student in client.get_students():
        students_list[str(student.id)] = student.name
    return students_list

_LOGGER = logging.getLogger(__name__)
autherror=False
try:
    if os.stat("vulcan.json").st_size == 0:
        autherror=True
    else:
        with open('vulcan.json') as f:
            certificate = json.load(f)
        client = Vulcan(certificate)
except FileNotFoundError:
    autherror=True

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
    
    if autherror == True:
        persistent_notification.async_create(hass, 'Coudl not import certificate, try to reconfigure integration', "Vulcan: Authentication error")
        
    if not vulcan:
        return True
    for student in client.get_students():
        if student.name == config[DOMAIN][CONF_STUDENT_NAME]:
            client.set_student(student)
            break

    hass.data[DOMAIN] = {
        'student_name_old': config[DOMAIN][CONF_STUDENT_NAME],
        'groups': config[DOMAIN][CONF_GROUPS],
    }
    
    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
    return True

async def async_setup_entry(hass, config_entry):
    students_list = get_students_list()
    hass.data[DOMAIN]['notify'] = config_entry.options.get(CONF_NOTIFY)
    hass.data[DOMAIN]['student_name'] = students_list[config_entry.options.get(CONF_STUDENT_NAME)]

    for student in client.get_students():
        if student.name == students_list[config_entry.options.get(CONF_STUDENT_NAME)]:
            client.set_student(student)
            break
    platform = entity_platform.current_platform.get()
    return True
