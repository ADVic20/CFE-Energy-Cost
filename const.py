"""Constants for CFE Energy Cost."""

from __future__ import annotations

DOMAIN = "cfe_energy_cost"

NAME = "CFE Energy Cost"

VERSION = "1.0.0-alpha1"

MANUFACTURER = "ADVic20"

DEFAULT_UPDATE_INTERVAL = 60

DEFAULT_PERIOD_DAYS = 60

STORAGE_VERSION = 1

STORAGE_KEY = DOMAIN

CONF_MAIN_SENSOR = "main_sensor"

CONF_DEVICE_SENSORS = "device_sensors"

CONF_TARIFF = "tariff"

CONF_START_DATE = "start_date"

CONF_PERIOD_DAYS = "period_days"

CONF_CATEGORIES = "categories"

ATTR_COST = "cost"

ATTR_CONSUMPTION = "consumption"

ATTR_PERIOD = "period"

ATTR_CATEGORY = "category"
