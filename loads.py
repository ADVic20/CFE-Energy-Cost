"""Energy loads management for CFE Energy Cost."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EnergyLoad:
    """Represent a monitored electrical load."""

    name: str

    # Entidad de Home Assistant
    entity_id: str

    # Potencia nominal
    power_w: float

    # Tipo de control:
    # switch, climate, sensor, manual
    load_type: str = "switch"

    enabled: bool = True

    # Estado interno
    is_on: bool = False

    started_at: Optional[datetime] = None

    accumulated_seconds: float = 0


    def update_state(self, state: str):
        """Update load state from Home Assistant."""

        now = datetime.now()

        active_states = [
            "on",
            "cooling",
            "heating",
        ]


        if state in active_states:

            if not self.is_on:

                self.is_on = True

                self.started_at = now


        else:

            if self.is_on:

                self.is_on = False

                if self.started_at:

                    self.accumulated_seconds += (
                        now - self.started_at
                    ).total_seconds()

                    self.started_at = None



    @property
    def active_hours(self):

        seconds = self.accumulated_seconds


        if self.is_on and self.started_at:

            seconds += (
                datetime.now()
                -
                self.started_at
            ).total_seconds()


        return seconds / 3600



    @property
    def estimated_kwh(self):

        if not self.enabled:

            return 0


        return (
            self.power_w
            *
            self.active_hours
            /
            1000
        )



class LoadManager:
    """Manage electrical loads."""

    def __init__(self):

        self.loads = {}



    def add_load(
        self,
        load: EnergyLoad
    ):

        self.loads[
            load.entity_id
        ] = load



    def update_load(
        self,
        entity_id,
        state
    ):

        load = self.loads.get(
            entity_id
        )

        if load:

            load.update_state(
                state
            )



    def total_kwh(self):

        return sum(
            load.estimated_kwh
            for load in self.loads.values()
        )
