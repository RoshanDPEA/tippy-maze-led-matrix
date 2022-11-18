from time import sleep

import odrive

from hardware import ODrive_Ease_Lib
from hardware.move_odrive import *
from hardware.ODrive_Ease_Lib import *
from hardware.Joystick import Joystick
from hardware.DPEAMotor import DPEAMotor

JOYSTICK = Joystick(number=0, ssh_deploy=True)
dpea_motor = DPEAMotor(motor_port=2)

OD = odrive.find_any()
axis_1 = ODrive_Ease_Lib.ODrive_Axis(OD.axis1)
axis_0 = ODrive_Ease_Lib.ODrive_Axis(OD.axis0)
ODRIVE = move_odrive(axis_0, axis_1, 200000, 28, 140000)

if __name__ == "__main__":
    ODRIVE.set_up_odrives()
    ODRIVE.home()
    switch = True
    try:
        while True:
            ODRIVE.run_axis_0()
            ODRIVE.run_axis_1()

            if JOYSTICK.button_combo_check([1]):
                ODRIVE.trajectory_mode(74000, 71000)

            if JOYSTICK.button_combo_check([0]):
                if switch:
                    dpea_motor.motor.run(1, 50)
                    switch = False
                else:
                    dpea_motor.motor.stop()
                    switch = True


    except KeyboardInterrupt:
        ODRIVE.axis_1.idle()
        ODRIVE.axis_0.idle()
        quit()
