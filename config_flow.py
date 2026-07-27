from **future** import annotations

from datetime import date

import voluptuous as vol

from homeassistant import config_entries

from homeassistant.helpers import selector

from .const import (

```
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

CONF_NOTIFICATIONS
```

)

class CFEEnergyCostConfigFlow(
config_entries.ConfigFlow,
domain=DOMAIN
):

```
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



            vol.Required(
                CONF_NAME,
                default="CFE Principal"
            ):
            str,





            vol.Required(
                CONF_ENERGY_SENSOR
            ):
            selector.EntitySelector(

                selector.EntitySelectorConfig(
                    domain="sensor"
                )

            ),






            vol.Required(
                CONF_TARIFF,
                default="1C"
            ):
            selector.SelectSelector(

                selector.SelectSelectorConfig(

                    options=[

                        selector.SelectOptionDict(
                            value="1",
                            label="Tarifa 1"
                        ),

                        selector.SelectOptionDict(
                            value="1A",
                            label="Tarifa 1A"
                        ),

                        selector.SelectOptionDict(
                            value="1B",
                            label="Tarifa 1B"
                        ),

                        selector.SelectOptionDict(
                            value="1C",
                            label="Tarifa 1C"
                        ),

                        selector.SelectOptionDict(
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
            selector.SelectSelector(

                selector.SelectSelectorConfig(

                    options=[

                        selector.SelectOptionDict(
                            value="norte",
                            label="Norte"
                        ),

                        selector.SelectOptionDict(
                            value="centro",
                            label="Centro"
                        ),

                        selector.SelectOptionDict(
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
            selector.SelectSelector(

                selector.SelectSelectorConfig(

                    options=[

                        selector.SelectOptionDict(
                            value="bimonthly",
                            label="Bimestral"
                        ),

                        selector.SelectOptionDict(
                            value="monthly",
                            label="Mensual"
                        ),

                    ]

                )

            ),






            #
            # Fecha de corte
            #

            vol.Required(
                CONF_START_DATE,
                default=date.today()
            ):
            selector.DateSelector(),






            #
            # Periodo del recibo
            #

            vol.Required(
                CONF_PERIOD_START,
                default=date.today()
            ):
            selector.DateSelector(),




            vol.Required(
                CONF_PERIOD_END,
                default=date.today()
            ):
            selector.DateSelector(),






            #
            # Lecturas
            #

            vol.Required(
                CONF_PREVIOUS_READING
            ):
            selector.NumberSelector(

                selector.NumberSelectorConfig(

                    min=0,

                    max=999999,

                    step=0.01,

                    mode=selector.NumberSelectorMode.BOX

                )

            ),





            vol.Required(
                CONF_CURRENT_READING
            ):
            selector.NumberSelector(

                selector.NumberSelectorConfig(

                    min=0,

                    max=999999,

                    step=0.01,

                    mode=selector.NumberSelectorMode.BOX

                )

            ),






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
