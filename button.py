from __future__ import annotations


from homeassistant.components.button import ButtonEntity

from homeassistant.helpers.entity import EntityCategory


from .const import DOMAIN



async def async_setup_entry(
    hass,
    entry,
    async_add_entities
):


    data = hass.data[DOMAIN][
        entry.entry_id
    ]


    async_add_entities(
        [
            CFENewPeriodButton(
                data["coordinator"]
            )
        ]
    )




class CFENewPeriodButton(
    ButtonEntity
):


    def __init__(
        self,
        coordinator
    ):

        self.coordinator = coordinator

        self._attr_name = (
            "CFE Nuevo Periodo"
        )

        self._attr_unique_id = (
            "cfe_new_period"
        )

        self._attr_entity_category = (
            EntityCategory.CONFIG
        )



    async def async_press(
        self
    ):

        state = (
            self.coordinator
            .hass
            .states
            .get(
                self.coordinator.energy_sensor
            )
        )


        if state is None:

            return



        meter = float(
            state.state
        )


        from datetime import date


        await self.coordinator.period.async_set_start(
            meter,
            str(date.today())
        )


        await self.coordinator.async_request_refresh()
