import logging
import os

import voluptuous as vol
from vulcan import Account, Keystore, VulcanHebe

from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN, register

_LOGGER = logging.getLogger(__name__)
from .const import CONF_ATTENDANCE_NOTIFY, CONF_GRADE_NOTIFY, CONF_MESSAGE_NOTIFY


class vulcanFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VulcanOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None, is_new_account=False):
        """GUI > Configuration > Integrations > Plus > Uonet+ Vulcan for Home Assistant"""
        error = None
        regdata = None
        if (
            self._async_current_entries()
            and is_new_account == False
            and not hasattr(self, "is_new_account")
        ):
            return await self.async_step_add_student()

        if user_input is not None:
            regdata = await register.register(
                user_input["token"], user_input["symbol"], user_input["pin"]
            )
            if not error:
                account = regdata["account"]
                keystore = regdata["keystore"]
                client = VulcanHebe(keystore, account)
                self._students = await client.get_students()
                await client.close()

                if len(self._students) > 1:
                    return await self.async_step_select_student()
                else:
                    self._student = self._students[0]
                await self.async_set_unique_id(str(self._student.pupil.id))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"{self._student.pupil.first_name} {self._student.pupil.last_name}",
                    data={
                        "student_id": str(self._student.pupil.id),
                        "login": account.user_login,
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
                "error_text": "\nERROR: " + regdata if regdata else ""
            },
        )

    async def async_step_select_student(self, user_input=None):
        error = None
        students_list = {}
        for student in self._students:
            students_list[
                str(student.pupil.id)
            ] = f"{student.pupil.first_name} {student.pupil.last_name}"
        if user_input is not None:
            student_id = user_input["student"]
            await self.async_set_unique_id(str(student_id))
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=students_list[student_id],
                data={
                    "student_id": str(student_id),
                    "login": self.account.user_login,
                },
            )

        data_schema = {
            vol.Required(
                "student",
            ): vol.In(students_list),
        }
        return self.async_show_form(
            step_id="select_student",
            data_schema=vol.Schema(data_schema),
            description_placeholders={
                "error_text": "\nERROR: " + error if error else ""
            },
        )

    async def async_step_select_saved_credentials(self, user_input=None):
        error = None
        credentials_list = {}
        for file in os.listdir(".vulcan"):
            if file.startswith("account-") and file.endswith(".json"):
                credentials_list[os.path.join(".vulcan", file)] = file[
                    len("account-") :
                ][: -len(".json")]

        if user_input is not None:
            with open(user_input["credentials"].replace("account", "keystore")) as f:
                keystore = Keystore.load(f)
            with open(user_input["credentials"]) as f:
                account = Account.load(f)
            self.account = account
            client = VulcanHebe(keystore, account)
            self._students = await client.get_students()
            await client.close()
            if len(self._students) == 1:
                self._student = self._students[0]
                await self.async_set_unique_id(str(self._student.pupil.id))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"{self._student.pupil.first_name} {self._student.pupil.last_name}",
                    data={
                        "student_id": str(self._student.pupil.id),
                        "login": account.user_login,
                    },
                )
            return await self.async_step_select_student()

        data_schema = {
            vol.Required(
                "credentials",
            ): vol.In(credentials_list),
        }
        return self.async_show_form(
            step_id="select_saved_credentials",
            data_schema=vol.Schema(data_schema),
            description_placeholders={
                "error_text": "\nERROR: " + error if error else ""
            },
        )

    async def async_step_add_student(self, user_input=None):
        error = None
        if user_input is not None:
            if user_input["use_saved_credentials"] == True:
                if len(os.listdir(".vulcan")) == 2:
                    for file in os.listdir(".vulcan"):
                        if file.startswith("keystore"):
                            with open(os.path.join(".vulcan", file)) as f:
                                keystore = Keystore.load(f)
                        elif file.startswith("account"):
                            with open(os.path.join(".vulcan", file)) as f:
                                account = Account.load(f)
                    self.account = account
                    client = VulcanHebe(keystore, account)
                    self._students = await client.get_students()
                    await client.close()
                    if len(self._students) == 1:
                        return self.async_abort(reason="all_student_already_configured")
                    return await self.async_step_select_student()
                else:
                    return await self.async_step_select_saved_credentials()
            else:
                self.is_new_account = True
                return await self.async_step_user(is_new_account=True)

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
        regdata = None
        if user_input is not None:
            regdata = await register.register(
                user_input["token"], user_input["symbol"], user_input["pin"]
            )
            if not error:
                account = regdata["account"]
                keystore = regdata["keystore"]
                client = VulcanHebe(keystore, account)
                students = await client.get_students()
                await client.close()
                for student in students:
                    for entry_id in self._async_current_ids():
                        if str(student.pupil.id) == str(entry_id):
                            existing_entry = await self.async_set_unique_id(
                                str(student.pupil.id)
                            )
                            self.hass.config_entries.async_update_entry(
                                existing_entry,
                                title=f"{student.pupil.first_name} {student.pupil.last_name}",
                                data={
                                    "login": account.user_login,
                                    "student_id": str(student.pupil.id),
                                },
                            )
                            await self.hass.config_entries.async_reload(
                                existing_entry.entry_id
                            )
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
                CONF_MESSAGE_NOTIFY,
                default=self.config_entry.options.get(CONF_MESSAGE_NOTIFY, False),
            ): bool,
            vol.Optional(
                CONF_ATTENDANCE_NOTIFY,
                default=self.config_entry.options.get(CONF_ATTENDANCE_NOTIFY, False),
            ): bool,
            vol.Optional(
                CONF_GRADE_NOTIFY,
                default=self.config_entry.options.get(CONF_GRADE_NOTIFY, False),
            ): bool,
        }

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(options), errors=errors
        )
