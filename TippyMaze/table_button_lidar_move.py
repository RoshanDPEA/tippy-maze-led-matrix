"""
@file table_move.py This file is used to exclusively move the table based off joystick input.
 Primarily intended for demonstrating the smooth table movements.
"""
from hardware.Joystick import Joystick
from hardware.Table import Table
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from Slush.Devices import L6470Registers


# Instantiate table and joystick
table = Table(x_axis_port=0, y_axis_port=1)
joystick_1 = Joystick(number=0, ssh_deploy=True)  # original joystick (mounted to project)
HOME_TABLE_BUTTON_COMBO = [0, 2]

def run_with_one_joystick():
    """
    Run the table using one joystick.
    Will use both axes on the joystick to control the table
    :return: None
    """
    table.process_movement(x_val=joystick_1.get_axis('x'), y_val=joystick_1.get_axis('y'))


def run_two_joysticks():
    """
    For two joystick mode joystick 2 should be positioned orthogonal to joystick 1.
    Joystick 1 controls the tables x axis.
    Joystick 2 controls the tables y axis but its value needs to be flipped.
    :return: None
    """
    joystick_2 = Joystick(number=1, ssh_deploy=True)  # Second joystick, used when in two joystick mode
    table.process_movement(x_val=joystick_1.get_axis('y'), y_val=joystick_2.get_axis('y'))


if __name__ == "__main__":
    table.home()
    cyprus.initialize()

    try:
        while True:  # Move the table indefinitely
            #run_two_joysticks()

            if not cyprus.read_gpio() & 0b0001:
                print("clicked")
                table.home()

            # if joystick_1.button_combo_check(HOME_TABLE_BUTTON_COMBO):
            #     table.home()
            run_with_one_joystick()
    except KeyboardInterrupt:  # Gracefully stop script execution from a KeyboardInterrupt
        table.free_all()
        quit()
