DOMAIN = "cfe_energy_cost"


# Config general

CONF_NAME = "name"
CONF_TARIFF = "tariff"
CONF_REGION = "region"


# Energy meter

CONF_ENERGY_SENSOR = "energy_sensor"


# Billing

CONF_BILLING = "billing"
CONF_START_DATE = "start_date"
CONF_CYCLE = "cycle"


# Datos del recibo CFE

CONF_PERIOD_START = "period_start"
CONF_PERIOD_END = "period_end"

CONF_PREVIOUS_READING = "previous_reading"
CONF_CURRENT_READING = "current_reading"



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

DEFAULT_NAME = "CFE Principal"

DEFAULT_TARIFF = "1C"

DEFAULT_REGION = "Norte"

DEFAULT_CYCLE = "bimonthly"
