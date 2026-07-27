from __future__ import annotations


import voluptuous as vol


from homeassistant import config_entries

from homeassistant.core import callback

from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectOptionDict,
    EntitySelector,
    EntitySelectorConfig
)


from .const import (
    DOMAIN,
    CONF_ENERGY_SENSOR,
    CONF_TARIFF,
    CONF_REGION,
    CONF_PERIOD_START,
    CONF_PERIOD_END,
    CONF_PREVIOUS_READING,
    CONF_CURRENT_READING
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


        if user_input is not None:


            return self.async_create_entry(
                title=user_input.get(
                    "name",
                    "CFE Principal"
                ),

                data=user_input
            )



        data_schema = vol.Schema(
            {


                vol.Required(
                    "name",
                    default="CFE Principal"
                ): str,



                vol.Required(
                    CONF_ENERGY_SENSOR
                ):
                EntitySelector(
                    EntitySelectorConfig(
                        domain="sensor"
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
                            )
                        ]
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
                                value="1C",
                                label="Tarifa 1C"
                            ),

                            SelectOptionDict(
                                value="DAC",
                                label="DAC"
                            )
                        ]
                    )
                ),




                vol.Required(
                    CONF_PERIOD_START
                ):
                str,



                vol.Required(
                    CONF_PERIOD_END
                ):
                str,



                vol.Required(
                    CONF_PREVIOUS_READING
                ):
                vol.Coerce(float),



                vol.Required(
                    CONF_CURRENT_READING
                ):
                vol.Coerce(float),

            }
        )


        return self.async_show_form(
            step_id="user",
            data_schema=data_schema
        )
