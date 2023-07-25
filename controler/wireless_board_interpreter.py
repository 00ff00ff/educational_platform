import wireless_board
import threading
from gi.repository import GLib

class Board_Interpreter():

    def __init__(self):
        self.board = wireless_board.Wireless_board()
        self.setup_devices = []
        self.setup_devices_s = []
        self.s_piny = [
            ["15", "3"],
            ["16", "4"],
            ["17", "5"],
            ["18", "6"],
            ["19", "7"],
            ["9", "9"],
            ["2k", "0"],
            ["3k", "1"],
            ["8k", "2"],
        ]
        self.input = [0, 0, 0, 0, 0, 0, 0, 0]

    def swap_pin(self, Pin):
        for e in self.s_piny:
            if str(Pin) == e[1]:
                return e[0]

    def con_func(self):
        self.input = self.board.get_input_once(self.input)
        return True

    def setup(self):
        self.board.setup(self.setup_devices)
        self.board.setup(self.setup_devices_s)


    def add_device(self, Pin, Func):
        if Pin == 9:
            self.setup_devices_s.append([1, 4])
            self.setup_devices_s.append([1, 5])
            self.setup_devices_s.append([1, 6])
            self.setup_devices_s.append([1, 7])
        else:
            self.setup_devices.append([Func, self.swap_pin(Pin)])

    def set_device(self, Pin, Value):
        if Pin == 9:
            if Value == 0:
                self.board.send(("1/4k1/5k1/6k1/7k0e"))
            if Value == 1:
                self.board.send(("1/4k0/5k1/6k1/7k1e"))
            if Value == 2:
                self.board.send(("1/4k0/5k0/6k0/7k0e"))
            if Value == 3:
                self.board.send(("1/4k0/5k1/6k1/7k0e"))
            if Value == 4:
                self.board.send(("1/4k1/5k1/6k1/7k1e"))
        else:
            self.board.send(("1/" + str(self.swap_pin(Pin)) + str(Value) + "e"))

    def get_input(self, Pin):
        self.board.get_input_once(self.input, self.swap_pin(Pin))
        return int(self.input[int(Pin)])

    def straight(self):
        return 0

    def back(self):
        return 1

    def stop(self):
        return 2

    def left(self):
        return 3

    def right(self):
        return 4

