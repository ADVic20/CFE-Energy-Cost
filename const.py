DOMAIN = "cfe_energy_cost"


# Config general

CONF_NAME = "name"
CONF_TARIFF = "tariff"
CONF_REGION = "region"


# Energy meter

CONF_ENERGY_SENSOR = "energy_sensor"


# Billing

CONF_BILLING = "billing"
CONF_START_DAY = "start_day"
CONF_CYCLE = "cycle"


# Charges

CONF_IVA = "iva"
CONF_DAP = "dap"


# Features

CONF_DASHBOARD = "dashboard"
CONF_HISTORY = "history"
CONF_REPORTS = "reports"
CONF_EXCEL = "excel"
CONF_PDF = "pdf"
CONF_NOTIFICATIONS = "notifications"
CONF_UNKNOWN = "unknown_consumption"


# Subentries

CONF_DEVICE_NAME = "device_name"
CONF_DEVICE_TYPE = "device_type"
CONF_DEVICE_SENSOR = "device_sensor"


DEVICE_TYPES = [
    "meter",
    "solar",
    "load",
    "ev",
    "other"
]


# Defaults

DEFAULT_NAME = "CFE Casa"

DEFAULT_TARIFF = "DAC"

DEFAULT_REGION = "norte"

DEFAULT_CYCLE = "bimonthly"
