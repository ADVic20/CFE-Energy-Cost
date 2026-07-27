from __future__ import annotations

from datetime import datetime

from homeassistant.helpers.storage import Store


STORAGE_VERSION = 1
STORAGE_KEY = "cfe_energy_cost_period"



class CFEPeriodStorage:


    def __init__(
        self,
        hass,
        entry_id
    ):

        self.store = Store(
            hass,
            STORAGE_VERSION,
            f"{STORAGE_KEY}_{entry_id}"
        )


        self.data = None



    async def async_load(
        self
    ):

        self.data = await self.store.async_load()


        if self.data is None:

            self.data = {

                "start_date": None,

                "initial_meter": None

            }


        return self.data




    async def async_set_start(
        self,
        meter_value: float,
        start_date: str
    ):


        self.data = {

            "start_date": start_date,

            "initial_meter": meter_value

        }


        await self.store.async_save(
            self.data
        )




    def calculate_consumption(
        self,
        current_meter: float
    ):


        if not self.data:

            return 0



        initial = self.data.get(
            "initial_meter"
        )


        if initial is None:

            return 0



        return round(
            current_meter - initial,
            2
        )
