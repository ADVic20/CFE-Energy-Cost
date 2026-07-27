from __future__ import annotations


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


        self.data = {}




    async def async_load(
        self
    ):


        saved = await self.store.async_load()


        if saved is None:

            saved = {

                "start_date": None,

                "end_date": None,

                "previous_reading": None,

                "current_reading": None

            }


        self.data = saved


        return self.data





    async def async_set_period(
        self,
        start_date: str,
        end_date: str,
        previous_reading: float,
        current_reading: float
    ):


        self.data = {

            "start_date": start_date,

            "end_date": end_date,

            "previous_reading": previous_reading,

            "current_reading": current_reading

        }


        await self.store.async_save(
            self.data
        )





    def get_consumption(
        self
    ):


        previous = self.data.get(
            "previous_reading"
        )


        current = self.data.get(
            "current_reading"
        )



        if (
            previous is None
            or current is None
        ):

            return 0



        return round(
            current - previous,
            2
        )
