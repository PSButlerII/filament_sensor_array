# active_lanes.py

import ujson as json


FILE_NAME = "active_lanes.json"


def default_lanes(lane_count):
    return {
        str(i): True
        for i in range(1, lane_count + 1)
    }


def normalize_lanes(data, lane_count):
    normalized = default_lanes(lane_count)

    if not isinstance(data, dict):
        return normalized

    for i in range(1, lane_count + 1):
        key = str(i)

        if key in data:
            normalized[key] = bool(data[key])

    return normalized


def load(lane_count):
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)

        return normalize_lanes(data, lane_count)

    except Exception:
        return default_lanes(lane_count)


def save(active_lanes, lane_count):
    normalized = normalize_lanes(active_lanes, lane_count)

    with open(FILE_NAME, "w") as f:
        json.dump(normalized, f)

    return normalized