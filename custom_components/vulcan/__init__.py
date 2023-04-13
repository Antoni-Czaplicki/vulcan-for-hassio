"""The Vulcan component."""

from aiohttp import ClientConnectorError
from vulcan import Account, Keystore, UnauthorizedCertificateException, Vulcan

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

PLATFORMS = [Platform.CALENDAR, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Uonet+ Vulcan integration."""
    hass.data.setdefault(DOMAIN, {})
    try:
        keystore = Keystore.load(entry.data["keystore"])
        account = Account.load(entry.data["account"])
        client = Vulcan(keystore, account, async_get_clientsession(hass))
        await client.select_student()
        students = await client.get_students()
        for student in students:
            if str(student.pupil.id) == str(entry.data["student_id"]):
                client.student = student
                break
    except UnauthorizedCertificateException as err:
        raise ConfigEntryAuthFailed("The certificate is not authorized.") from err
    except ClientConnectorError as err:
        raise ConfigEntryNotReady(
            f"Connection error - please check your internet connection: {err}"
        ) from err
    hass.data[DOMAIN]["students_number"] = len(
        hass.config_entries.async_entries(DOMAIN)
    )
    hass.data[DOMAIN][entry.entry_id] = client

    if not entry.update_listeners:
        entry.add_update_listener(_async_update_options)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def _async_update_options(hass, entry):
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        try:
            with open(
                f".vulcan/keystore-{config_entry.data.get('login')}.json"
            ) as file:
                keystore_old = Keystore.load(file)
            with open(f".vulcan/account-{config_entry.data.get('login')}.json") as file:
                account_old = Account.load(file)
        except:
            _LOGGER.error(
                "Migration to config version 2 unsuccessful, please reconfigure integration"
            )
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={"source": "reauth"},
                )
            )
            config_entry.version = 2
            return False

        data = {
            "student_id": config_entry.data["student_id"],
            "keystore": keystore_old.as_dict,
            "account": account_old.as_dict,
        }

        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=data)

    _LOGGER.info("Migration to version %s successful", config_entry.version)

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
