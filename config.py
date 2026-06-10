# config.py

DEVICE_NAME = "pico-spool-monitor-v2"


# # Start with 4 lanes while we validate stability.
# SENSOR_GPIOS = [2, 3, 4, 5]
# LED_GPIOS = [6, 7, 8, 9]

# 8-lane option:
SENSOR_GPIOS = [2, 3, 4, 5, 10, 11, 12, 13]
LED_GPIOS = [6, 7, 8, 9, 14, 15, 16, 17]

DEBOUNCE_MS = 75
MONITOR_INTERVAL_MS = 100
DASHBOARD_JSON_INTERVAL_MS = 500
LOADED_LED_HOLD_SECONDS = 5

BAD_SWITCH_WINDOW_SEC = 30
BAD_SWITCH_TOGGLE_LIMIT = 8
MAX_EVENTS = 40

WIFI_PROFILES_FILE = "wifi_profiles.json"

AP_SSID = "PicoSpoolSetup"
AP_PASSWORD = "pico-setup"

API_PORT = 80
DASHBOARD_REFRESH_MS = 5000