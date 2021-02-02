import logging
import os

import voluptuous as vol
from vulcan import Account, Keystore, VulcanHebe

from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN, register

_LOGGER = logging.getLogger(__name__)
from .const import CONF_ATTENDANCE_NOTIFY, CONF_NOTIFY, CONF_STUDENT_NAME


class vulcanFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VulcanOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """GUI > Configuration > Integrations > Plus > Uonet+ Vulcan for Home Assistant"""
        error = None
        if self._async_current_entries():
            try:
                if (
                    os.stat(".vulcan/keystore.json").st_size != 0
                    and os.stat(".vulcan/account.json").st_size != 0
                ):
                    with open(".vulcan/keystore.json") as f:
                        keystore = Keystore.load(f)
                    with open(".vulcan/account.json") as f:
                        account = Account.load(f)
                    client = VulcanHebe(keystore, account)
                    self._students = await client.get_students()
                    await client.close()
                    if len(self._students) == 1:
                        return self.async_abort(reason="all_student_already_configured")
                    else:
                        return await self.async_step_add_student()
            except:
                pass

        if user_input is not None:
            error = await register.register(
                user_input["token"], user_input["symbol"], user_input["pin"]
            )
            if not error:
                with open(".vulcan/keystore.json") as f:
                    keystore = Keystore.load(f)
                with open(".vulcan/account.json") as f:
                    account = Account.load(f)
                client = VulcanHebe(keystore, account)
                self._students = await client.get_students()
                await client.close()

                if len(self._students) > 1:
                    return await self.async_step_select_student()
                else:
                    self._student = self._students[0]
                await self.async_set_unique_id(self._student.pupil.id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=self._student.pupil.first_name
                    + " "
                    + self._student.pupil.last_name,
                    data={
                        "user_input": user_input,
                        "student_id": self._student.pupil.id,
                        "students_number": len(self._students),
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("token"): str,
                    vol.Required("symbol"): str,
                    vol.Required("pin"): str,
                }
            ),
            description_placeholders={
                "error_text": "\nERROR: " + error if error else ""
            },
        )

    async def async_step_select_student(self, user_input=None):
        error = None

        students_list = {}
        for student in self._students:
            students_list[str(student.pupil.id)] = (
                student.pupil.first_name + " " + student.pupil.last_name
            )

        if user_input is not None:
            student_id = user_input[CONF_STUDENT_NAME]
            await self.async_set_unique_id(student_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=get_students_list()[student_id],
                data={
                    "user_input": user_input,
                    "student_id": student_id,
                    "students_number": len(students_list),
                },
            )

        data_schema = {
            vol.Required(
                CONF_STUDENT_NAME,
            ): vol.In(students_list),
        }
        return self.async_show_form(
            step_id="select_student",
            data_schema=vol.Schema(data_schema),
            description_placeholders={
                "error_text": "\nERROR: " + error if error else ""
            },
        )

    async def async_step_add_student(self, user_input=None):
        error = None
        if user_input is not None:
            if user_input["use_saved_credentials"] == True:
                return await self.async_step_select_student()
            else:
                if os.path.exists(".vulcan/keystore.json"):
                    os.remove(".vulcan/keystore.json")
                if os.path.exists(".vulcan/account.json"):
                    os.remove(".vulcan/account.json")
                return await self.async_step_user()

        data_schema = {
            vol.Required("use_saved_credentials", default=True): bool,
        }
        return self.async_show_form(
            step_id="add_student",
            data_schema=vol.Schema(data_schema),
            description_placeholders={
                "error_text": "\nERROR: " + error if error else ""
            },
        )

    async def async_step_reauth(self, user_input=None):
        error = None

        if user_input is not None:
            error = await register.register(
                user_input["token"], user_input["symbol"], user_input["pin"]
            )
            if not error:
                with open(".vulcan/keystore.json") as f:
                    keystore = Keystore.load(f)
                with open(".vulcan/account.json") as f:
                    account = Account.load(f)
                client = VulcanHebe(keystore, account)
                students = await client.get_students()
                await client.close()
                for student in students:
                    existing_entry = await self.async_set_unique_id(student.pupil.id)
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth",
            data_schema=vol.Schema(
                {
                    vol.Required("token"): str,
                    vol.Required("symbol"): str,
                    vol.Required("pin"): str,
                }
            ),
            description_placeholders={
                "error_text": "\nERROR: " + error if error else ""
            },
        )


class VulcanOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry
        self._students = {}

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Optional(
                CONF_NOTIFY,
                default=self.config_entry.options.get(CONF_NOTIFY, False),
            ): bool,
            vol.Optional(
                CONF_ATTENDANCE_NOTIFY,
                default=self.config_entry.options.get(CONF_ATTENDANCE_NOTIFY, False),
            ): bool,
        }

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(options), errors=errors
        )
