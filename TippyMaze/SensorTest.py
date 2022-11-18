from time import sleep
from hardware.LidarSensor import LidarSensor
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from hardware.GumBallRelease import GumBallReleaseMotor


GUMBALL_RELEASE = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=25)


sensor = LidarSensor(port=4, threshold=25)  # first sensor on ramp down


if __name__ == '__main__':
    cyprus.initialize()
    sensor.reset()
    sensor.refresh_last_read()

    try:
        while True:
            if GUMBALL_RELEASE.motor.read_switch() == 1:
                sleep(.05)
                if GUMBALL_RELEASE.motor.read_switch() == 1:
                    print("there")
            # print(cyprus.read_gpio() & 0b0010)
            # if not cyprus.read_gpio() & 0b0001:
            #     sleep(.05)
            #     if not cyprus.read_gpio() & 0b0001:
            #         print("made it here")
            # print(sensor.distance())
            # if sensor.detected_object():
            #     break
            # sensor.refresh_last_read()
    except KeyboardInterrupt:
         quit()