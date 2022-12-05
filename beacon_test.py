
from lib_mcp23017 import MCP23017
import time
import RPi.GPIO as GPIO
fpin=0
bpin=1
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
GPIO2.setup(fpin, GPIO.IN)
GPIO2.setup(bpin, GPIO.IN)

while 1:
	k=5
	inpf=1
	inpb=1
	while k:
		if GPIO2.input(fpin)==0:
			inpf=0
		if GPIO2.input(bpin)==0:
			inpb=0
		k-=1
	#	time.sleep(0.1)
	if inpf:
		print ("front triggered!!!!!")
	elif inpb:
		print("back triggered")
	else:
		print("nil")
#	time.sleep(1)
