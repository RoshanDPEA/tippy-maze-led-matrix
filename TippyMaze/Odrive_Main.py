"""
@file main2.0.py Initiates project and controls program flow better than main.py
"""
from time import sleep

import RPi.GPIO as GPIO
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus

from hardware import ODrive_Ease_Lib
from hardware.GumBallRelease import GumBallReleaseMotor
from hardware.Joystick import Joystick
from hardware.LidarSensor import LidarSensor
from hardware.DPEAMotor import DPEAMotor

import odrive
from hardware.move_odrive import *
from hardware.ODrive_Ease_Lib import *

"""
Variables
"""
START_GAME = True

"""
Declaration of all objects needed to interface with the hardware
"""
OD = odrive.find_any()
axis_1 = ODrive_Ease_Lib.ODrive_Axis(OD.axis1)
axis_0 = ODrive_Ease_Lib.ODrive_Axis(OD.axis0)
ODRIVE = move_odrive(axis_0, axis_1, 200000, 32, 140000)

GUMBALL_RELEASE = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=25)
dpea_motor = DPEAMotor(motor_port=2)

JOYSTICK = Joystick(number=0, ssh_deploy=True)
TOP_RAMP_SENSOR = LidarSensor(port=0, threshold=30)  # first sensor on ramp down
LOWER_RAMP_SENSOR = LidarSensor(port=2, threshold=30)  # second sensor on ramp down

# Button combos should be an array of buttons that need to be pressed to activate, indexed starting at 0
HOME_TABLE_BUTTON_COMBO = [9, 10]
RESET_GAME = [5, 6]


def exit_routine():
    """
    Frees all stepper motors, set odrives to idle state, and joins all threads
    :return: None
    """
    axis_1.idle()
    axis_0.idle()
    GUMBALL_RELEASE.free()
    dpea_motor.motor.free()

    GPIO.cleanup()


def finish_game():
    """
    Checks sensors to see if gumball has made it to the end of the maze
    :return: None
    """
    TOP_RAMP_SENSOR.refresh_last_read()
    sleep(.05)
    LOWER_RAMP_SENSOR.refresh_last_read()
    sleep(.05)

    if TOP_RAMP_SENSOR.detected:
        print("Top")
        reset_game()

    if LOWER_RAMP_SENSOR.detected:
        print("Bottom")
        reset_game()


def reset_game():
    """
    Reset the game upon completion
    :return: None
    """
    global START_GAME

    ODRIVE.trajectory_mode(74000, 71000)

    TOP_RAMP_SENSOR.reset()
    LOWER_RAMP_SENSOR.reset()
    GUMBALL_RELEASE.sensor.reset()

    START_GAME = True


def check_button_combos():
    """
    Check all button combos and perform tasks associated with the button combinations
    :return: None
    """

    if JOYSTICK.button_combo_check(RESET_GAME):
        reset_game()

    if JOYSTICK.button_combo_check(HOME_TABLE_BUTTON_COMBO):
        ODRIVE.trajectory_mode(74000, 71000)


if __name__ == '__main__':
    cyprus.initialize()
    ODRIVE.set_up_odrives()
    ODRIVE.home()
    reset_game()
    GUMBALL_RELEASE.motor.set_limit_hardstop(False)

    try:
        while True:
            while START_GAME:
                if GUMBALL_RELEASE.motor.read_switch() == 1:
                    sleep(.05)
                    if GUMBALL_RELEASE.motor.read_switch() == 1:
                        print("in")
                        START_GAME = False
                        GUMBALL_RELEASE.release_gumball()
                        print("out")

            finish_game()

            ODRIVE.run_axis_1()  # x-axis
            ODRIVE.run_axis_0()  # y-axis

           # check_button_combos()

    except (KeyboardInterrupt, SystemExit):
        exit_routine()  # Prepare for script termination
