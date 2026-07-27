from __future__ import annotations



from homeassistant.components.button import (
    ButtonEntity
)



from homeassistant.helpers.entity import (
    EntityCategory
)



from .const import (

    DOMAIN,

    CONF_PREVIOUS_READING,

    CONF_CURRENT_READING

)







async def async_setup_entry(
    hass,
    entry,
    async_add_entities
):


    async_add_entities(

        [

            CFEPeriodResetButton(
                hass,
                entry
            )

        ]

    )









class CFEPeriodResetButton(
    ButtonEntity
):


    _attr_name = (
        "CFE Nuevo Periodo"
    )


    _attr_icon = (
        "mdi:file-refresh"
    )



    _attr_entity_category = (
        EntityCategory.CONFIG
    )






    def __init__(
        self,
        hass,
        entry
    ):


        self.hass = hass

        self.entry = entry


        self._attr_unique_id = (

            f"{DOMAIN}_new_period_"

            f"{entry.entry_id}"

        )







    async def async_press(
        self
    ):


        data = dict(
            self.entry.data
        )



        current = float(

            data.get(

                CONF_CURRENT_READING,

                0

            )

        )



        data[

            CONF_PREVIOUS_READING

        ] = current




        data[

            CONF_CURRENT_READING

        ] = 0





        self.hass.config_entries.async_update_entry(

            self.entry,

            data=data

        )


        await self.coordinator.async_request_refresh()
