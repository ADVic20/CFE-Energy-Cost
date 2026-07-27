import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector
from datetime import date

from .const import (
    DOMAIN,

    CONF_NAME,
    CONF_TARIFF,
    CONF_REGION,

    CONF_ENERGY_SENSOR,

    CONF_START_DATE,
    CONF_CYCLE,

    CONF_IVA,
    CONF_DAP,

    CONF_DASHBOARD,
    CONF_HISTORY,
    CONF_EXCEL,
    CONF_PDF,
    CONF_NOTIFICATIONS
)


class CFEEnergyCostConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN
):

    VERSION = 1


    async def async_step_user(
        self,
        user_input=None
    ):

        return await self.async_step_general()



    async def async_step_general(
        self,
        user_input=None
    ):


        if user_input:

            self.data = user_input

            return await self.async_step_meter()



        schema = vol.Schema(
            {

                vol.Required(
                    CONF_NAME,
                    default="CFE Principal"
                ):
                str,


                vol.Required(
                    CONF_TARIFF,
                    default="1C"
                ):
                vol.In(
                    [
                        "1",
                        "1A",
                        "1B",
                        "1C",
                        "DAC"
                    ]
                ),


                vol.Required(
                    CONF_REGION,
                    default="Norte"
                ):
                str

            }
        )


        return self.async_show_form(
            step_id="general",
            data_schema=schema
        )



    async def async_step_meter(
        self,
        user_input=None
    ):


        if user_input:

            self.data.update(
                user_input
            )

            return await self.async_step_billing()



        schema = vol.Schema(
            {

                vol.Required(
                    CONF_ENERGY_SENSOR
                ):
                selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="energy"
                     )
                )

            }
        )


        return self.async_show_form(
            step_id="meter",
            data_schema=schema
        )



    async def async_step_billing(
        self,
        user_input=None
    ):


        if user_input:

            self.data.update(
                user_input
            )

            return await self.async_step_options()



        schema = vol.Schema(
            {

                vol.Required(
                    CONF_START_DATE
                ):
                selector.DateSelector(),


                vol.Required(
                    CONF_CYCLE,
                    default="bimonthly"
                ):
                vol.In(
                    [
                        "monthly",
                        "bimonthly"
                    ]
                )

            }
        )


        return self.async_show_form(
            step_id="billing",
            data_schema=schema
        )



    async def async_step_options(
        self,
        user_input=None
    ):


        if user_input:

            self.data.update(
                user_input
            )


            return self.async_create_entry(
                title=self.data[CONF_NAME],
                data=self.data
            )



        schema = vol.Schema(
            {


                vol.Optional(
                    CONF_IVA,
                    default=True
                ):
                bool,


                vol.Optional(
                    CONF_DAP,
                    default=True
                ):
                bool,


                vol.Optional(
                    CONF_DASHBOARD,
                    default=True
                ):
                bool,


                vol.Optional(
                    CONF_HISTORY,
                    default=True
                ):
                bool,


                vol.Optional(
                    CONF_EXCEL,
                    default=True
                ):
                bool,


                vol.Optional(
                    CONF_PDF,
                    default=True
                ):
                bool,


                vol.Optional(
                    CONF_NOTIFICATIONS,
                    default=True
                ):
                bool

            }
        )


        return self.async_show_form(
            step_id="options",
            data_schema=schema
        )
