# sensors.py

from machine import Pin


class SensorBoard:
    def __init__(self, sensor_gpios, led_gpios):
        if len(sensor_gpios) != len(led_gpios):
            raise ValueError(
                "sensor_gpios and led_gpios must have the same length"
            )

        self.sensor_gpios = sensor_gpios
        self.led_gpios = led_gpios
        self.lane_count = len(sensor_gpios)

        self.sensor_pins = [
            Pin(gpio, Pin.IN, Pin.PULL_UP)
            for gpio in sensor_gpios
        ]

        self.led_pins = [
            Pin(gpio, Pin.OUT)
            for gpio in led_gpios
        ]

        self.onboard_led = Pin("LED", Pin.OUT)

    def read_raw_list(self):
        return [
            int(not pin.value())
            for pin in self.sensor_pins
        ]

    def read_raw_dict(self):
        values = self.read_raw_list()

        return {
            str(i + 1): values[i]
            for i in range(self.lane_count)
        }

    def toggle_onboard(self):
        self.onboard_led.toggle()

    def update_lane_leds(
        self,
        stable_states,
        active_lanes,
        blink_state,
        loaded_led_until=None,
        now_seconds=0
    ):
        for i in range(self.lane_count):
            lane = str(i + 1)

            present = stable_states.get(lane, 0)
            active = active_lanes.get(lane, True)

            hold_until = 0
            if loaded_led_until is not None:
                hold_until = loaded_led_until.get(lane, 0)

            if not active:
                self.led_pins[i].value(0)

            elif present == 0:
                # Empty active lane = blink.
                self.led_pins[i].value(1 if blink_state else 0)

            elif present == 1 and now_seconds < hold_until:
                # Recently loaded/recovered = solid ON briefly.
                self.led_pins[i].value(1)

            else:
                # Loaded and stable = OFF.
                self.led_pins[i].value(0)