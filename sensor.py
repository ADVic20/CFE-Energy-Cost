from __future__ import annotations


from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)


from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)


from .const import DOMAIN



SENSORS = [

    ("consumption", "CFE Consumo", "kWh"),

    ("energy_cost", "CFE Costo Energía", "MXN"),

    ("iva", "CFE IVA", "MXN"),

    ("dap", "CFE DAP", "MXN"),

    ("total", "CFE Recibo Estimado", "MXN"),

    ("loads_kwh", "CFE Cargas Estimadas", "kWh"),

]




async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):


    coordinator = hass.data[DOMAIN][
        entry.entry_id
    ][
        "coordinator"
    ]



    entities = []


    # Sensores principales

    for key, name, unit in SENSORS:

        entities.append(

            CFESensor(
                coordinator,
                key,
                name,
                unit
            )

        )



    # Sensores individuales de cargas

    for load_name in coordinator.loads.loads:


        entities.append(

            CFELoadSensor(

                coordinator,

                load_name

            )

        )



    async_add_entities(
        entities
    )





class CFESensor(
    CoordinatorEntity,
    SensorEntity,
):


    def __init__(
        self,
        coordinator,
        key,
        name,
        unit,
    ):


        super().__init__(
            coordinator
        )


        self.key = key


        self._attr_name = name


        self._attr_unique_id = (

            f"{DOMAIN}_"
            f"{coordinator.entry_id}_"
            f"{key}"

        )


        self._attr_native_unit_of_measurement = unit




    @property
    def native_value(
        self
    ):


        return self.coordinator.data.get(
            self.key
        )



    @property
    def device_class(
        self
    ):


        if self.key in (

            "consumption",

            "loads_kwh",

        ):

            return SensorDeviceClass.ENERGY



        if self.key in (

            "energy_cost",

            "iva",

            "dap
