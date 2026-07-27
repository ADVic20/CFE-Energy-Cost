from __future__ import annotations


import voluptuous as vol


from homeassistant import config_entries

from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectOptionDict
)


from .const import (
    DOMAIN,

    CONF_NAME,

    CONF_TARIFF,
    CONF_REGION,

    CONF_ENERGY_SENSOR,

    CONF_CYCLE,

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



        if user_input is not None:


            return self.async_create_entry(

                title=user_input.get(
                    CONF_NAME,
                    "CFE Principal"
                ),

                data=user_input

            )





        schema = vol.Schema(


            {


                #
                # Nombre
                #

                vol.Required(
                    CONF_NAME,
                    default="CFE Principal"
                ):
                str,



                #
                # Sensor medidor
                #

                vol.Required(
                    CONF_ENERGY_SENSOR
                ):
                EntitySelector(

                    EntitySelectorConfig(
                        domain="sensor"
                    )

                ),




                #
                # Tarifa
                #

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
                            )

                        ]

                    )

                ),





                #
                # Región
                #

                vol.Required(
                    CONF_REGION,
                    default="Norte"
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





                #
                # Ciclo
                #

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
                            )

                        ]

                    )

                ),





                #
                # Periodo del recibo
                #

                vol.Required(
                    CONF_PERIOD_START
                ):
                str,



                vol.Required(
                    CONF_PERIOD_END
                ):
                str,





                #
                # Lecturas CFE
                #

                vol.Required(
                    CONF_PREVIOUS_READING
                ):
                vol.Coerce(float),



                vol.Required(
                    CONF_CURRENT_READING
                ):
                vol.Coerce(float),





                #
                # Cargos
                #

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





                #
                # Funciones
                #

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


            }

        )




        return self.async_show_form(

            step_id="user",

            data_schema=schema

        )
