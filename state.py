# state.py

import time


class SpoolState:
    def __init__(
        self,
        lane_count,
        debounce_ms=75,
        bad_switch_window_sec=30,
        bad_switch_toggle_limit=8,
        max_events=40,
        loaded_led_hold_seconds=5
    ):
        self.lane_count = lane_count
        self.debounce_ms = debounce_ms

        self.bad_switch_window_sec = bad_switch_window_sec
        self.bad_switch_toggle_limit = bad_switch_toggle_limit

        self.max_events = max_events

        self.loaded_led_hold_seconds = loaded_led_hold_seconds

        self.raw_states = self._lane_dict(1)
        self.stable_states = self._lane_dict(1)

        self.last_change_ms = self._lane_dict(0)

        self.loaded_led_until = self._lane_dict(0)

        self.active_lanes = self._lane_dict(True)

        self.toggle_history = {
            str(i): []
            for i in range(1, lane_count + 1)
        }

        self.events = []

        self.alerts = []
        self.bad_switches = []

        self.updated_at = "not-ready"

    def _lane_dict(self, value):
        return {
            str(i): value
            for i in range(1, self.lane_count + 1)
        }

    def set_active_lanes(self, active_lanes):
        normalized = {}

        for i in range(1, self.lane_count + 1):
            key = str(i)

            normalized[key] = bool(
                active_lanes.get(key, True)
            )

        self.active_lanes = normalized

    def log_event(
        self,
        event_type,
        lane,
        timestamp,
        detail=""
    ):
        self.events.append({
            "type": event_type,
            "lane": lane,
            "time": timestamp,
            "detail": detail
        })

        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]

    def _track_toggle(self, lane, timestamp_seconds):
        history = self.toggle_history[lane]

        history.append(timestamp_seconds)

        cutoff = (
            timestamp_seconds
            - self.bad_switch_window_sec
        )

        while history and history[0] < cutoff:
            history.pop(0)

        return (
            len(history)
            >= self.bad_switch_toggle_limit
        )

    def update(
        self,
        raw_states,
        timestamp,
        timestamp_seconds
    ):
        current_ms = time.ticks_ms()

        for lane, raw_value in raw_states.items():

            if raw_value != self.raw_states[lane]:
                self.raw_states[lane] = raw_value
                self.last_change_ms[lane] = current_ms

            if raw_value != self.stable_states[lane]:

                if (
                    time.ticks_diff(
                        current_ms,
                        self.last_change_ms[lane]
                    ) >= self.debounce_ms
                ):

                    previous = self.stable_states[lane]

                    self.stable_states[lane] = raw_value

                    if self.active_lanes.get(lane, True):

                        if previous == 1 and raw_value == 0:
                            self.log_event(
                                "EMPTY",
                                lane,
                                timestamp
                            )

                        elif previous == 0 and raw_value == 1:
                            self.log_event(
                                "RECOVERED",
                                lane,
                                timestamp
                            )

                            self.loaded_led_until[lane] = (
                                timestamp_seconds
                                + self.loaded_led_hold_seconds
                            )

                    if self._track_toggle(
                        lane,
                        timestamp_seconds
                    ):
                        self.log_event(
                            "BAD_SWITCH",
                            lane,
                            timestamp,
                            "Too many toggles in short window"
                        )

        self.alerts = sorted([
            int(lane)
            for lane, value in self.stable_states.items()
            if value == 0
            and self.active_lanes.get(lane, True)
        ])

        self.bad_switches = sorted([
            int(lane)
            for lane, history in self.toggle_history.items()
            if len(history)
            >= self.bad_switch_toggle_limit
        ])

        self.updated_at = timestamp

    def payload(self, device_info):
        return {
            "device": device_info,

            "state": {
                "spools": self.stable_states,

                "active_lanes": self.active_lanes,

                "alerts": self.alerts,

                "bad_switches": self.bad_switches,

                "timestamp": self.updated_at
            },

            "events": self.events
        }