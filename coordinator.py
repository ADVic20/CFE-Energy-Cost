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


        self.energy_sensor = (
            config[
                CONF_ENERGY_SENSOR
            ]
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
                f"Energy sensor not found: {self.energy_sensor}"
            )



        try:

            meter_value = float(
                state.state
            )


        except ValueError:

            raise Exception(
                "Invalid energy value"
            )



        #
        # Consumo real del periodo
        #

        consumption = (
            self.period
            .calculate_consumption(
                meter_value
            )
        )



        #
        # Tarifa seleccionada
        #

        tariff = (
            self.config
            .get(
                CONF_TARIFF,
                "1C"
            )
            .lower()
        )


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

        country = "mexico"


        region = (
            self.config
            .get(
                CONF_REGION,
                "norte"
            )
            .lower()
        )



        tariff_data = load_tariff(
            country,
            region,
            tariff
        )



        #
        # Cálculo CFE
        #

        result = calculate_cfe_cost(
            consumption,
            tariff_data
        )



        return {

            # Medidor acumulado real

            "meter": meter_value,


            # Consumo del periodo

            "energy": consumption,


            # Datos del periodo

            "initial_meter":
            self.period.data.get(
                "initial_meter"
            ),


            "start_date":
            self.period.data.get(
                "start_date"
            ),



            # Tarifa

            "tariff":
            tariff_data[
                "name"
            ],



            # Costos

            "energy_cost":
            result[
                "energy_cost"
            ],


            "iva":
            result[
                "iva"
            ],


            "dap":
            result[
                "dap"
            ],


            "total":
            result[
                "total"
            ],



            "blocks":
            result[
                "blocks"
            ]

        }
