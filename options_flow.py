from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectOptionDict,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import DOMAIN


CONF_LOADS = "loads"
CONF_LOAD_NAME = "load_name"
CONF_LOAD_ENTITY = "load_entity"
CONF_LOAD_POWER = "load_power"
CONF_LOAD_TYPE = "load_type"


class OptionsFlowHandler(
    config_entries.OptionsFlow
):
    """Manage CFE Energy Cost options."""


    def __init__(
        self,
        config_entry
    ):
        self.config_entry = config_entry


        self.loads = list(
            config_entry.options.get(
                CONF_LOADS,
                []
            )
        )



    async def async_step_init(
        self,
        user_input=None
    ):

        if user_input is not None:

            self.loads.append({

                "name":
                    user_input[CONF_LOAD_NAME],


                "entity_id":
                    user_input[CONF_LOAD_ENTITY],


                "power_w":
                    user_input[CONF_LOAD_POWER],


                "type":
                    user_input[CONF_LOAD_TYPE],

            })


            return await self.async_step_add_more()



        return await self.async_step_load()



    async def async_step_load(
        self,
        user_input=None
    ):

        schema = vol.Schema({

            vol.Required(
                CONF_LOAD_NAME,
                default="Clima Manuel"
            ):
            str,


            vol.Required(
                CONF_LOAD_ENTITY
            ):
            EntitySelector(

                EntitySelectorConfig(

                    domain=[

                        "switch",

                        "climate",

                        "sensor",

                    ]

                )

            ),



            vol.Required(
                CONF_LOAD_POWER,
                default=1000
            ):
            NumberSelector(

                NumberSelectorConfig(

                    min=1,

                    max=30000,

                    step=1,

                    mode=NumberSelectorMode.BOX

                )

            ),



            vol.Required(
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

            step_id="load",

            data_schema=schema

        )



    async def async_step_add_more(
        self,
        user_input=None
    ):


        if user_input is not None:


            if user_input.get(
                "add_more"
            ):

                return await self.async_step_load()



            return self.async_create_entry(

                title="",

                data={

                    CONF_LOADS:
                        self.loads

                }

            )



        schema = vol.Schema({

            vol.Required(
                "add_more",
                default=True
            ):
            bool

        })


        return self.async_show_form(

            step_id="add_more",

            data_schema=schema

        )
