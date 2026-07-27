from __future__ import annotations


import logging


from datetime import timedelta


from homeassistant.core import HomeAssistant


from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)



from .const import (
    DOMAIN,
    CONF_ENERGY_SENSOR,
    CONF_TARIFF,
    CONF_REGION
)


from .tariffs.loader import load_tariff


from .calculator import calculate_cfe_cost


from .period import CFEPeriodStorage




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


        self.energy_sensor = config.get(
            CONF_ENERGY_SENSOR
        )



        self.period = CFEPeriodStorage(
            hass,
            entry_id
        )



        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                minutes=5
            )
        )




    async def async_initialize(
        self
    ):


        await self.period.async_load()





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



        state = self.hass.states.get(
            self.energy_sensor
        )



        if state is None:

            raise Exception(
                "Energy sensor not found"
            )



        meter_value = float(
            state.state
        )



        #
        # Consumo del recibo
        #

        consumption = (
            self.period
            .get_consumption()
        )



        #
        # Tarifa
        #

        tariff = self.config.get(
            CONF_TARIFF,
            "1C"
        )



        tariff = tariff.lower()



        if not tariff.startswith(
            "tarifa_"
        ):

            tariff = (
                "tarifa_"
                +
                tariff
            )



        #
        # Región
        #

        region = self.config.get(
            CONF_REGION,
            "norte"
        )



        tariff_data = load_tariff(
            "mexico",
            region,
            tariff
        )



        if tariff_data is None:

            raise Exception(
                "Tariff not found"
            )



        result = calculate_cfe_cost(
            consumption,
            tariff_data
        )




        return {


            "meter": meter_value,


            "energy": consumption,



            "period_start":
            self.period.data.get(
                "start_date"
            ),



            "period_end":
            self.period.data.get(
                "end_date"
            ),



            "previous_reading":
            self.period.data.get(
                "previous_reading"
            ),



            "current_reading":
            self.period.data.get(
                "current_reading"
            ),



            "tariff":
            tariff_data.get(
                "name"
            ),



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
            )

        }
