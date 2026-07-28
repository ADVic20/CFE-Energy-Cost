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

    ("previous_reading", "CFE Lectura Anterior", "kWh"),

    ("current_reading", "CFE Lectura Actual", "kWh"),

    ("days", "CFE Días del Periodo", "días"),

    ("tariff", "CFE Tarifa", None),

    ("region", "CFE Región", None),

    ("period_start", "CFE Inicio del Periodo", None),

    ("period_end", "CFE Fin del Periodo", None),

    ("cut_date", "CFE Fecha de Corte", None),

    ("unknown_consumption", "CFE Consumo Desconocido", "kWh"),

]



async def async_setup_entry(
    hass,
    entry,
    async_add_entities,
):

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]


    async_add_entities(

        [

            CFESensor(
                coordinator,
                key,
                name,
                unit,
            )

            for key, name, unit in SENSORS

        ]

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

            f"{DOMAIN}_{coordinator.entry_id}_{key}"

        )


        if unit:

            self._attr_native_unit_of_measurement = unit



    @property
    def native_value(self):

        if self.coordinator.data is None:

            return None


        return self.coordinator.data.get(
            self.key
        )



    @property
    def device_class(self):

        if self.key in (

            "consumption",

            "previous_reading",

            "current_reading",

            "unknown_consumption",

        ):

            return SensorDeviceClass.ENERGY



        if self.key in (

            "energy_cost",

            "iva",

            "dap",

            "total",

        ):

            return SensorDeviceClass.MONETARY



        return None



    @property
    def state_class(self):


        if self.key in (

            "consumption",

            "previous_reading",

            "current_reading",

            "unknown_consumption",

        ):

            return SensorStateClass.TOTAL



        if self.key in (

            "energy_cost",

            "iva",

            "dap",

            "total",

        ):

            return SensorStateClass.TOTAL



        return None



    @property
    def extra_state_attributes(self):

        if self.key != "total":

            return None


        return {

            "Bloques":

                self.coordinator.data.get(
                    "blocks",
                    []
                ),


            "Periodo":

                self.coordinator.data.get(
                    "period"
                ),


            "Tarifa":

                self.coordinator.data.get(
                    "tariff"
                ),


            "Región":

                self.coordinator.data.get(
                    "region"
                ),

        }
