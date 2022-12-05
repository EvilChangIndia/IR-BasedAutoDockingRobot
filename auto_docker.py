import os
import RPi.GPIO as GPIO
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685 #using the i2c device
from adafruit_motor import servo
from ina219 import INA219
from ina219 import DeviceRangeError
from lib_mcp23017 import MCP23017

SHUNT_OHMS = 0.03
MAX_EXPECTED_AMPS = 5
delta=1.33 #volts
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c,address=0x40)
pca.frequency = 60
inp=0

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
GPIO2.setup(1, GPIO.IN)

class MCBot:
	def __init__(self):    #value is an array of the format: [forward intensity,backward intensity,left,right]]
		self.beacon1=0 	#beacon at front
		self.beacon2=1 	#beacon at back
		invertl=0
		invertr=1
		
		#add other initializations here

	def beacon(self, k=10):		
		inp=0
		while k:				#k is the sample size
			if GPIO2.input(self.beacon1)==1:
				inp=1
			elif GPIO2.input(self.beacon2)==1:
				inp=2
			else:
				inp=0
			k-=1
		return inp

	def allign(self, id=1,t=20):
		if id==1:			#left		
			self.charger_dir=0
			while 1:
				self.refresh([0,0,30,0],0.02)
				inp=self.beacon()
				if inp:
					inp=self.beacon(40)
					if inp:
						self.charger_dir=inp
						print("ID1: Found charger in the ")
						if inp==1:
							print("Front")
						if inp==2:
							print("Back")

						return 1
			return 0
		if id==2:			#right
			self.charger_dir=0
			while 1:
				self.refresh([0,0,0,30],0.05)
				inp=self.beacon()
				if inp:
					inp=self.beacon(500)
					if inp:
						self.charger_dir=inp
						print("Found charger")
						return 1
			return 0
		if id==3:			# Sweep allign: relocate beacon
			tt=t
			f=0
			while 1:
				while t:
					if t>(tt/2):			#left sweep
						if t>(3*tt/4):
							self.refresh([0,0,30,0],0.05)
						else:
							self.refresh([0,0,0,30],0.05)
					else:				#right sweep
						if t>(tt/4):
							self.refresh([0,0,0,30],0.05)
						else:
							self.refresh([0,0,30,0],0.05)
					t=t-1
					if self.beacon():
						f=1
						break
				if f==1:
					print("ID3: Found beacon!")
					self.allign(4)
					break
				else:
					print("ID3: increased sweep by 4")
					tt=tt+4
					t=tt
			return 0
		if id==4:			#sweep allign repeated
			#tt=t
#			print ("id 4")
			stepsl=0 #temp variable
			steps=0	#steps variable
			while self.beacon()==self.charger_dir:
				self.refresh([0,0,30,0],0.1)
				stepsl+=1
#				print("1")
			steps=stepsl
			while stepsl:
				self.refresh([0,0,0,30],0.1)
				stepsl-=1
#				print("2")
			while self.beacon()==self.charger_dir:
				self.refresh([0,0,0,30],0.1)
				stepsl+=1
#				print("3")
			steps+=stepsl
#			print("steps= ", steps)
			stepsl=int(steps/2)
			stepsl=stepsl if stepsl%2==0 else stepsl+1
			while stepsl>0:
				self.refresh([0,0,30,0],0.1)
#				print("4")
				stepsl-=1
			if self.beacon():
				print("ID4: Fully Alligned!")
				return 1
			else:
				print("ID4: Lost beacon position. Realligning..")
				return 0
	def park(self):							#main algo
		k=0
		self.allign(1)						#to initially locate the beacon approximately
		while 1:
			if self.ireadavg(5)>0:
				break
			if k%30==0:
#				self.allign(3,4)
				i=self.allign(4)
				if i==0:
					self.allign(3,20)
#					self.allign(4)
			d=[35,0,0,0]if self.charger_dir==1 else [0,35,0,0]
			self.refresh(d,0.007)
			time.sleep(0.05)
			k=k+1
		print("Park: Done parking!")


	def refresh(self,values,t=0):   #updates values(drection of motion) and move machine for t seconds
		'''Your code here'''

	#add other functions here

if __name__ == "__main__":

	m=MCBot()
	while 1:                 #choose 3 for this code. rest work work
		i=int(input("1. Zero all 2. Allign 3. Park\t: "))
		if i==1:
			m.refresh([0,0,0,0],3)
		elif i==2:
			k=int(input("id: "))
			m.allign(k,10)
		elif i==3:
			m.park()
		else:
			break

	pca.deinit()

