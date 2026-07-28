from __future__ import annotations

from homeassistant.components.button import (
    ButtonEntity,
)

from homeassistant.helpers.entity import (
    EntityCategory,
)

from .const import DOMAIN


async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    async_add_entities(

        [

            CFENewPeriodButton(
                coordinator
            )

        ]

    )


class CFENewPeriodButton(
    ButtonEntity
):

    _attr_icon = "mdi:file-refresh"

    _attr_entity_category = (
        EntityCategory.CONFIG
    )

    def __init__(
        self,
        coordinator,
    ):

        self.coordinator = coordinator

        self._attr_name = (
            "CFE Nuevo Periodo"
        )

        self._attr_unique_id = (

            f"{DOMAIN}_"

            f"{coordinator.entry_id}"

            "_new_period"

        )

    async def async_press(
        self,
    ):

        await self.coordinator.async_start_new_period()

        await self.coordinator.async_request_refresh()
