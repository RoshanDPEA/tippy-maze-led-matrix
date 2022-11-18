"""
@file gumball_release_lidar_test.py This file is used to run the gumball release motor until a gumball release
    has been detected by the attached lidar sensor
"""
from hardware.GumBallRelease import GumBallReleaseMotor

SENSOR_THRESHOLD = 35

# TODO sometimes at start a detected event occurrs, the threshold may need to be adjusted
gumball_release_motor = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=SENSOR_THRESHOLD)
gumball_release_motor.sensor.refresh_last_read()
gumball_release_motor.sensor.reset()

def exit_routine():
    gumball_release_motor.motor.hard_stop()
    gumball_release_motor.free()

try:
    gumball_release_motor.release_gumball()  # Run the motor until a gumball has been detected 

except KeyboardInterrupt:  # Handle a keyboard interrupt while releasing a gumball
    print("Keyboard interrupt")  # Signal keyboard interrupt and cleanup
    exit_routine()

print("Complete")  # Signal script completion and clean up
exit_routine()