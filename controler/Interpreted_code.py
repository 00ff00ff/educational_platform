from time import sleep
try:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
except:
	pass

class MyProgram():
	def __init__(self):
		self.output = ""
		self.con = True
	def code(self):
		import wireless_board_interpreter
		l =wireless_board_interpreter.Board_Interpreter()
		
		l.add_device(6,0)
		l.add_device(7,0)
		l.add_device(9,1)
		l.setup()
		
		while self.con:
			if l.get_input(6)>200 and l.get_input(7)>200:
				l.set_device(9, l.straight())
				
			elif l.get_input(6)>200:
				l.set_device(9, l.right())
				
				
			elif l.get_input(7)>200:
				l.set_device(9, l.left())
				
				
			else:
				l.set_device(9, l.stop())
				
				
			sleep(0.1)
			
			