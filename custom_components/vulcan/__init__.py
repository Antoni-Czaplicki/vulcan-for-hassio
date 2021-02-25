# This Integration uses unofficial Vulcan-api https://github.com/kapi2289/vulcan-api
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType
from vulcan import Account, Keystore, Vulcan

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

client = None


async def async_setup(hass, config) -> bool:
    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass, config_entry):
    global client
    try:
        with open(f".vulcan/keystore-{config_entry.data.get('login')}.json") as f:
            keystore = Keystore.load(f)
        with open(f".vulcan/account-{config_entry.data.get('login')}.json") as f:
            account = Account.load(f)
        client = Vulcan(keystore, account)
        await client.select_student()
        students = await client.get_students()
        for student in students:
            if student.pupil.id == config_entry.data.get("student_id"):
                client.student = student
                break
    except:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": "reauth"},
            )
        )
        return False
    num = 0
    for _ in hass.config_entries.async_entries(DOMAIN):
        num += 1
    hass.data[DOMAIN]["students_number"] = num
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True


class VulcanEntity(Entity):
    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def state(self):
        return self._state
