from __future__ import annotations

import logging
from pathlib import Path
import json

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from homeassistant.helpers.event import (
    async_track_state_change_event,
)

from homeassistant.core import callback

from .calculator import calculate_cfe_cost
from .period import CFEPeriodStorage
from .const import (
    CONF_ENERGY_SENSOR,
    CONF_TARIFF,
)

_LOGGER = logging.getLogger(__name__)


class CFEEnergyCoordinator(DataUpdateCoordinator):
    """Coordinator CFE Energy Cost."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: dict,
        entry_id: str,
    ):

        super().__init__(
            hass,
            _LOGGER,
            name="CFE Energy Cost",
        )

        self.config = config
        self.entry_id = entry_id

        self.energy_sensor = config[CONF_ENERGY_SENSOR]

        self.tariff = config[CONF_TARIFF]

        self.period = CFEPeriodStorage(
            hass,
            entry_id,
        )

        self.cost = {}

    async def async_config_entry_first_refresh(self):

        await self.period.async_load()

        await self._async_update_data()

        async_track_state_change_event(
            self.hass,
            [self.energy_sensor],
            self._sensor_updated,
        )

    @callback
    async def _sensor_updated(
        self,
        event,
    ):

        await self.async_refresh()

    async def _async_update_data(self):

        state = self.hass.states.get(
            self.energy_sensor
        )

        if state is None:
            return

        try:
            current_energy = float(
                state.state
            )

        except (ValueError, TypeError):
            return

        consumption = self.period.calculate_consumption(
            current_energy
        )

        tariff_file = (
            Path(__file__).parent
            / "tariffs"
            / f"{self.tariff}.json"
        )

        with open(
            tariff_file,
            "r",
            encoding="utf-8",
        ) as file:

            tariff_data = json.load(file)

        self.cost = calculate_cfe_cost(
            consumption,
            tariff_data,
        )

        self.async_update_listeners()

        return self.cost
