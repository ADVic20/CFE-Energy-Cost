"""Config flow for CFE Energy Cost."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_MAIN_SENSOR,
    CONF_TARIFF,
    CONF_PERIOD_DAYS,
    CONF_START_DATE,
)

TARIFFS = [
    "Tarifa 1",
    "Tarifa 1A",
    "Tarifa 1B",
    "Tarifa 1C",
    "Tarifa 1D",
    "Tarifa 1E",
    "Tarifa 1F",
    "DAC",
    "Personalizada",
]


class CFEEnergyCostConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CFE Energy Cost."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ):
        """Handle the initial step."""

        if user_input is not None:

            await self.async_set_unique_id("cfe_energy_cost")

            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="CFE Energy Cost",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_MAIN_SENSOR,
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            device_class="energy",
                        )
                    ),
                    vol.Required(
                        CONF_TARIFF,
                        default="Tarifa 1",
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=TARIFFS,
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Required(
                        CONF_START_DATE,
                    ): selector.DateSelector(),
                    vol.Required(
                        CONF_PERIOD_DAYS,
                        default=60,
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=365,
                            mode=selector.NumberSelectorMode.BOX,
                        )
                    ),
                }
            ),
        )
