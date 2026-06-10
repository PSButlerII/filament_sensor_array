# main.py
from time import localtime, time
import uasyncio as asyncio
import ujson as json

import config
import wifi_manager
from sensors import SensorBoard
from state import SpoolState
from http_server import TinyHttpServer
import active_lanes


def iso_timestamp():
    t = localtime()
    return "%04d-%02d-%02dT%02d:%02d:%02d" % (
        t[0], t[1], t[2], t[3], t[4], t[5]
    )


board = SensorBoard(config.SENSOR_GPIOS, config.LED_GPIOS)

spool_state = SpoolState(
    lane_count=board.lane_count,
    debounce_ms=config.DEBOUNCE_MS,
    bad_switch_window_sec=config.BAD_SWITCH_WINDOW_SEC,
    bad_switch_toggle_limit=config.BAD_SWITCH_TOGGLE_LIMIT,
    max_events=config.MAX_EVENTS,
    loaded_led_hold_seconds=config.LOADED_LED_HOLD_SECONDS
)

saved_active_lanes = active_lanes.load(board.lane_count)
spool_state.set_active_lanes(saved_active_lanes)

network_mode = "boot"
connected_ssid = None
ip_address = None
blink_state = False
latest_dashboard_json = "{}"


def device_info():
    return {
        "name": config.DEVICE_NAME,
        "lane_count": board.lane_count,
        "sensor_gpios": config.SENSOR_GPIOS,
        "led_gpios": config.LED_GPIOS,
        "network_mode": network_mode,
        "connected_ssid": connected_ssid,
        "ip": ip_address,
        "dashboard_refresh_ms": config.DASHBOARD_REFRESH_MS
    }

def rebuild_dashboard_json():
    global latest_dashboard_json
    latest_dashboard_json = json.dumps(
        spool_state.payload(device_info())
    )

def get_dashboard_json():
    return latest_dashboard_json

def get_alert_json():
    payload = {
        "ok": True,
        "alerts": spool_state.alerts,
        "bad_switches": spool_state.bad_switches,
        "active_lanes": spool_state.active_lanes,
        "timestamp": spool_state.updated_at,
        "should_pause": bool(spool_state.alerts),
        "message": "No active alerts"
    }

    if spool_state.alerts:
        payload["message"] = "Empty active lane(s): " + ", ".join(
            [str(x) for x in spool_state.alerts]
        )

    elif spool_state.bad_switches:
        payload["message"] = "Bad switch suspected: " + ", ".join(
            [str(x) for x in spool_state.bad_switches]
        )

    return json.dumps(payload)

def save_wifi_profile_from_api(data):
    ssid = data.get("ssid")
    password = data.get("password", "")
    priority = data.get("priority", 10)

    if not ssid:
        return {
            "ok": False,
            "message": "ssid is required"
        }

    wifi_manager.save_or_update_profile(ssid, password, priority)

    return {
        "ok": True,
        "ssid": ssid,
        "priority": priority,
        "message": "saved; power-cycle to connect"
    }

def save_active_lanes_from_api(data):
    lanes = data.get("active_lanes")

    if not isinstance(lanes, dict):
        return {
            "ok": False,
            "message": "active_lanes object required"
        }

    saved = active_lanes.save(
        lanes,
        board.lane_count
    )

    spool_state.set_active_lanes(saved)
    rebuild_dashboard_json()

    return {
        "ok": True,
        "active_lanes": saved,
        "message": "active lanes saved"
    }

async def monitor_task():
    global blink_state

    last_json_update = 0

    while True:
        blink_state = not blink_state
        board.toggle_onboard()

        raw = board.read_raw_dict()
        now_text = iso_timestamp()
        now_seconds = time()

        spool_state.update(raw, now_text, now_seconds)
        board.update_lane_leds(
            spool_state.stable_states,
            spool_state.active_lanes,
            blink_state,
            spool_state.loaded_led_until,
            now_seconds
        )

        current_ms = int(now_seconds * 1000)

        if current_ms - last_json_update >= config.DASHBOARD_JSON_INTERVAL_MS:
            rebuild_dashboard_json()
            last_json_update = current_ms

        await asyncio.sleep_ms(config.MONITOR_INTERVAL_MS)

def start_network():
    global network_mode, connected_ssid, ip_address

    print("Trying saved Wi-Fi profiles...")
    ok, info = wifi_manager.try_saved_profiles(timeout=15)

    if ok:
        network_mode = "station"
        connected_ssid = info
        ip_address = wifi_manager.station_ip()
        wifi_manager.stop_ap()

        print("Connected to:", connected_ssid)
        print("IP:", ip_address)

    else:
        print("Wi-Fi connect failed:", info)
        print("Starting AP fallback...")

        wifi_manager.start_ap()

        network_mode = "ap"
        connected_ssid = None
        ip_address = wifi_manager.ap_ip()

        print("AP SSID:", config.AP_SSID)
        print("AP IP:", ip_address)

async def main():
    print("Pico Spool Monitor v2 Phase 3 starting")
    print("Lanes:", board.lane_count)

    start_network()
    rebuild_dashboard_json()

    server = TinyHttpServer(
        get_dashboard_json=get_dashboard_json,
        get_alert_json=get_alert_json,
        save_wifi_profile=save_wifi_profile_from_api,
        save_active_lanes=save_active_lanes_from_api
    )

    asyncio.create_task(monitor_task())

    print("Starting tiny dashboard server on 0.0.0.0:%s" % config.API_PORT)

    await server.start(config.API_PORT)

    while True:
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()