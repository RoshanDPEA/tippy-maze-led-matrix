"""
This file is intended to be used to determine the threshold of a Lidar Sensor
for accurate object detection
"""
from hardware.LidarSensor import LidarSensor

sensor = LidarSensor(port=2, threshold=30)

sensor.refresh_last_read()
sensor.reset()

try:
    while True:
        print(sensor.distance())

        sensor.refresh_last_read()

        # if sensor.detected_object():
        #     print("detected jawbreaker")
        #     break
except (KeyboardInterrupt, SystemExit):
    quit()
