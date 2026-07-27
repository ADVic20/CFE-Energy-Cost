from __future__ import annotations

import logging

from datetime import timedelta
from .period import CFEPeriodStorage

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



_LOGGER = logging.getLogger(__name__)




class CFEEnergyCoordinator(
    DataUpdateCoordinator
):


    def __init__(
        self,
        hass: HomeAssistant,
        config: dict
    ):


        self.hass = hass

        self.config = config


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


        energy_sensor = (
            self.config[
                CONF_ENERGY_SENSOR
            ]
        )


        state = self.hass.states.get(
            energy_sensor
        )


        if state is None:

            raise Exception(
                f"Sensor not found: {energy_sensor}"
            )



        energy = float(
            state.state
        )



        #
        # Tarifa
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
        # País y región
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



        result = calculate_cfe_cost(
            energy,
            tariff_data
        )



        return {

            "energy": energy,

            "tariff": tariff_data["name"],

            "energy_cost": result["energy_cost"],

            "iva": result["iva"],

            "dap": result["dap"],

            "total": result["total"],

            "blocks": result["blocks"]

        }
