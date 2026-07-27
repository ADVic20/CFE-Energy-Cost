from __future__ import annotations

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

            name=DOMAIN,

            update_interval=timedelta(
                minutes=5
            )
        )



    async def _async_update_data(
        self
    ):

        try:

            return await self.calculate()



        except Exception as error:

            raise UpdateFailed(
                f"CFE calculation error: {error}"
            )



    async def calculate(
        self
    ):


        sensor = (
            self.config
            [CONF_ENERGY_SENSOR]
        )


        state = self.hass.states.get(
            sensor
        )


        if state is None:

            raise Exception(
                f"Energy sensor not found: {sensor}"
            )


        try:

            energy = float(
                state.state
            )


        except ValueError:

            raise Exception(
                "Invalid energy value"
            )



        tariff_name = (
            self.config
            .get(
                CONF_TARIFF,
                "tarifa_1C"
            )
            .lower()
        )


        region = (
            self.config
            .get(
                CONF_REGION,
                "mexico"
            )
            .lower()
        )



        tariff = load_tariff(
            region,
            tariff_name
        )



        result = calculate_cfe_cost(
            energy,
            tariff,
            dap_amount=0
        )



        return {

            "energy": energy,

            "tariff": tariff["name"],

            "cost": result["energy_cost"],

            "iva": result["iva"],

            "dap": result["dap"],

            "total": result["total"],

            "blocks": result["blocks"]

        }
