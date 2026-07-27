from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator
)

from homeassistant.core import HomeAssistant


from .const import DOMAIN



class CFEEnergyCoordinator(
    DataUpdateCoordinator
):


    def __init__(
        self,
        hass: HomeAssistant,
        config
    ):


        self.config = config


        super().__init__(
            hass,
            hass.helpers.event,
            name=DOMAIN,
            update_interval=timedelta(
                minutes=5
            )
        )



    async def _async_update_data(
        self
    ):

        energy_sensor = (
            self.config["energy_sensor"]
        )


        state = self.hass.states.get(
            energy_sensor
        )


        if state is None:

            return {}


        energy = float(
            state.state
        )


        tariff = (
            self.config
            .get("tariff", {})
            .get("type", "DAC")
        )


        cost = self.calculate_cost(
            energy,
            tariff
        )


        return {

            "energy": energy,

            "cost": cost,

            "tariff": tariff

        }



    def calculate_cost(
        self,
        kwh,
        tariff
    ):


        if tariff == "DAC":

            return kwh * 6.5


        if tariff == "1":

            return kwh * 1.2


        return kwh * 2.5
