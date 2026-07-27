import voluptuous as vol

from homeassistant.config_entries import (
    ConfigSubentryFlow
)

from .const import (
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_DEVICE_SENSOR,
    DEVICE_TYPES
)



class CFEDeviceSubentryFlow(
    ConfigSubentryFlow
):


    async def async_step_user(
        self,
        user_input=None
    ):


        if user_input:

            return self.async_create_entry(
                title=user_input[CONF_DEVICE_NAME],
                data=user_input
            )



        schema = vol.Schema(
            {

                vol.Required(
                    CONF_DEVICE_NAME
                ):
                str,


                vol.Required(
                    CONF_DEVICE_TYPE
                ):
                vol.In(
                    DEVICE_TYPES
                ),


                vol.Required(
                    CONF_DEVICE_SENSOR
                ):
                str

            }
        )


        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )
