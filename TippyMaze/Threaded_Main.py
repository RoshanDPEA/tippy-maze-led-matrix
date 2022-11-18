"""
@file main2.0.py Initiates project and controls program flow better than main.py
"""
from time import sleep

# from pidev.stepperutilities import NEMA_17
import RPi.GPIO as GPIO
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus

from hardware.GumBallRelease import GumBallReleaseMotor
from hardware.Joystick import Joystick
from hardware.LidarSensor import LidarSensor
from hardware.Table import *

from threading import Thread
"""
Variables
"""
START_GAME = True
RELEASE_GUMBALL = False
END_GAME = False

"""
Declaration of all objects needed to interface with the hardware
"""
TABLE = Table(x_axis_port=0, y_axis_port=1)
GUMBALL_RELEASE = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=25)
# GEAR_MOTOR= stepper(stepper_type=NEMA_17)

JOYSTICK = Joystick(number=0, ssh_deploy=True)

TOP_RAMP_SENSOR = LidarSensor(port=0, threshold=30)  # first sensor on ramp down
LOWER_RAMP_SENSOR = LidarSensor(port=2, threshold=30)  # second sensor on ramp down

# Button combos should be an array of buttons that need to be pressed to activate, indexed starting at 0
HOME_TABLE_BUTTON_COMBO = [9, 10]
RESET_GAME = [5, 6]

def exit_routine():
    """
    Frees all stepper motors and joins all threads
    :return: None
    """
    TABLE.free_all()
    GUMBALL_RELEASE.free()

    GPIO.cleanup()


def finish_game():

    global END_GAME
    global RELEASE_GUMBALL

    while True:

        #GUMBALL_RELEASE.sensor.refresh_last_read()

        if RELEASE_GUMBALL:
            print("made it")
            RELEASE_GUMBALL = False
            GUMBALL_RELEASE.release_gumball()

        TOP_RAMP_SENSOR.refresh_last_read()
        LOWER_RAMP_SENSOR.refresh_last_read()

        if TOP_RAMP_SENSOR.detected:
            print("Top")
            TOP_RAMP_SENSOR.reset()
            LOWER_RAMP_SENSOR.reset()
            GUMBALL_RELEASE.sensor.reset()
            END_GAME = True

        if LOWER_RAMP_SENSOR.detected:
            print("Bottom")
            TOP_RAMP_SENSOR.reset()
            LOWER_RAMP_SENSOR.reset()
            GUMBALL_RELEASE.sensor.reset()
            END_GAME = True


def reset_game():
    """
    Reset the game upon completion
    :return: None
    """
    global START_GAME
    global END_GAME

    TABLE.home()

    START_GAME = True
    END_GAME = False

def check_button_combos():
    """
    Check all button combos and perform tasks associated with the button combinations
    :return: None
    """
    # if JOYSTICK.button_combo_check(HOME_TABLE_BUTTON_COMBO):
    #     TABLE.home()

    if JOYSTICK.button_combo_check(RESET_GAME):
        reset_game()


if __name__ == '__main__':
    cyprus.initialize()
    reset_game()
    x = Thread(daemon=True, target=finish_game)
    x.start()

    try:
        while True:
            while START_GAME:
                if not cyprus.read_gpio() & 0b0001:
                    sleep(.05)
                    if not cyprus.read_gpio() & 0b0001:
                        print("in")
                        START_GAME = False
                        RELEASE_GUMBALL = True
                        print("out")

            if END_GAME:
                reset_game()

            TABLE.process_movement(x_val=JOYSTICK.get_axis('x'), y_val=JOYSTICK.get_axis('y'))

            check_button_combos()

    except (KeyboardInterrupt, SystemExit):
        exit_routine()  # Prepare for script termination