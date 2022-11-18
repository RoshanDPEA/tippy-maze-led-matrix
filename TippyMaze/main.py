"""
@file main.py Initiates project and controls program flow
"""
from threading import Thread
from time import sleep

import RPi.GPIO as GPIO
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus

from hardware.CoinAcceptor import CoinAcceptor

from hardware.GumBallRelease import GumBallReleaseMotor
from hardware.Joystick import Joystick
from hardware.LidarSensor import LidarSensor
from hardware.Table import *

"""
Variables needed to keep track of various states, control program flow
"""
REQUIRE_MONEY = False
KEEP_THREADS_ALIVE = True  # Boolean to determine whether to keep threads alive
REFRESH_RAMP_SENSORS = True
GAME_COMPLETE = False

# Array to hold the last read values from the joystick
LAST_READ = [0.0, 0.0]

# Button combos should be an array of buttons that need to be pressed to activate, indexed starting at 0
HOME_TABLE_BUTTON_COMBO = [0, 3]
REQUIRE_MONEY_BUTTON_COMBO = [0, 4]
RESET_GAME = [7, 8]

"""
Declaration of all objects needed to interface with the hardware
"""
TABLE = Table(x_axis_port=0, y_axis_port=1)
GUMBALL_RELEASE = GumBallReleaseMotor(motor_port=3, sensor_port=4, sensor_threshold=40)

JOYSTICK = Joystick(number=0, ssh_deploy=True)
# COIN_ACCEPTOR = CoinAcceptor(required_amt=25)

TOP_RAMP_SENSOR = LidarSensor(port=0, threshold=25)  # first sensor on ramp down
LOWER_RAMP_SENSOR = LidarSensor(port=2, threshold=10)  # second sensor on ramp down


def game_complete_check():
    """
    Constantly check to see if either ramp lidar sensors have detected a gumball pass
    :return: None
    """
    global GAME_COMPLETE

    while KEEP_THREADS_ALIVE:
        # if either sensor has detected an object going by reset the game
        if TOP_RAMP_SENSOR.detected or LOWER_RAMP_SENSOR.detected:
            GAME_COMPLETE = True


"""
def check_coin_acceptor():
    
    Method to check the coin acceptor for new input
    :return:
   
    while KEEP_THREADS_ALIVE:
        COIN_ACCEPTOR.get_coin_input()
        sleep(0.1)
"""


def exit_routine():
    """
    Frees all stepper motors, closes serial connection with coin acceptor, joins all threads
    :return: None
    """
    global KEEP_THREADS_ALIVE
    KEEP_THREADS_ALIVE = False

    TABLE.free_all()
    GUMBALL_RELEASE.free()

    # COIN_ACCEPTOR.close_serial_connection()

    GPIO.cleanup()


def handle_game():
    """
    Get the joystick position and determine if it has been moved or not.
    Request table movement if a new position has been detected
    :return:
    """
    global LAST_READ

    pos_x = JOYSTICK.get_axis('x')
    pos_y = JOYSTICK.get_axis('y')

    if pos_x != LAST_READ[0] or pos_y != LAST_READ[1]:
        if pos_x or pos_y != 0:  # ignore "new" pos in center
            LAST_READ = [pos_x, pos_y]
            TABLE.process_movement(x_val=pos_x, y_val=pos_y)


def reset_game():
    """
    Reset the game upon completion
    :return: None
    """
    global GAME_COMPLETE

    TABLE.home()

    TOP_RAMP_SENSOR.reset()
    LOWER_RAMP_SENSOR.reset()
    GUMBALL_RELEASE.sensor.reset()

    GUMBALL_RELEASE.release_gumball()
    # COIN_ACCEPTOR.reset_amount_inputted()

    GAME_COMPLETE = False


def check_button_combos():
    """
    Check all button combos and perform tasks associated with the button combinations
    :return: Array of triggered button combos homing combo="home", money combo="money", reset game combo ="reset"
    """
    global REQUIRE_MONEY
    triggered = []

    if JOYSTICK.button_combo_check(HOME_TABLE_BUTTON_COMBO):
        TABLE.home()

        while TABLE.check_movements():  # wait for homing to finish
            continue
        triggered.append("home")

    if JOYSTICK.button_combo_check(RESET_GAME):
        reset_game()
        triggered.append("reset")

    return triggered


if __name__ == "__main__":
    # TODO determine if this thread is still necessary
    GAME_COMPLETE_CHECK = Thread(target=game_complete_check,daemon=True)

    reset_game()  # Begin game

    GAME_COMPLETE_CHECK.start()

    try:
        while True:

            check_button_combos()

            TOP_RAMP_SENSOR.refresh_last_read()
            LOWER_RAMP_SENSOR.refresh_last_read()

            if GAME_COMPLETE:
                reset_game()

            """
            if REQUIRE_MONEY:  # If the game has been set to require money
                while COIN_ACCEPTOR.amount_inputted < COIN_ACCEPTOR.required_amount:  # wait for enough money
                    COIN_ACCEPTOR.get_coin_input()
                    # Check to see if the user changes the requirement
                    if "money" in check_button_combos():
                        break
                    continue
            """
            handle_game()  # Filter joystick input and request table movement

    except (KeyboardInterrupt, SystemExit):
        exit_routine()  # Prepare for script termination
