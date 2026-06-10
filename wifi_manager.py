# wifi_manager.py

import network
import time
import ujson as json

import config


def load_profiles():
    try:
        with open(config.WIFI_PROFILES_FILE, "r") as f:
            data = json.load(f)

            return data.get("profiles", [])

    except Exception:
        return []


def save_profiles(profiles):
    with open(config.WIFI_PROFILES_FILE, "w") as f:
        json.dump(
            {"profiles": profiles},
            f
        )


def save_or_update_profile(
    ssid,
    password,
    priority=10
):
    profiles = load_profiles()

    updated = False

    for profile in profiles:

        if profile.get("ssid") == ssid:
            profile["password"] = password
            profile["priority"] = priority

            updated = True
            break

    if not updated:
        profiles.append({
            "ssid": ssid,
            "password": password,
            "priority": priority
        })

    profiles.sort(
        key=lambda p: p.get("priority", 999)
    )

    save_profiles(profiles)


def station_ip():
    wlan = network.WLAN(network.STA_IF)

    if wlan.active() and wlan.isconnected():
        return wlan.ifconfig()[0]

    return None


def ap_ip():
    access_point = network.WLAN(network.AP_IF)

    if access_point.active():
        return access_point.ifconfig()[0]

    return None


def connect_to_wifi(
    ssid,
    password,
    timeout=15
):
    wlan = network.WLAN(network.STA_IF)

    try:
        wlan.active(False)
        time.sleep(1)

        wlan.active(True)
        time.sleep(1)

    except Exception:
        pass

    try:
        wlan.disconnect()

    except Exception:
        pass

    try:
        wlan.connect(ssid, password)

    except Exception as e:
        return False, str(e)

    start = time.time()

    while time.time() - start < timeout:

        if wlan.isconnected():
            return True, wlan.ifconfig()[0]

        time.sleep(1)

    return False, "timeout"


def try_saved_profiles(timeout=15):
    profiles = load_profiles()

    if not profiles:
        return False, "no saved profiles"

    profiles.sort(
        key=lambda p: p.get("priority", 999)
    )

    for profile in profiles:

        ssid = profile.get("ssid")
        password = profile.get("password", "")

        if not ssid:
            continue

        ok, info = connect_to_wifi(
            ssid,
            password,
            timeout=timeout
        )

        if ok:
            return True, ssid

    return False, "saved profiles failed"


def start_ap():
    access_point = network.WLAN(network.AP_IF)

    access_point.active(True)

    try:
        access_point.config(
            essid=config.AP_SSID,
            password=config.AP_PASSWORD,
            authmode=3
        )

    except Exception:
        access_point.config(
            essid=config.AP_SSID
        )

    return access_point


def stop_ap():
    network.WLAN(network.AP_IF).active(False)


def disconnect_station():
    try:
        network.WLAN(network.STA_IF).disconnect()

    except Exception:
        pass