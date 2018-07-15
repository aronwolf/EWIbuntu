#!/usr/bin/python
import bluepy.btle as btle
import binascii
import mido
import time
import os
import sys
#import RPi.GPIO as GPIO


# Settings
PRINT = True		# set to True to enable printing to screen (for debugging)
#GPIO.setwarnings(False) # don't print warnings about GPIO events


# The following settings are for the midi ports that are used to send
# and receive midi messages to/from the EWI
# 
# Only parts of the names are needed, as the program does a "contains"-type
# match. The program is set up to be able to use RtMidi or PortMidi backends. PortMidi
# is the default for Mido and is installed with Mido. When the program does a search for available ports
# different names are generated, depending on the backend used. The defaults here work with
# both backends.
SYSEXPORT = "Vir"	# the port for receiving Sysex messages.
EWIPORT = "EWI"		# the port the EWI_USB appears on if using USB not BT.

# FILE LOCATIONS

SYNTHPORTFILE = "/home/aron/ewi/data/synthport.txt" 	# the path to the file with the name of the synth port
NOTEOFFFILE = "/home/aron/ewi/data/noteoff.txt" 		# the path to the file to turn on the noteoff function
BUTTONSFILE = "/home/aron/ewi/data/buttons.txt" 		# the path to the file to turn on GPIO buttons function
EWIDATAFILE = "/home/aron/ewi/data/ewidata.txt" 		# the path to the file with the config data read from the EWI 
EWICONFIGFILE = "/home/aron/ewi/data/sendewidata.txt"	# the path to the file with the new config to be sent to the EWI
P1CONFIGFILE = "/home/aron/ewi/data/preset1.txt"		# the path to the file with the preset config to be sent to the EWI
P2CONFIGFILE = "/home/aron/ewi/data/preset2.txt"		# the path to the file with the preset config to be sent to the EWI
P3CONFIGFILE = "/home/aron/ewi/data/preset3.txt"		# the path to the file with the preset config to be sent to the EWI
P4CONFIGFILE = "/home/aron/ewi/data/preset4.txt"		# the path to the file with the preset config to be sent to the EWI
MODECONFIGFILE = "/home/aron/ewi/data/mode.txt"		# the path to the BT/USB mode setting file
BTADDRESSFILE = "/home/aron/ewi/data/btaddress.txt"	# the path to the UD-BT01 Bluetooth address file
FINETUNEFILE = "/home/aron/ewi/data/finetune.txt"		# the path to the synth fine tune setting file

#Uncomment the following line if you want to use RtMidi (You will need to install RtMidi yourself).
mido.set_backend('mido.backends.rtmidi')

# The preset buttons and thier LEDs use GPIO
#GPIO.setmode(GPIO.BCM)
#GINPUTS = [4, 17, 22, 10]	# these are the inputs in order as wired
#GOUTPUTS = [18, 23, 25, 24] # these are the outputs (LEDs) in order as wired
#for n in GINPUTS:
#	GPIO.setup(n, GPIO.IN)
#for n in GOUTPUTS:
#        GPIO.setup(n, GPIO.OUT)

usleep = lambda x: time.sleep(x/1000000.0)	# introducing microseconds sleep times


# =====================================================================
# Functions-----------------------
# ================================

def readEWI():

	try: 
		os.remove(EWIDATAFILE)
	except:
		if PRINT: print "file already deleted"



#	if MODE == "BT":
#		# Sends Sysex requests to the EWI to read its settings
#		#
#		# Writing data to the udbt01 is done to handle 27 (decimal)
#		# The first two bytes of each message are:
#		# 1. the header (a dummy value that works)
#		# 2. the timestamp (arbirary value, but increasing)
#		# The second-last char on the two data requests is 
#		# a timestamp (arbitrary, but increasing) 
#
#		if PRINT: print "Reading EWI via BT..."
#
#
#    		# send enable request
#		p.writeCharacteristic(27, "\x80\x84\xB0\x63\x01\xB0\x62\x04\xB0\x06\x20", False) 
#
#		# A short delay is needed here, otherwise the messages get confused
#		time.sleep(0.2)
#
#		# request bank 0 data
#		p.writeCharacteristic(27, "\x80\x82\xF0\x47\x7F\x6D\x40\x00\x00\x83\xF7", False)
#	
#		time.sleep(0.2)
#
#   		# send enable request
#		p.writeCharacteristic(27, "\x80\x84\xB0\x63\x01\xB0\x62\x04\xB0\x06\x20", False) 
#		time.sleep(0.2)
#	
#		# request bank 2 data
#		p.writeCharacteristic(27, "\x80\x85\xF0\x47\x7F\x6D\x42\x00\x00\x86\xF7", False) 
#		time.sleep(0.2)
#
#		# send "finished" request. This is generally not needed
#		p.writeCharacteristic(27, "\x80\x87\xB0\x63\x01\xB0\x62\x04\xB0\x06\x10", False)
#
#	else: 

	if PRINT: print "Reading EWI via USB..."

	# send "enable" request
	USBOUTPORT.send(mido.parse([0xB0, 0x63, 0x01]))
	USBOUTPORT.send(mido.parse([0xB0, 0x62, 0x04]))
	USBOUTPORT.send(mido.parse([0xB0, 0x06, 0x20]))
	time.sleep(0.2)

	# request bank 0 data
	USBOUTPORT.send(mido.Message('sysex', data=[71, 127, 109, 64, 0, 0]))
	time.sleep(0.2)
		
	# send "enable" request
	USBOUTPORT.send(mido.parse([0xB0, 0x63, 0x01]))
	USBOUTPORT.send(mido.parse([0xB0, 0x62, 0x04]))
	USBOUTPORT.send(mido.parse([0xB0, 0x06, 0x20]))
	time.sleep(0.2)

	# request bank 2 data
	USBOUTPORT.send(mido.Message('sysex', data=[71, 127, 109, 66, 0, 0]))
	time.sleep(0.2)


	# send "finished" request
	USBOUTPORT.send(mido.parse([0xB0, 0x63, 0x01]))
	USBOUTPORT.send(mido.parse([0xB0, 0x62, 0x04]))
	USBOUTPORT.send(mido.parse([0xB0, 0x06, 0x10]))

	return

# =====================================================================

def configEWI(PRESET):
	# Sends the Sysex commands to the EWI
	# to change the configuration.

	# preset 0 is used when the config update is requested from the web page
	# it uses the file that is written by the webpage. This includes
	# the "reset to defaults" function

	if PRESET == 0:
		FILE = open(EWICONFIGFILE,'r')
	if PRESET == 1:
		FILE = open(P1CONFIGFILE,'r')
	if PRESET == 2:
		FILE = open(P2CONFIGFILE,'r')
	if PRESET == 3:
		FILE = open(P3CONFIGFILE,'r')
	if PRESET == 4:
		FILE = open(P4CONFIGFILE,'r')

	L1 = (FILE.readline()).replace("\n","")
	L2 = (FILE.readline()).replace("\n","")
	FILE.close()

	L1 = L1.replace("F0 47 00","F0 47 7F")	# replace "receive" with "send" - only needed for the presets
	L2 = L2.replace("F0 47 00","F0 47 7F")


	# create lists from hex strings
	LINE1 = L1.split()
	LINE2 = L2.split()

#	if MODE == "BT":
#		if PRINT: print "Configuring EWI via BT..."
#
#		# The udbt01 has a max character limit of 20, so
#		# the second Sysex has to be split into two
#		# arbitrary header bytes and timestamps are used
#
#		# modify line 1 to fit BT MIDI spec for Sysex
#		LINE1.pop(-1)	#remove last character
#		LINE1 = ['80','82'] + LINE1 + ['83','F7']	#add header and (2) timing bytes
#
#		# line 2 is 19 char long. Max size is 20 char.
#		# Need to take off last char, and add header and 1 timing bytes (=20 chars)
#		# then add a line 3 with a header, timing byte and F7 (Sysex end byte)
#		LINE2.pop(-1)	#remove last character
#		LINE2 = ['80','85'] + LINE2	# add header and timing byte
#		LINE3 = ['80','86','F7']	# create line 3
#
#		# Convert to binary
#		B1 = binascii.unhexlify("".join(LINE1))
#		B2 = binascii.unhexlify("".join(LINE2))
#		B3 = binascii.unhexlify("".join(LINE3))
#
#		# Data is written to handle 27 (decimal) 
#   		# send "enable" request
#		p.writeCharacteristic(27, "\x80\x84\xB0\x63\x01\xB0\x62\x04\xB0\x06\x20", False) 
#		time.sleep(0.2)
#
#		# send line 1
#		p.writeCharacteristic(27, B1, False) 
#		time.sleep(0.2)
#
#		# send "enable" request
#		p.writeCharacteristic(27, "\x80\x84\xB0\x63\x01\xB0\x62\x04\xB0\x06\x20", False) 
#		time.sleep(0.2)
#
#		# send line 2 in two messages 
#		p.writeCharacteristic(27, B2, False) 
#		time.sleep(0.2)
#
#		p.writeCharacteristic(27, B3, False)
#		time.sleep(0.2)
#
#		# send "finished" request
#		p.writeCharacteristic(27, "\x80\x87\xB0\x63\x01\xB0\x62\x04\xB0\x06\x10", False) 
#
#	else:

	if PRINT: print "Configuring EWI via USB..."
		# send "enable" request
	USBOUTPORT.send(mido.parse([0xB0, 0x63, 0x01]))
	USBOUTPORT.send(mido.parse([0xB0, 0x62, 0x04]))
	USBOUTPORT.send(mido.parse([0xB0, 0x06, 0x20]))
		# remove F0 and F7 chars 
	LINE1.pop(0)
	LINE1.pop(-1)
	INTLIST = [int(x,16) for x in LINE1]
		# send bank 0 data
	USBOUTPORT.send(mido.Message('sysex', data=INTLIST))

	# send "enable" request
	USBOUTPORT.send(mido.parse([0xB0, 0x63, 0x01]))
	USBOUTPORT.send(mido.parse([0xB0, 0x62, 0x04]))
	USBOUTPORT.send(mido.parse([0xB0, 0x06, 0x20]))
	
	# remove F0 and F7 chars 
	LINE2.pop(0)
	LINE2.pop(-1)
	INTLIST = [int(x,16) for x in LINE2]
	# send bank 2 data
	USBOUTPORT.send(mido.Message('sysex', data=INTLIST))
		# send "finished" request
	USBOUTPORT.send(mido.parse([0xB0, 0x63, 0x01]))
	USBOUTPORT.send(mido.parse([0xB0, 0x62, 0x04]))
	USBOUTPORT.send(mido.parse([0xB0, 0x06, 0x10]))


	return

# =====================================================================

def readPRESETS():
	# read the EWIDATA
	try:
		FILE = open(EWIDATAFILE,'r')
		L1 = (FILE.readline()).replace("\n","")
		L2 = (FILE.readline()).replace("\n","")
		FILE.close()
	except:
		L1=""
		L2=""

	# read presets
	FILE = open(P1CONFIGFILE,'r')
	P1L1 = (FILE.readline()).replace("\n","")
	P1L2 = (FILE.readline()).replace("\n","")
	FILE.close()

	FILE = open(P2CONFIGFILE,'r')
	P2L1 = (FILE.readline()).replace("\n","")
	P2L2 = (FILE.readline()).replace("\n","")
	FILE.close()

	FILE = open(P3CONFIGFILE,'r')
	P3L1 = (FILE.readline()).replace("\n","")
	P3L2 = (FILE.readline()).replace("\n","")
	FILE.close()

	FILE = open(P4CONFIGFILE,'r')
	P4L1 = (FILE.readline()).replace("\n","")
	P4L2 = (FILE.readline()).replace("\n","")
	FILE.close()


	# check against presets and turn on or off appropriate LEDs
#	if BUTTONS:	
#		if L1 + L2 == P1L1 + P1L2:
#			GPIO.output(GOUTPUTS[0],1)
#		else:
#			GPIO.output(GOUTPUTS[0],0)
#		if L1 + L2 == P2L1 + P2L2:
#			GPIO.output(GOUTPUTS[1],1)
#		else:
#			GPIO.output(GOUTPUTS[1],0)
#		if L1 + L2 == P3L1 + P3L2:
#			GPIO.output(GOUTPUTS[2],1)
#		else:
#			GPIO.output(GOUTPUTS[2],0)
#		if L1 + L2 == P4L1 + P4L2:
#			GPIO.output(GOUTPUTS[3],1)
#		else:
#			GPIO.output(GOUTPUTS[3],0)

	return

# =====================================================================

def configSYNTH():

# read the ewidata file
	try:
		FILE = open(EWIDATAFILE,'r')
		L1 = (FILE.readline()).replace("\n","")
		L2 = (FILE.readline()).replace("\n","")
		FILE.close()
	except:
		L2="00 00 00 00 00 00 00 00"

# extract the midi channel
	LINE2 = L2.split()
	try:
		MIDICHAN = int(LINE2[7],16)
	except:
		MIDICHAN = 0

# read the finetune file
	FILE = open(FINETUNEFILE,'r')
	FINETUNE = int((FILE.readline()).replace("\n",""))
	FILE.close()

	# send the finetune info to the synth
	sendmidi(mido.Message('control_change', channel=MIDICHAN, control=101, value=0))
	sendmidi(mido.Message('control_change', channel=MIDICHAN, control=100, value=1))
	sendmidi(mido.Message('control_change', channel=MIDICHAN, control=6, value=FINETUNE))
	sendmidi(mido.Message('control_change', channel=MIDICHAN, control=38, value=0))
	sendmidi(mido.Message('control_change', channel=MIDICHAN, control=101, value=127))
	sendmidi(mido.Message('control_change', channel=MIDICHAN, control=100, value=127))



	return

def writesysex(MSG):	# writes the received Sysex messages to a file
	if PRINT: print "Writing EWIDATA file"
	FILE = open(EWIDATAFILE,'a')
	FILE.write(" ".join(MSG) + "\n")
        FILE.close()

	return

# =====================================================================

def sendmidi(MSG):	# Sends the midi messages to the synth
	global HELDMSG
		
	OUTPORT.send(MSG) 


	# If the MIDI message is for a new note-on,
	# the next section adds an extra "note-off" for the previous note played
	# This is needed because the EWI misses note-off commands occasionally.
	if NOTEOFF:
        	if MSG.type == 'note_on' and MSG.velocity >0:
			if MSG.note != HELDMSG.note:
				usleep(500.0) # introduce a small delay
				OUTPORT.send(HELDMSG.copy(velocity=0))
				if PRINT: print "Noteoff sent for note "+str(HELDMSG.note)
				HELDMSG = MSG	
	return

# =========================================================================

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise

    def handleNotification(self, cHandle, data):
        # ... process 'data'
	global SYSEX, SYSEXSAVE, PRINT
	# check if it is a Sysex message (third char is F0), or we are waiting for a Sysex tail
	if data[2:3] == "\xF0" or SYSEX: 
		MIDILINE = binascii.hexlify(data).upper()	# convert to hex
		MIDILINE = ' '.join([MIDILINE[i:i+2] for i in range(0, len(MIDILINE), 2)]) # add spaces
		MIDI = MIDILINE.split()		# create a list variable
		if MIDI[-1] != "F7":	# The last char is not F7, we have the first part of a Sysex
			MIDI.pop(0)	# remove header
			MIDI.pop(0)	# remove first timestamp
			SYSEXSAVE = MIDI	#save the part message
			SYSEX = True	#set this to True so the following message is concatenated
		else:
			# we have a short Sysex or a tail
			if SYSEX:		# it's a tail
				MIDI.pop(0) 	# remove header
				MIDI.pop (-2)	# remove second timestamp (second-last char)
				SYSEXSAVE = SYSEXSAVE + MIDI	# concatenate tail
			else:			# it's a short Sysex 
				MIDI.pop(0)	# remove header
				MIDI.pop(0)	# remove first timestamp
				MIDI.pop(-2)	# remove second timestamp (second-last char)
				SYSEXSAVE = MIDI
			if PRINT:	print " ".join(SYSEXSAVE)
			writesysex(SYSEXSAVE)	# write the sysex to the file
			SYSEX = False
	else:					# extract the midi commands and send them
		if PRINT:	print mido.parse(data[2:5])
		sendmidi(mido.parse(data[2:5]))
		if len(data) > 5:
			if PRINT: 	print mido.parse(data[6:9])
			sendmidi(mido.parse(data[6:9]))
		if len(data) > 9:
			if PRINT: 	print mido.parse(data[10:13])
			sendmidi(mido.parse(data[10:13]))
		if len(data) > 13:
			if PRINT: 	print mido.parse(data[14:17])
			sendmidi(mido.parse(data[14:17]))
	
# ==========================================================================
# Initialisation  -------
# =======================

FILE = open(MODECONFIGFILE,'r')
MODE = (FILE.readline()).replace("\n","")
FILE.close()

FILE = open(BTADDRESSFILE,'r')
BTADDRESS = (FILE.readline()).replace("\n","")
FILE.close()

FILE = open(SYNTHPORTFILE,'r')
SYNTHPORT = (FILE.readline()).replace("\n","")
FILE.close()

FILE = open(NOTEOFFFILE,'r')
N = (FILE.readline()).replace("\n","")
FILE.close()

if N == "RUN":
	NOTEOFF = True
else:	
	NOTEOFF = False

FILE = open(BUTTONSFILE,'r')
N = (FILE.readline()).replace("\n","")
FILE.close()

if N == "RUN":
	BUTTONS = True
else:	
	BUTTONS = False

# if the first GPIO button is on at startup - assume they aren't connected
#if BUTTONS:
#	if GPIO.input(GINPUTS[0]) == 0:
#		BUTTONS = False
#
# turn off all outputs on startup
#for m in GOUTPUTS:
#	GPIO.output(m,0)


SYSEX = False
HELDMSG = mido.Message('note_on', channel=0, note=60, velocity=0)	# dummy first mesage for "note off"


# find the synth/virtual/USB midi ports and connect to them

INNOTSET = True		# to make sure only one connection is made
OUTNOTSET = True	# ditto
for PORT in mido.get_output_names():
	if PRINT: print PORT
	if OUTNOTSET and SYNTHPORT in PORT :
		OUTPORT = mido.open_output( PORT)
		OUTNOTSET = False
		if PRINT:	print "Midi output port opened - ",PORT
	if EWIPORT in PORT:
		USBOUTPORT = mido.open_output(PORT)
		if PRINT:	print "EWI-USB input port opened - ",PORT
for PORT in mido.get_input_names():
	if PRINT: print PORT
	if INNOTSET and SYSEXPORT in PORT:
		INPORT = mido.open_input(PORT)
		INNOTSET = False
		if PRINT:	print "Midi input port opened - ",PORT
	if EWIPORT in PORT:
		USBINPORT = mido.open_input(PORT)
		if PRINT:	print "EWI-USB input port opened - ",PORT

#if MODE == "BT":
#	# Connect to the udbt01
#	p = btle.Peripheral( BTADDRESS, "random" )
#	p.withDelegate( MyDelegate() )
#
#	# Enable BT notifications - handle for notifications is decimal 28
#	p.writeCharacteristic(28, "\x01\x00", False) 



# read the ewi config
readEWI()

FIRSTTIME = True
CHKPRESETS = True

#===================
# Main loop --------
#===================

while True:
#	if MODE == "BT":
#		if p.waitForNotifications(1.0):
#	        # handleNotification() was called
#        		continue
#	else:

	for m in USBINPORT.iter_pending():
		if m.type == "sysex":
			MIDI = m.hex().split()		# create a list variable
			writesysex(MIDI)
		else:
			sendmidi(m)

	# first time through, the EWI has been queried, now update stuff
	if FIRSTTIME:
		time.sleep(0.5)
		configSYNTH()
		FIRSTTIME = False
	
	# if a preset check is required 					
	if CHKPRESETS:
		time.sleep(0.5)
		readPRESETS()
		CHKPRESETS = False

	# Now check for
	# local MIDI messages to read/configure the EWI 
	time.sleep(0.02)

	for m in INPORT.iter_pending():
		if m.note == 64:	# This is a dummy message to say "Read the EWI"
			readEWI()
		if m.note == 65:	# This is a dummy message to say "Write new config to the EWI"
			configEWI(0)
			readEWI()
			configSYNTH()
			CHKPRESETS = True
		if m.note == 66:	# This is a dummy message to say "Write preset 1 to the EWI"
			configEWI(1)
			readEWI()
			configSYNTH()
			CHKPRESETS = True
		if m.note == 67:	# This is a dummy message to say "Write preset 2 to the EWI"
			configEWI(2)
			readEWI()
			configSYNTH()
			CHKPRESETS = True
		if m.note == 68:	# This is a dummy message to say "Write preset 3 to the EWI"
			configEWI(3)
			readEWI()
			configSYNTH()
			CHKPRESETS = True
		if m.note == 69:	# This is a dummy message to say "Write preset 4 to the EWI"
			configEWI(4)
			readEWI()
			configSYNTH()
			CHKPRESETS = True


	#Check Preset buttons, and load a preset if pressed


#	if BUTTONS:
#		for n in range(0,len(GINPUTS)):
#			if GPIO.input(GINPUTS[n]) == 0:
#				if PRINT: print "GPIO "+str(n+1)+" is on"
#
#				# turn on all LEDs to indicate that the command is accepted
#				for m in GOUTPUTS:
#					GPIO.output(m,1)
#
#				# now check if preset 1 and 4 are pressed together = shutdown
#				if n == 0 and GPIO.input(GINPUTS[3]) == 0:
#					os.system("sudo poweroff")
#
#				# turn off all LEDs after a short time on
#				time.sleep(0.5)
#				for m in GOUTPUTS:
#					GPIO.output(m,0)
#
#				# if a button was pressed, load the config
#				configEWI(n+1)
#				# then check it was loaded
#				readEWI()
#				CHKPRESETS = True
#
#===================
# End of Main loop -
#===================
 	


#GPIO.cleanup()



