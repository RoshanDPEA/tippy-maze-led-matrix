"""
@file ramp_sensors_test.py This file is responsible for testing the functionality of the ramp Lidar Sensors
"""
from hardware.LidarSensor import LidarSensor
from threading import Thread

TOP_RAMP_SENSOR = LidarSensor(port=0, threshold=40)  # first sensor on ramp down
LOWER_RAMP_SENSOR = LidarSensor(port=2, threshold=40)  # second sensor on ramp down
RAMP_SENSORS = [TOP_RAMP_SENSOR, LOWER_RAMP_SENSOR]  # List of instantiated ramp sensors
GUMBALL_DETECTED_EVENT = False


def check_ramp_sensors() -> None:
    """
    Check all ramp sensors if any have detected a gumball passing over.
    This function is intended to be used in a thread as it will block code execution
    :return: None
    """
    global GUMBALL_DETECTED_EVENT

    while True:
        refresh_ramp_sensors()
        if any(sensor.detected for sensor in RAMP_SENSORS):
            GUMBALL_DETECTED_EVENT = True


def refresh_ramp_sensors() -> None:
    """
    Refresh all ramp sensors last read value
    :return: None
    """
    for sensor in RAMP_SENSORS:
        sensor.refresh_last_read()


def reset_ramp_sensors() -> None:
    """
    Reset all of the ramp sensors
    :return: None
    """
    for sensor in RAMP_SENSORS:
        sensor.reset()


if __name__ == "__main__":
    global GUMBALL_DETECTED_EVENT
    check_ramp_sensors_thread = Thread(target=check_ramp_sensors(), daemon=True)
    check_ramp_sensors_thread.start()

    try:
        if GUMBALL_DETECTED_EVENT:
            print("Detected a gumball pass")
            GUMBALL_DETECTED_EVENT = False
    except KeyboardInterrupt:
        exit(0)
