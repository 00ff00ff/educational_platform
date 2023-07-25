import Final_Program


class Arm_Controller():
    def __init__(self):
        pass

    def jump_to(self, step):
        Final_Program.trik().servo.jump_to(step)
