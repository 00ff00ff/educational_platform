import RPi.GPIO as GPIO

class Panel_Interpreter():

    def __init__(self):
        self.pins = [
            [1, 27],
            [2, 22],
            [3, 23],
            [4, [6, 12]],
            [5, [13, 16]],
            [6, 24],
            [7, 25],
            [8, 5],
            [9, 4],
            [10, 26],
            [11, 10],
            [12, 17],
            [13, 18]
        ]
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def add_device(self, Pin, Func):
        if Pin == 5:
            pins = self.swap_pin(Pin)
            GPIO.setup(pins[0], GPIO.OUT)
            GPIO.setup(pins[1], GPIO.OUT)
        elif Pin == 4:
            pins = self.swap_pin(Pin)
            GPIO.setup(pins[0], GPIO.IN)
            GPIO.setup(pins[1], GPIO.IN)
        elif Pin == 10 or Pin == 11 or Pin == 9:
            GPIO.setup(self.swap_pin(Pin), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else:
            if Func == 0:
                GPIO.setup(self.swap_pin(Pin), GPIO.IN)
            if Func == 1:
                GPIO.setup(self.swap_pin(Pin), GPIO.OUT)


    def swap_pin(self, Pin):
        for e in self.pins:
            if e[0] == Pin:
                return e[1]

    def get_input(self, Pin):
        if Pin == 4:
            if GPIO.input(6):
                return 1
            if GPIO.input(12):
                return -1
        return GPIO.input(self.swap_pin(Pin))

    def set_device(self, Pin, Val):
        if Pin == 5:
            if Val == 1:
                GPIO.output(13, GPIO.HIGH)
                GPIO.output(16, GPIO.LOW)
            if Val == 0:
                GPIO.output(16, GPIO.HIGH)
                GPIO.output(13, GPIO.LOW)
            if Val == -1:
                GPIO.output(16, GPIO.LOW)
                GPIO.output(13, GPIO.LOW)
        else:
            GPIO.output(self.swap_pin(Pin), Val)