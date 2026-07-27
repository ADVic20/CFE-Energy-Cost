from __future__ import annotations


import logging


from datetime import timedelta, date


from homeassistant.core import HomeAssistant


from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)



from .const import (
    DOMAIN,

    CONF_ENERGY_SENSOR,

    CONF_TARIFF,
    CONF_REGION,

    CONF_START_DATE,

    CONF_PERIOD_START,
    CONF_PERIOD_END,

    CONF_PREVIOUS_READING,
    CONF_CURRENT_READING,
)



from .tariffs.loader import load_tariff


from .calculator import calculate_cfe_cost





_LOGGER = logging.getLogger(__name__)






class CFEEnergyCoordinator(
    DataUpdateCoordinator
):



    def __init__(
        self,
        hass: HomeAssistant,
        config: dict,
        entry_id: str
    ):


        self.hass = hass

        self.config = config

        self.entry_id = entry_id



        super().__init__(

            hass,

            _LOGGER,

            name=DOMAIN,

            update_interval=timedelta(
                minutes=5
            )

        )







    async def _async_update_data(
        self
    ):


        try:


            return await self.async_calculate()



        except Exception as error:


            raise UpdateFailed(

                f"CFE Energy Cost error: {error}"

            )







    async def async_calculate(
        self
    ):



        #
        # Lectura del medidor
        #

        meter = 0



        sensor = self.config.get(
            CONF_ENERGY_SENSOR
        )



        if sensor:


            state = self.hass.states.get(
                sensor
            )


            if state:


                try:

                    meter = float(
                        state.state
                    )


                except ValueError:

                    meter = 0







        #
        # Lecturas del recibo
        #

        previous = float(

            self.config.get(

                CONF_PREVIOUS_READING,

                0

            )

        )



        current = float(

            self.config.get(

                CONF_CURRENT_READING,

                0

            )

        )





        consumption = round(

            current - previous,

            2

        )



        if consumption < 0:

            consumption = 0








        #
        # Fechas
        #

        period_start = self.config.get(

            CONF_PERIOD_START

        )


        period_end = self.config.get(

            CONF_PERIOD_END

        )




        days = 0



        if period_start and period_end:


            try:


                start = date.fromisoformat(

                    str(period_start)

                )


                end = date.fromisoformat(

                    str(period_end)

                )


                days = (

                    end - start

                ).days



            except Exception:


                days = 0







        #
        # Tarifa
        #

        tariff = self.config.get(

            CONF_TARIFF,

            "1C"

        )



        region = self.config.get(

            CONF_REGION,

            "norte"

        )





        tariff_file = load_tariff(

            "mexico",

            region,

            f"tarifa_{tariff.lower()}"

        )



        if tariff_file is None:


            raise Exception(

                f"Tariff not found: {tariff}"

            )







        #
        # Calculo CFE
        #

        result = calculate_cfe_cost(

            consumption,

            tariff_file

        )








        return {


            "meter":

                meter,



            "consumption":

                consumption,



            "previous_reading":

                previous,



            "current_reading":

                current,



            "period_start":

                period_start,



            "period_end":

                period_end,



            "cut_date":

                self.config.get(

                    CONF_START_DATE

                ),



            "days":

                days,



            "tariff":

                tariff_file.get(

                    "name",

                    tariff

                ),



            "region":

                region,



            "energy_cost":

                result.get(

                    "energy_cost",

                    0

                ),



            "iva":

                result.get(

                    "iva",

                    0

                ),



            "dap":

                result.get(

                    "dap",

                    0

                ),



            "total":

                result.get(

                    "total",

                    0

                ),



        }
