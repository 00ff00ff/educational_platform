import serial
import threading
from time import sleep





class Wireless_board():

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200)
        self.ser.timeout = 0.01
        self.stan = False
        self.wait_for_input = True
        self.delay = False
        self.inpt = ""
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

    def swap_pin(self, Pin):
        for e in self.s_piny:
            if str(Pin) == e[0]:
                return e[1]

    def stop(self):
        self.stan = False


    def send_command(self, s_lista_polecen):
        self.stan = True
        c = []
        for e in s_lista_polecen:
            if e[0] == 2:
                c.append("d" + str(e[1]))
                continue
            if e[1] == 9:
                if e[2] == 0:
                    c.append("4k1")
                    c.append("5k1")
                    c.append("6k1")
                    c.append("7k0")
                if e[2] == 1:
                    c.append("4k0")
                    c.append("5k1")
                    c.append("6k1")
                    c.append("7k1")
                if e[2] == 2:
                    c.append("4k1")
                    c.append("5k0")
                    c.append("6k0")
                    c.append("7k0")
                if e[2] == 3:
                    c.append("4k0")
                    c.append("5k1")
                    c.append("6k1")
                    c.append("7k0")
                if e[2] == 4:
                    c.append("4k1")
                    c.append("5k1")
                    c.append("6k1")
                    c.append("7k1")
                continue
            if len(str(e[1])) == 2:
                ce = ""
                ce += str(e[1])
                if e[0] == 0:
                    ce += 'i'
                    c.append(ce)
            elif len(str(e[1])) == 1:
                ce = ""
                ce += (str(e[1]) + 'k')
                if e[0] == 0:
                    ce += 'i'
                    c.append(ce)
        self.t = threading.Thread(target=self.serial_worker, args=[c])
        self.t.start()

    def send(self, c):
        self.ser.write(bytes(c, 'UTF-8'))

    def serial_worker(self, c):
        while True:
            if not self.stan:
                for e in range(10):
                    self.send("1/5k0/6k0e")
                return False
            command = "1"
            self.ser.flush()
            for e in c:
                if e[0] == 'd':
                    if command != "1":
                        self.send((command + 'e'))
                        command = "1"
                    delay = ""
                    for d in range(1, len(e), 1):
                        delay += e[d]
                    self.delay = True
                    sleep(int(delay)/1000)
                    self.delay = False
                    continue
                command += ('/' + e)
            if command != "1":
                 self.send((command + 'e'))



    def setup(self, s_lista_urzadzen):
        c = "0"
        for e in s_lista_urzadzen:
            c += "/"
            try:
                if e[3] == 9:
                    c += str(e[1][0]) + "k1"
                    c += "/"
                    c += str(e[1][1]) + "k1"
                    c += "/"
                    c += str(e[1][2]) + "k1"
                    c += "/"
                    c += str(e[1][3]) + "k1"
                    continue
            except:
                pass
            if len(str(e[1])) == 2:
                c += str(e[1])
            else:
                c += (str(e[1]) + 'k')
            c += str(e[0])
        c += 'e'
        self.send(c)

    def read_until(self, terminator):
        s = ""
        c = ''
        while c != terminator:
            if self.ser.in_waiting:
                c = self.ser.read(1).decode('UTF-8')
                s += str(c)
            else:
                return s
        return s

    def find(self, f, seq):
        for item in seq:
            if f(item):
                return item

    def get_input_once(self, i, c):
        self.send("1/" + c + "ie")
        if self.ser.in_waiting:
            self.inpt = self.read_until(terminator='e')
        ipt = []
        bypass = False
        p = ""
        w = ""
        for e1 in range(len(self.inpt)):
            if self.inpt[e1] == '/':
                if len(p) == 2 or bypass:
                    ipt.append([p, w])
                    p = ""
                    w = ""
                    bypass = False
                    continue
                continue
            else:
                if self.inpt[e1] == 'o':
                    continue
                if self.inpt[e1] == 'e':
                    ipt.append([p, w])
                    break
                if len(p) < 2 and not bypass:
                    if self.inpt[e1] != 'k':
                        p += self.inpt[e1]
                    else:
                        bypass = True
                    continue
                w += self.inpt[e1]
        try:
            if ipt != None:
                for e in ipt:
                    if e != None:
                        i[int(self.swap_pin(e[0]))] = e[1]
                        self.ser.flush()
                        return i
            return i

        except:
            return i



    def proceed_input(self, s_lista_urzadzen):
        if self.ser.in_waiting:
            self.inpt = self.ser.read_until(size=100).decode('UTF-8')
        ipt = []
        bypass = False
        p = ""
        w = ""
        for e1 in range(len(self.inpt)):
            if self.inpt[e1] == '/':
                if len(p) == 2 or bypass:
                    ipt.append([p, w])
                    p = ""
                    w = ""
                    bypass = False
                    continue
                continue
            else:
                if self.inpt[e1] == 'o':
                    continue
                if self.inpt[e1] == 'e':
                    ipt.append([p, w])
                    break
                if len(p) < 2 and not bypass:
                    if self.inpt[e1] != 'k':
                        p += self.inpt[e1]
                    else:
                        bypass = True
                    continue
                w += self.inpt[e1]
        output = ""
        for e in ipt:
            s = self.find(lambda x: str(x[1]) == e[0], s_lista_urzadzen)
            if s != None:
                output += ("\n" + "Wartosc " + s[2] + " = " + e[1])
        self.ser.flush()

        return output



    def close(self):
        self.ser.close()


