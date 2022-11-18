"""
CoinAcceptor Module for interacting with the Adafruit Coin Acceptor. All comm with the coin acceptor is done over serial
"""
import serial
from serial.serialutil import SerialException
import sys


class CoinAcceptor:
    """
    Class to interact with the Adafruit Coin Acceptor
    """

    def __init__(self, serial_port='/dev/ttyUSB0', baud_rate=4800, timeout=1, required_amt=0):
        """
        Opens the serial connection with the Coin Acceptor default connection is through USB

        :param serial_port: serial port to connect to, if not supplied defaults to /dev/ttyUSB0
        :param baud_rate: baud rate to run the serial connection at
        :param timeout: timeout allowed for serial connection
        :param required_amt: Set the amount (Integer) of money required to play the game
        """
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout

        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)
        except SerialException:
            sys.exit("Serial connection failed ensure that the Coin Acceptor is plugged in via USB & serial is enabled")

        self.required_amount = required_amt
        self.amount_inputted = 0

    def get_coin_input(self):
        """
        Gets the coin input. Note this will only run once.
        :return: Integer value of the coin input
        """
        serial_input = self.ser.readline()

        if len(serial_input) > 0:
            self.amount_inputted += ord(serial_input)
            return ord(serial_input)
        else:
            return 0

    def wait_for_coin_input(self):
        """
        Waits for coin input before returning. Warning this is blocking.
        :return: Integer value of the coin input
        """
        while True:
            serial_input = self.ser.readline()

            if len(serial_input) > 0:
                self.amount_inputted += ord(serial_input)
                return ord(serial_input)

    def set_amount_required(self, amount):
        """
        Set the required amount to play the game. Ex: 100 = $1
        :param amount:
        """
        self.required_amount = amount

    def has_collected_enough(self):
        """
        Check to see if the coin acceptor has collected enough money to run the game
        """
        return self.amount_inputted >= self.required_amount

    def reset_amount_inputted(self):
        """
        Reset the amount the user has inputted
        """
        self.amount_inputted = 0

    def close_serial_connection(self):
        """
        Close the serial connection with the coin acceptor
        :return:
        """
        try:
            self.ser.close()
        except SerialException:
            sys.exit("Failed to close the serial connection")

    def open_serial_connection(self):
        """
        Reopen the serial connection with the coin acceptor
        """
        try:
            self.ser.open()
        except SerialException:
            sys.exit("Failed to reopen the serial connection")
