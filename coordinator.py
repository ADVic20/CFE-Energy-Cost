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


        try:

            energy = float(
                state.state
            )


        except ValueError:

            raise Exception(
                "Energy sensor value invalid"
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


        #
        # Región
        #

        country = (
            self.config
            .get(
                CONF_REGION,
                "mexico"
            )
            .lower()
        )



        #
        # Convertimos:
        #
        # 1C
        #  |
        #  v
        # tarifa_1C.json
        #

        if not tariff.startswith(
            "tarifa_"
        ):

            tariff = (
                "tarifa_"
                +
                tariff
            )



        tariff_data = load_tariff(
            country,
            tariff
        )



        result = calculate_cfe_cost(
            energy,
            tariff_data,
            dap_amount=0
        )



        return {

            "energy": energy,

            "tariff": tariff_data[
                "name"
            ],

            "currency": tariff_data[
                "currency"
            ],

            "energy_cost": result[
                "energy_cost"
            ],

            "iva": result[
                "iva"
            ],

            "dap": result[
                "dap"
            ],

            "total": result[
                "total"
            ],

            "blocks": result[
                "blocks"
            ]

        }
