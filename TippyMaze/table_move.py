"""
@file table_move.py This file is used to exclusively move the table based off joystick input.
 Primarily intended for demonstrating the smooth table movements.
"""
from time import sleep
from hardware.Joystick import Joystick
from hardware.Table import Table
from hardware.Table import AXIS_MOTOR_SETTINGS
# pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
# from Slush.Devices import L6470Registers


# Instantiate table and joystick
table = Table(x_axis_port=0, y_axis_port=1)
joystick_1 = Joystick(number=0, ssh_deploy=True)  # original joystick (mounted to project)
HOME_TABLE_BUTTON_COMBO = [8]
MOVE_TABLE_BUTTON_COMBO = [9]
GET_OUT_BUTTON_COMBO = [7]
in_while = [5]
out_while = [6]

def send():
    """
    Run the table with relative moves only
    :return: None
    """
    joystick_1.refresh()
    table.use_relative_move(x_val=joystick_1.joystick.get_axis(0), y_val=joystick_1.joystick.get_axis(1))

def run_with_one_joystick():
    """
    Run the table using one joystick.
    Will use both axes on the joystick to control the table
    :return: None
    """
    joystick_1.refresh()
    table.process_movement(x_val=joystick_1.joystick.get_axis(0), y_val=joystick_1.joystick.get_axis(1))
    #table.process_movement(x_val=joystick_1.get_axis('x'), y_val=joystick_1.get_axis('y'))
    #table.process_movement(x_val=joystick_1.get_axis('x') / 4.25, y_val=joystick_1.get_axis('y') / 4.25)


def run_two_joysticks():
    """
    For two joystick mode joystick 2 should be positioned orthogonal to joystick 1.
    Joystick 1 controls the tables x axis.
    Joystick 2 controls the tables y axis but its value needs to be flipped.
    :return: None
    """
    joystick_2 = Joystick(number=1, ssh_deploy=True)  # Second joystick, used when in two joystick mode
    table.process_movement(x_val=joystick_1.get_axis('x'), y_val=-joystick_2.get_axis('x'))


if __name__ == "__main__":
    table.home()
    # AXIS_MOTOR_SETTINGS['output_max'] = table.calculate_out_max()

    try:
        while True:  # Move the table indefinitely
            # run_two_joysticks()

            # if cyprus.read_gpio() & 0b1000:
            #     pass
            # else:
            #     table.home()
            # if joystick_1.button_combo_check(HOME_TABLE_BUTTON_COMBO):
            #     table.home()

            run_with_one_joystick()

            #send()

            if joystick_1.button_combo_check(MOVE_TABLE_BUTTON_COMBO):
                while True:
                    table.process_movement(0,-1)
                    sleep(2)
                    table.process_movement(0,1)
                    sleep(2)
                    if joystick_1.button_combo_check(GET_OUT_BUTTON_COMBO):
                        break
            if joystick_1.button_combo_check([10]):
                while True:
                    table.process_movement(-1,0)
                    sleep(2)
                    table.process_movement(1,0)
                    sleep(2)
                    if joystick_1.button_combo_check(GET_OUT_BUTTON_COMBO):
                        break

            if joystick_1.button_combo_check(HOME_TABLE_BUTTON_COMBO):
                table.home()

    except KeyboardInterrupt:  # Gracefully stop script execution from a KeyboardInterrupt
        table.free_all()
        quit()
