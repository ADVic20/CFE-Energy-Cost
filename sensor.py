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





async def async_setup_entry(
    hass,
    entry,
    async_add_entities
):


    coordinator = hass.data[DOMAIN][
        entry.entry_id
    ][
        "coordinator"
    ]



    entities = [


        CFESensor(
            coordinator,
            "consumption",
            "CFE Consumo",
            "kWh"
        ),



        CFESensor(
            coordinator,
            "energy_cost",
            "CFE Costo Energía",
            "MXN"
        ),



        CFESensor(
            coordinator,
            "iva",
            "CFE IVA",
            "MXN"
        ),



        CFESensor(
            coordinator,
            "dap",
            "CFE DAP",
            "MXN"
        ),



        CFESensor(
            coordinator,
            "total",
            "CFE Recibo Estimado",
            "MXN"
        ),




        CFESensor(
            coordinator,
            "previous_reading",
            "CFE Lectura Anterior",
            "kWh"
        ),



        CFESensor(
            coordinator,
            "current_reading",
            "CFE Lectura Actual",
            "kWh"
        ),




        CFESensor(
            coordinator,
            "days",
            "CFE Días Periodo",
            "días"
        ),



        CFESensor(
            coordinator,
            "tariff",
            "CFE Tarifa",
            None
        ),



        CFESensor(
            coordinator,
            "region",
            "CFE Región",
            None
        ),



        CFESensor(
            coordinator,
            "period_start",
            "CFE Inicio Periodo",
            None
        ),



        CFESensor(
            coordinator,
            "period_end",
            "CFE Fin Periodo",
            None
        ),



        CFESensor(
            coordinator,
            "cut_date",
            "CFE Fecha Corte",
            None
        ),

    ]



    async_add_entities(
        entities
    )








class CFESensor(
    CoordinatorEntity,
    SensorEntity
):


    def __init__(
        self,
        coordinator,
        key,
        name,
        unit
    ):


        super().__init__(
            coordinator
        )


        self.key = key


        self._attr_name = name


        self._attr_unique_id = (
            f"{DOMAIN}_{key}"
        )



        if unit:

            self._attr_native_unit_of_measurement = unit





    @property
    def native_value(
        self
    ):


        if not self.coordinator.data:

            return None



        return self.coordinator.data.get(
            self.key
        )





    @property
    def device_class(
        self
    ):


        if self.key in (
            "consumption",
            "previous_reading",
            "current_reading"
        ):

            return SensorDeviceClass.ENERGY


        if self.key in (
            "energy_cost",
            "iva",
            "dap",
            "total"
        ):

            return SensorDeviceClass.MONETARY



        return None






    @property
    def state_class(
        self
    ):


        if self.key in (
            "consumption",
            "previous_reading",
            "current_reading"
        ):

            return SensorStateClass.TOTAL_INCREASING


        return None
