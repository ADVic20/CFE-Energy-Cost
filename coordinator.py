from __future__ import annotations

from datetime import date

import logging

from homeassistant.core import HomeAssistant

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from homeassistant.helpers.event import (
    async_track_state_change_event,
)

from .tariff_loader import load_tariff
from .calculator import calculate_cfe_cost
from .period import CFEPeriodStorage
from .loads import (
    LoadManager,
    EnergyLoad,
)


_LOGGER = logging.getLogger(__name__)


class CFEEnergyCoordinator(
    DataUpdateCoordinator,
):
    """Coordinator de CFE Energy Cost."""


    def __init__(
        self,
        hass: HomeAssistant,
        config: dict,
        options: dict,
        entry_id: str,
    ) -> None:


        super().__init__(
            hass,
            _LOGGER,
            name="CFE Energy Cost",
        )


        self.hass = hass

        self.entry_id = entry_id

        self.config = config

        self.options = options


        self.energy_sensor = config[
            "energy_sensor"
        ]


        self.period = CFEPeriodStorage(
            hass,
            entry_id,
        )


        self.loads = LoadManager()


        self._load_listeners = []


        self._setup_loads()



        self.data = {}



    def _setup_loads(self):

        loads = self.options.get(
            "loads",
            []
        )


        for item in loads:


            load = EnergyLoad(

                name=item.get(
                    "name"
                ),

                entity_id=item.get(
                    "entity_id"
                ),

                power_w=item.get(
                    "power_w",
                    0
                ),

                load_type=item.get(
                    "type",
                    "switch"
                ),

            )


            self.loads.add_load(
                load
            )


            remove = async_track_state_change_event(

                self.hass,

                load.entity_id,

                self._load_state_changed,

            )


            self._load_listeners.append(
                remove
            )



    async def _load_state_changed(
        self,
        event
    ):


        new_state = event.data.get(
            "new_state"
        )


        if new_state is None:

            return



        self.loads.update_load(

            event.data.get(
                "entity_id"
            ),

            new_state.state

        )


        await self.async_request_refresh()



    async def async_config_entry_first_refresh(
        self,
    ):

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



        consumption = max(

            0,

            current_reading -
            previous_reading

        )



        tariff_data = load_tariff(

            self.config.get(
                "tariff",
                "1C"
            ),

            self.config.get(
                "region",
                "norte"
            ),

        )



        bill = calculate_cfe_cost(

            energy_kwh=consumption,

            tariff_data=tariff_data,

            dap_amount=self.config.get(
                "dap_amount",
                0
            ),

        )



        self.data = {

            "consumption":
                consumption,


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


            "loads_kwh":
                self.loads.total_kwh(),


            "loads":
                {

                    load.name:
                        load.estimated_kwh

                    for load in
                    self.loads.loads.values()

                },

        }


        return self.data
