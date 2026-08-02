from __future__ import annotations

from datetime import date

import voluptuous as vol

from homeassistant import config_entries

from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectOptionDict,
    DateSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import (
    DOMAIN,

    CONF_NAME,
    CONF_TARIFF,
    CONF_REGION,
    CONF_ENERGY_SENSOR,
    CONF_CYCLE,

    CONF_START_DATE,
    CONF_PERIOD_START,
    CONF_PERIOD_END,

    CONF_PREVIOUS_READING,
    CONF_CURRENT_READING,

    CONF_IVA,
    CONF_DAP,

    CONF_DASHBOARD,
    CONF_HISTORY,
    CONF_REPORTS,
    CONF_EXCEL,
    CONF_PDF,
    CONF_NOTIFICATIONS,

    CONF_LOAD_NAME,
    CONF_LOAD_ENTITY,
    CONF_LOAD_POWER,
    CONF_LOAD_TYPE,
)


class ConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN
):

    VERSION = 1


    async def async_step_user(
        self,
        user_input=None
    ):

        if user_input is not None:

            self.user_data = user_input

            return await self.async_step_loads()


        schema = vol.Schema({

            vol.Required(
                CONF_NAME,
                default="CFE Principal"
            ):
            str,


            vol.Required(
                CONF_ENERGY_SENSOR
            ):
            EntitySelector(
                EntitySelectorConfig(
                    domain="sensor"
                )
            ),


            vol.Required(
                CONF_TARIFF,
                default="1C"
            ):
            SelectSelector(
                SelectSelectorConfig(
                    options=[
                        SelectOptionDict(
                            value="1",
                            label="Tarifa 1"
                        ),

                        SelectOptionDict(
                            value="1A",
                            label="Tarifa 1A"
                        ),

                        SelectOptionDict(
                            value="1B",
                            label="Tarifa 1B"
                        ),

                        SelectOptionDict(
                            value="1C",
                            label="Tarifa 1C"
                        ),

                        SelectOptionDict(
                            value="DAC",
                            label="DAC"
                        ),
                    ]
                )
            ),


            vol.Required(
                CONF_REGION,
                default="norte"
            ):
            SelectSelector(
                SelectSelectorConfig(
                    options=[
                        SelectOptionDict(
                            value="norte",
                            label="Norte"
                        ),

                        SelectOptionDict(
                            value="centro",
                            label="Centro"
                        ),

                        SelectOptionDict(
                            value="sur",
                            label="Sur"
                        ),
                    ]
                )
            ),


            vol.Required(
                CONF_CYCLE,
                default="bimonthly"
            ):
            SelectSelector(
                SelectSelectorConfig(
                    options=[
                        SelectOptionDict(
                            value="bimonthly",
                            label="Bimestral"
                        ),

                        SelectOptionDict(
                            value="monthly",
                            label="Mensual"
                        ),
                    ]
                )
            ),


            vol.Required(
                CONF_START_DATE,
                default=date.today().isoformat()
            ):
            DateSelector(),


            vol.Required(
                CONF_PERIOD_START,
                default=date.today().isoformat()
            ):
            DateSelector(),


            vol.Required(
                CONF_PERIOD_END,
                default=date.today().isoformat()
            ):
            DateSelector(),


            vol.Required(
                CONF_PREVIOUS_READING
            ):
            NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=999999,
                    step=0.01,
                    mode=NumberSelectorMode.BOX
                )
            ),


            vol.Required(
                CONF_CURRENT_READING
            ):
            NumberSelector(
                NumberSelectorConfig(
                    min=0,
                    max=999999,
                    step=0.01,
                    mode=NumberSelectorMode.BOX
                )
            ),


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
                CONF_REPORTS,
                default=False
            ):
            bool,


            vol.Optional(
                CONF_EXCEL,
                default=False
            ):
            bool,


            vol.Optional(
                CONF_PDF,
                default=False
            ):
            bool,


            vol.Optional(
                CONF_NOTIFICATIONS,
                default=True
            ):
            bool,

        })


        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )



    async def async_step_loads(
        self,
        user_input=None
    ):


        if user_input is not None:

            self.user_data["load"] = user_input


            return self.async_create_entry(

                title=self.user_data.get(
                    CONF_NAME,
                    "CFE Principal"
                ),

                data=self.user_data

            )


        schema = vol.Schema({

            vol.Optional(
                CONF_LOAD_NAME,
                default="Clima Manuel"
            ):
            str,


            vol.Optional(
                CONF_LOAD_ENTITY
            ):
            EntitySelector(
                EntitySelectorConfig(
                    domain=[
                        "switch",
                        "climate",
                        "sensor"
                    ]
                )
            ),


            vol.Optional(
                CONF_LOAD_POWER,
                default=1000
            ):
            NumberSelector(
                NumberSelectorConfig(
                    min=1,
                    max=20000,
                    step=1,
                    mode=NumberSelectorMode.BOX
                )
            ),


            vol.Optional(
                CONF_LOAD_TYPE,
                default="switch"
            ):
            SelectSelector(
                SelectSelectorConfig(
                    options=[

                        SelectOptionDict(
                            value="switch",
                            label="Interruptor"
                        ),

                        SelectOptionDict(
                            value="climate",
                            label="Clima"
                        ),

                        SelectOptionDict(
                            value="sensor",
                            label="Sensor de energía"
                        ),

                    ]
                )
            ),

        })


        return self.async_show_form(
            step_id="loads",
            data_schema=schema
        )
