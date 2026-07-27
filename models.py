from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class TariffBlock:
    """Representa un bloque tarifario."""

    name: str

    limit: float

    price: float


@dataclass(slots=True)
class DeviceEnergy:

    entity_id: str

    name: str

    energy: float = 0

    cost: float = 0

    category: str | None = None
