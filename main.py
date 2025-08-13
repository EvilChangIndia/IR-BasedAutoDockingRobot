import os
import RPi.GPIO as GPIO
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685 #using the i2c device
from adafruit_motor import servo
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1
delta=1.33 #volts
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c,address=0x40)
pca.frequency = 60
#pca.reset()
#SS5= servo.Servo(pca.channels[5])
#SS6= servo.Servo(pca.channels[6],min_pulse=500, max_pulse=2500, actuation_range=180) #OUTER OF STIRRER 2

from lib_mcp23017 import MCP23017
import time
import RPi.GPIO as GPIO

print("")
if GPIO.RPI_REVISION > 0:
        from smbus import SMBus
        i2cbus = SMBus(1)  # SMBus(0) or SMBus(1) depending board revision
        resetPin=0
else:
        i2cbus = GPIO.I2C()
        #i2cbus.detect()     # optional diagnostic: find devices on I2C bus.  Comment out when finished with this!
        resetPin = 0
GPIO2 = MCP23017(GPIO, i2cbus, 0x20, resetPin)

if not GPIO2.found:
    print ("MCP23017 on %s not detected, or not reset properly" % hex(GPIO2.addr))

GPIO2.setup(0, GPIO.IN)
inp=0
while 1:
	k=10
	while k:
		if GPIO2.input(0)==1:
			inp=1
		k-=1
	#	time.sleep(0.1)
	if inp:
		print ("There you are!!!!!")
	else:
		print(".")
	inp=0

class MCBot:
	def __init__(self):    #value is an array of the format: [forward intensity,backward intensity,left,right]]
		self.xmid=0
		self.ymid=0
		self.values=[]
		self.lvalues=[]
		self.charging=0
		self.lf1=0
		self.lf2=0
		self.lb1=0
		self.lb2=0
		self.rf1=0
		self.rf2=0
		self.rb1=0
		self.rb2=0

		invertl=0
		invertr=1

		self.SS0= pca.channels[4] #pins for left side
		self.SS1= pca.channels[5]
		self.SS2= pca.channels[6]
		self.SS3= pca.channels[7]
		self.SS4= pca.channels[0+invertr] #pins for right side
		self.SS5= pca.channels[1-invertr]
		self.SS6= pca.channels[2+invertr]
		self.SS7= pca.channels[3-invertr]

		self.charger=pca.channels[8]

		self.sx= servo.Servo(pca.channels[13]) #x-axis pan
		self.sy= servo.Servo(pca.channels[12]) #y-axis pan
#		self.ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x41)
#		self.ina.configure(self.ina.RANGE_32V)
		#self.set_cam_centre()
		#self.fbmult=1
		#self.lrmult=0.8
		#self.charge(0)
		self.led(0)

	def set_cam_centre(self, o='m'):
		self.xmid=70
		self.ymid=90 
		if o=='d':
			self.ymid=45
		elif o=='u':
			self.ymid=180
#		print("toggled cam centre to ", o)
	
	def look_around(self,v):
		invertx=-1
		inverty=1
		self.lvalues=v
		sx=max(0, (self.xmid+((v[0]/100)*75)*invertx))
		sy=max(0, (self.ymid+((v[1]/100)*90)*inverty))
		self.sx.angle=min(int(sx),180)
		self.sy.angle=min(int(sy),180)
		print("panning cam")

	def centre_cam(self):
		sx=self.xmid
		sy=self.ymid
		self.sx.angle=min(int(sx),180)
		self.sy.angle=min(int(sy),180)
		print("centring cam")

	def calc_intensities(self):
		v=self.values
		v = [min(value, 100) for value in v]
		#v[0]=v[0]*self.fbmult
		#v[1]=v[1]*self.fbmult
		#v[2]=v[2]*self.lrmult
		#v[2]=v[3]*self.lrmult
		self.lf1=min(65535, (int(655.35*(v[1]+v[2]))))
		self.lf2=min(65535, (int(655.35*(v[0]+v[3]))))
		self.lb1=min(65535, (int(655.35*(v[1]+v[2]))))
		self.lb2=min(65535, (int(655.35*(v[0]+v[3]))))
		self.rf1=min(65535, (int(655.35*(v[1]+v[3]))))
		self.rf2=min(65535, (int(655.35*(v[0]+v[2]))))
		self.rb1=min(65535, (int(655.35*(v[1]+v[3]))))
		self.rb2=min(65535, (int(655.35*(v[0]+v[2]))))
		#print("calculated intensity")

#	def calc_intensities(self):
#		v=self.values
#		self.lf1=int(655.35*v[1])
#		self.lf2=min(int(655.35*((v[0]**2+v[3]**2)**0.5)),65535) 
#		self.lb1=int(655.35*v[1])
#		self.lb2=min(int(655.35*((v[0]**2+v[3]**2)**0.5)),65535)
#		self.rf1=int(655.35*v[1])
#		self.rf2=min(int(655.35*((v[0]**2+v[2]**2)**0.5)),65535)
#		self.rb1=int(655.35*v[1])
#		self.rb2=min(int(655.35*((v[0]**2+v[2]**2)**0.5)),65535)
		#print("calculated intensity")	
		#print(" lf1= ", self.lf1)
		#print(" lf2= ", self.lf2)
		#print(" lb1= ", self.lb1)
		#print(" lb2= ", self.lb2)
		#print(" rf1= ", self.rf1)
		#print(" rf2= ", self.rf2)
		#print(" rb1= ", self.rb1)
		#print(" rb2= ", self.rb2)

	def update(self,values):
		self.values=values
		self.calc_intensities()
		print("updated values to ", self.values)

	def move(self,t=0):			#moves machine for time t
		self.SS0.duty_cycle=self.lf1
		self.SS1.duty_cycle=self.lf2
		self.SS2.duty_cycle=self.lb1
		self.SS3.duty_cycle=self.lb2
		self.SS4.duty_cycle=self.rf1
		self.SS5.duty_cycle=self.rf2
		self.SS6.duty_cycle=self.rb1
		self.SS7.duty_cycle=self.rb2
		print("moving")
		time.sleep(t)

	def stop(self):
		self.SS0.duty_cycle=0
		self.SS1.duty_cycle=0
		self.SS2.duty_cycle=0
		self.SS3.duty_cycle=0
		self.SS4.duty_cycle=0
		self.SS5.duty_cycle=0
		self.SS6.duty_cycle=0
		self.SS7.duty_cycle=0
		print("stopping")

	def refresh(self,values,t=0):   #updates values and moves for t seconds
		self.update(values)
		self.move(t)
		self.stop()

	def set_velocity(self,values):   #updates values and moves
		self.update(values)
		self.move_indefinitely()

	def move_indefinitely(self):	#moves machine
		self.SS0.duty_cycle=self.lf1
		self.SS1.duty_cycle=self.lf2
		self.SS2.duty_cycle=self.lb1
		self.SS3.duty_cycle=self.lb2
		self.SS4.duty_cycle=self.rf1
		self.SS5.duty_cycle=self.rf2
		self.SS6.duty_cycle=self.rb1
		self.SS7.duty_cycle=self.rb2

	def charge(self,state):
		self.charging=state
		self.charger.duty_cycle=0 if state==1 else 65535 

	def led(self,state):
		l=1 if state==0 else 0
		GPIO.output(17,l)

	def vread(self):
#		volt=ina.supply_voltage()+delta
#		return volt
		return 0
	def vreadavg(self,n):
		volt=0
#		for i in range(0,n):
#			volt+=self.ina.supply_voltage()
#		volt=volt/n + delta
		return volt

	def speak(self,text):
		os.system('sh audio.sh "'+text+'"')
		print("audio time!")
if __name__ == "__main__":

	m=MCBot()
	m.speak("hi friends. drink tea.")
	m.refresh([100,0,0,0],3)
	m.refresh([0,100,0,0],3)
#	m.look_around([100,-100])
	#m.charge(1)
	#print("charging")
	#a=i=0
	#m.charge(0)
	#print("not charging")
	#time.sleep(100)
	#m.led(1)
#	m.charge(0)
	#print("disconnected")
	#time.sleep(2)
	#m.led(0)
	m.centre_cam()
	#pca.reset()
	#pca.deinit()

