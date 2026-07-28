from __future__ import annotations

from datetime import date
import logging

from homeassistant.core import HomeAssistant

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .calculator import calculate_cfe_cost
from .period import CFEPeriodStorage


_LOGGER = logging.getLogger(__name__)


class CFEEnergyCoordinator(
    DataUpdateCoordinator,
):
    """Coordinator de CFE Energy Cost."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: dict,
        entry_id: str,
    ) -> None:

        super().__init__(
            hass,
            _LOGGER,
            name="CFE Energy Cost",
        )

        self.entry_id = entry_id

        self.config = config

        self.energy_sensor = config[
            "energy_sensor"
        ]

        self.period = CFEPeriodStorage(
            hass,
            entry_id,
        )

        self.data = {}


    async def async_config_entry_first_refresh(
        self,
    ):

        await self.async_request_refresh()


    async def async_start_new_period(
        self,
    ):

        state = self.hass.states.get(
            self.energy_sensor
        )

        if state is None:
            return


        meter = float(
            state.state
        )


        await self.period.async_set_period(

            start_date=self.config.get(
                "start_date"
            ),

            end_date=self.config.get(
                "period_end"
            ),

            previous_reading=meter,

            current_reading=meter,

        )


        await self.async_request_refresh()
            async def _async_update_data(
        self,
    ):

        state = self.hass.states.get(
            self.energy_sensor
        )


        if state is None:

            return self.data


        try:

            current_reading = float(
                state.state
            )

        except (
            TypeError,
            ValueError
        ):

            current_reading = 0.0



        previous_reading = float(

            self.config.get(

                "previous_reading",

                0

            )

        )



        period_start = self.config.get(
            "period_start"
        )


        period_end = self.config.get(
            "period_end"
        )


        cut_date = self.config.get(
            "start_date"
        )



        consumption = max(

            0,

            current_reading - previous_reading

        )



        unknown_consumption = max(

            0,

            previous_reading - current_reading

        )



        try:

            start = date.fromisoformat(
                period_start
            )

            end = date.fromisoformat(
                period_end
            )


            days = (

                end - start

            ).days + 1



        except Exception:

            days = 0




        tariff_data = self.config.get(

            "tariff_data",

            {}

        )



        dap_amount = self.config.get(

            "dap_amount",

            0

        )




        bill = calculate_cfe_cost(

            energy_kwh=consumption,

            tariff_data=tariff_data,

            dap_amount=dap_amount,

        )




        self.data = {

            "consumption":

                consumption,


            "previous_reading":

                previous_reading,


            "current_reading":

                current_reading,


            "unknown_consumption":

                unknown_consumption,


            "days":

                days,


            "tariff":

                self.config.get(

                    "tariff"

                ),


            "region":

                self.config.get(

                    "region"

                ),


            "period_start":

                period_start,


            "period_end":

                period_end,


            "cut_date":

                cut_date,



            "energy_cost":

                bill.get(

                    "energy_cost",

                    0

                ),



            "iva":

                bill.get(

                    "iva",

                    0

                ),



            "dap":

                bill.get(

                    "dap",

                    0

                ),



            "total":

                bill.get(

                    "total",

                    0

                ),



            "blocks":

                bill.get(

                    "blocks",

                    []

                ),



            "period":

                {

                    "start":

                        period_start,


                    "end":

                        period_end,


                    "days":

                        days,

                },

        }



        return self.data
