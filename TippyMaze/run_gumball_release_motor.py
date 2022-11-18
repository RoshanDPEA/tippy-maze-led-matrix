"""
@file run_gumball_release_motor.py This file is intended to simply run the gumball release
motor indefinitely.
"""
from hardware.GumBallRelease import GumBallReleaseMotor, GUMBALL_MOTOR_SETTINGS

release_motor = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=35)

if __name__ == "__main__":
    release_motor.sensor.reset()
    try:
        release_motor.release_gumball()


    except KeyboardInterrupt:
        print("exiting")
        release_motor.motor.stop()
        release_motor.motor.free()
