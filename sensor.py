from __future__ import annotations


from homeassistant.components.sensor import (
    SensorEntity
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity
)


from .const import DOMAIN



async def async_setup_entry(
    hass,
    entry,
    async_add_entities
):


    data = hass.data[DOMAIN][
        entry.entry_id
    ]


    coordinator = data[
        "coordinator"
    ]


    async_add_entities(

        [

            CFEConsumptionSensor(
                coordinator
            ),

            CFEEnergyCostSensor(
                coordinator
            ),

            CFEIVASensor(
                coordinator
            ),

            CFEDAPSensor(
                coordinator
            ),

            CFETotalSensor(
                coordinator
            ),

            CFETariffSensor(
                coordinator
            )

        ]

    )



class CFEBaseSensor(
    CoordinatorEntity,
    SensorEntity
):


    def __init__(
        self,
        coordinator,
        name,
        key
    ):

        super().__init__(
            coordinator
        )


        self._attr_name = (
            f"CFE {name}"
        )

        self.key = key


        self._attr_unique_id = (
            f"{DOMAIN}_{key}"
        )


    @property
    def native_value(
        self
    ):

        return (
            self.coordinator
            .data
            .get(
                self.key
            )
        )



class CFEConsumptionSensor(
    CFEBaseSensor
):


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator,
            "Consumo",
            "energy"
        )


    @property
    def native_unit_of_measurement(
        self
    ):

        return "kWh"



class CFEEnergyCostSensor(
    CFEBaseSensor
):


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator,
            "Costo Energía",
            "energy_cost"
        )


    @property
    def native_unit_of_measurement(
        self
    ):

        return "MXN"



class CFEIVASensor(
    CFEBaseSensor
):


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator,
            "IVA",
            "iva"
        )


    @property
    def native_unit_of_measurement(
        self
    ):

        return "MXN"



class CFEDAPSensor(
    CFEBaseSensor
):


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator,
            "DAP",
            "dap"
        )


    @property
    def native_unit_of_measurement(
        self
    ):

        return "MXN"



class CFETotalSensor(
    CFEBaseSensor
):


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator,
            "Recibo Estimado",
            "total"
        )


    @property
    def native_unit_of_measurement(
        self
    ):

        return "MXN"



class CFETariffSensor(
    CFEBaseSensor
):


    def __init__(
        self,
        coordinator
    ):

        super().__init__(
            coordinator,
            "Tarifa",
            "tariff"
        )
