import maestro
import threading
from time import sleep
try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
except:
    pass

class Arm_Controller():
    def __init__(self):
        #   0. szczypce
        #   1. rotacja szczycami
        #   2. pierwszy czlon
        #   3. drugi czlon prawe serwo norm
        #   4. drugi czlon lewe serwo odw
        #   5. podstawa prawe serwo norm
        #   6. podstawa lewe odw

        #   27 - dir
        #   22 - step
        self.pressed_state = False
        self.servo_running = True
        self.step_list = []
        self.servo = maestro.Controller()
        self.servo.setAccel(0, 6)
        self.servo.setAccel(1, 6)
        self.servo.setAccel(2, 6)
        self.servo.setAccel(3, 6)
        self.servo.setAccel(4, 6)
        self.servo.setAccel(5, 6)
        self.servo.setAccel(6, 6)
        self.servo.setSpeed(0, 10)
        self.servo.setSpeed(1, 10)
        self.servo.setSpeed(2, 10)
        self.servo.setSpeed(3, 10)
        self.servo.setSpeed(4, 10)
        self.servo.setSpeed(5, 10)
        self.servo.setSpeed(6, 10)
        self.servo.setRange(0, 2000, 8000)
        self.servo.setRange(1, 2000, 8000)

        self.pos = [2000, 7450, 8000, 8000, 4000, 4000, 8000, 0]
        self.step_count = 0
        t = threading.Thread(target=self.servo_thread, daemon=True)
        t.start()

    def jump_to(self, step):
        for e in range(len(step)):
            if e != 7:
                self.pos[e] = step[e]
            else:
                while step[7] > self.step_count:
                    self.step_count += 1
                    GPIO.output(27, GPIO.HIGH)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(22, GPIO.LOW)
                    sleep(0.01)
                while step[7] < self.step_count:
                    self.step_count -= 1
                    GPIO.output(27, GPIO.LOW)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(22, GPIO.LOW)
                    sleep(0.01)

    def stop(self):
        self.servo_running = False

    def servo_thread(self):
        try:
            GPIO.setup(27, GPIO.OUT)
            GPIO.setup(22, GPIO.OUT)
        except:
            pass

        while True:
            if self.servo_running:
                self.servo.setTarget(0, self.pos[0])
                self.servo.setTarget(1, self.pos[1])
                self.servo.setTarget(2, self.pos[2])
                self.servo.setTarget(3, self.pos[3])
                self.servo.setTarget(4, self.pos[4])
                self.servo.setTarget(5, self.pos[5])
                self.servo.setTarget(6, self.pos[6])
                if self.pos[7] == 1:
                    try:
                        GPIO.output(27, GPIO.HIGH)
                        GPIO.output(22, GPIO.HIGH)
                        self.pos[7] = 0
                        self.step_count += 1
                        GPIO.output(22, GPIO.LOW)

                    except:
                        pass
                if self.pos[7] == -1:
                    try:
                        GPIO.output(27, GPIO.LOW)
                        GPIO.output(22, GPIO.HIGH)
                        self.pos[7] = 0
                        self.step_count -= 1
                        GPIO.output(22, GPIO.LOW)
                    except:
                        pass

                sleep(0.01)
            else:
                return False



    def get_pos(self):
        pos = []
        pos.append(self.servo.getPosition(0))
        pos.append(self.servo.getPosition(1))
        pos.append(self.servo.getPosition(2))
        pos.append(self.servo.getPosition(3))
        pos.append(self.servo.getPosition(4))
        pos.append(self.servo.getPosition(5))
        pos.append(self.servo.getPosition(6))

        return pos


    def continous_func(self, c):
        if self.pressed_state:
            if c == 1:
                if (self.pos[2] - 50) >= 4000 and (self.pos[3] + 50) <= 8000 and (self.pos[4] - 50) >= 4000 and (self.pos[5] + 50) <= 8000 and (self.pos[6] - 50) >= 4000:
                    self.pos[2] -= 50
                    self.pos[3] += 50
                    self.pos[4] -= 50
                    self.pos[5] += 50
                    self.pos[6] -= 50

            if c == 4:
                if (self.pos[2] + 50) <= 8000 and (self.pos[3] - 50) >= 4000 and (self.pos[4] + 50) <= 8000 and (self.pos[5] - 50) >= 4000 and (self.pos[6] + 50) <= 8000:
                    self.pos[2] += 50
                    self.pos[3] -= 50
                    self.pos[4] += 50
                    self.pos[5] -= 50
                    self.pos[6] += 50

            if c == 5:
                if (self.pos[1] - 50) >= 4000:
                    self.pos[1] -= 50

            if c == 6:
                if (self.pos[1] + 50) <= 8000:
                    self.pos[1] += 50

            if c == 7:
                if (self.pos[0] - 50) >= 4000:
                    self.pos[0] -= 50

            if c == 8:
                if (self.pos[0] + 50) <= 8000:
                    self.pos[0] += 50

            if c == 2:
                self.pos[7] = 1

            if c == 3:
                self.pos[7] = -1

            sleep(0.05)
            return True
        return False




