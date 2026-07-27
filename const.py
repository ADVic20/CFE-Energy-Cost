from __future__ import annotations


#
# Dominio
#

DOMAIN = "cfe_energy_cost"





#
# Configuración general
#

CONF_NAME = "name"

CONF_TARIFF = "tariff"

CONF_REGION = "region"

CONF_CYCLE = "cycle"





#
# Sensor principal de energía
#

CONF_ENERGY_SENSOR = "energy_sensor"





#
# Fechas del recibo CFE
#

# Fecha de corte del usuario

CONF_START_DATE = "start_date"


# Inicio y fin del periodo facturado

CONF_PERIOD_START = "period_start"

CONF_PERIOD_END = "period_end"





#
# Lecturas del medidor
#

CONF_PREVIOUS_READING = "previous_reading"

CONF_CURRENT_READING = "current_reading"





#
# Cargos CFE
#

CONF_IVA = "iva"

CONF_DAP = "dap"





#
# Funciones adicionales
#

CONF_DASHBOARD = "dashboard"

CONF_HISTORY = "history"

CONF_REPORTS = "reports"

CONF_EXCEL = "excel"

CONF_PDF = "pdf"

CONF_NOTIFICATIONS = "notifications"


# Consumo desconocido

CONF_UNKNOWN = "unknown_consumption"





#
# Subdispositivos / submedidores
#

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





#
# Historial
#

CONF_HISTORY_LIMIT = "history_limit"





#
# Defaults
#

DEFAULT_NAME = "CFE Principal"

DEFAULT_TARIFF = "1C"

DEFAULT_REGION = "norte"

DEFAULT_CYCLE = "bimonthly"





#
# Tarifas disponibles
#

TARIFFS = [

    "1",

    "1A",

    "1B",

    "1C",

    "DAC"

]





#
# Regiones disponibles
#

REGIONS = [

    "norte",

    "centro",

    "sur"

]





#
# Sensores internos
#

SENSOR_CONSUMPTION = "consumption"

SENSOR_ENERGY_COST = "energy_cost"

SENSOR_IVA = "iva"

SENSOR_DAP = "dap"

SENSOR_TOTAL = "total"

SENSOR_UNKNOWN_CONSUMPTION = "unknown_consumption"
