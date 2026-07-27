from __future__ import annotations


from datetime import datetime


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


    coordinator = hass.data[DOMAIN][
        entry.entry_id
    ]["coordinator"]



    sensors = [

        CFESensor(
            coordinator,
            "consumo",
            "CFE Consumo Periodo",
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
            "tariff",
            "CFE Tarifa",
            None
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


    ]



    async_add_entities(
        sensors
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


        self._attr_native_unit_of_measurement = unit


        self._attr_unique_id = (
            f"{DOMAIN}_{key}"
        )





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
    def extra_state_attributes(
        self
    ):


        if not self.coordinator.data:

            return {}



        return {


            "period_start":
            self.coordinator.data.get(
                "period_start"
            ),


            "period_end":
            self.coordinator.data.get(
                "period_end"
            ),


            "previous_reading":
            self.coordinator.data.get(
                "previous_reading"
            ),


            "current_reading":
            self.coordinator.data.get(
                "current_reading"
            )

        }
