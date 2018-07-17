#!/usr/bin/python
import binascii
import mido
import time
import os
import sys

pitches = {48:'C',
49:'C#',
50:'D',
51:'Eb',
52:'E',
53:'F',
54:'F#',
55:'G',
56:'G#',
57:'A',
58:'Bb',
59:'B',
60:'C',
61:'C#',
62:'D',
63:'Eb',
64:'E',
65:'F',
66:'F#',
67:'G',
68:'G#',
69:'A',
70:'Bb',
71:'B',
72:'C',
73:'C#',
74:'D',
75:'Eb',
76:'E',
77:'F',
78:'F#',
79:'G',
80:'G#',
81:'A',
82:'Bb',
83:'B',
84:'C',
85:'C#',
86:'D',
87:'Eb',
88:'E',
89:'F',
90:'F#',
91:'G',
92:'G#',
93:'A',
94:'Bb',
95:'B',
96:'C',
97:'C#',
98:'D',
99:'Eb',
100:'E',
101:'F',
102:'F#',
103:'G',
104:'G#',
105:'A',
106:'Bb',
107:'B',
108:'C',
109:'C#'
}


octave1 = {48:72,
48:72,
49:73,
50:74,
51:75,
52:76,
53:77,
54:78,
55:79,
56:80,
57:81,
58:82,
59:83,
60:72,
61:73,
62:74,
63:75,
64:76,
65:77,
66:78,
67:79,
68:80,
69:81,
70:82,
71:83,
72:72,
73:73,
74:74,
75:75,
76:76,
77:77,
78:78,
79:79,
80:80,
81:81,
82:82,
83:83,
84:72,
85:73,
86:74,
87:75,
88:76,
89:77,
90:78,
91:79,
92:80,
93:81,
94:82,
95:83,
96:72,
97:73,
98:74,
99:75,
100:76,
101:77,
102:78,
103:79,
104:80,
105:81,
106:82,
107:83,
108:72,
109:73}

octave2 = {48:84,
49:85,
50:86,
51:87,
52:88,
53:89,
54:90,
55:91,
56:92,
57:93,
58:94,
59:95,
60:84,
61:85,
62:86,
63:87,
64:88,
65:89,
66:90,
67:91,
68:92,
69:93,
70:94,
71:95,
72:84,
73:85,
74:86,
75:87,
76:88,
77:89,
78:90,
79:91,
80:92,
81:93,
82:94,
83:95,
84:84,
85:85,
86:86,
87:87,
88:88,
89:89,
90:90,
91:91,
92:92,
93:93,
94:94,
95:95,
96:84,
97:85,
98:86,
99:87,
100:88,
101:89,
102:90,
103:91,
104:92,
105:93,
106:94,
107:95,
108:84,
109:85}

# Settings
PRINT = True		# set to True to enable printing to screen (for debugging)

SYSEXPORT = "Vir"	# the port for receiving Sysex messages.
EWIPORT = "EWI"		# the port the EWI_USB appears on if using USB not BT.

# FILE LOCATIONS

SYNTHPORTFILE = "../data/synthport.txt" 	# the path to the file with the name of the synth port
NOTEOFFFILE = "../data/noteoff.txt" 		# the path to the file to turn on the noteoff function
BUTTONSFILE = "../data/buttons.txt" 		# the path to the file to turn on GPIO buttons function
EWIDATAFILE = "../data/ewidata.txt" 		# the path to the file with the config data read from the EWI 
EWICONFIGFILE = "../data/sendewidata.txt"	# the path to the file with the new config to be sent to the EWI
P1CONFIGFILE = "../data/preset1.txt"		# the path to the file with the preset config to be sent to the EWI
P2CONFIGFILE = "../data/preset2.txt"		# the path to the file with the preset config to be sent to the EWI
P3CONFIGFILE = "../data/preset3.txt"		# the path to the file with the preset config to be sent to the EWI
P4CONFIGFILE = "../data/preset4.txt"		# the path to the file with the preset config to be sent to the EWI
MODECONFIGFILE = "../data/mode.txt"		# the path to the BT/USB mode setting file
BTADDRESSFILE = "../data/btaddress.txt"	# the path to the UD-BT01 Bluetooth address file
FINETUNEFILE = "../data/finetune.txt"		# the path to the synth fine tune setting file

#Uncomment the following line if you want to use RtMidi (You will need to install RtMidi yourself).
mido.set_backend('mido.backends.rtmidi')

usleep = lambda x: time.sleep(x/1000000.0)	# introducing microseconds sleep times


# =====================================================================
# Functions-----------------------
# ================================

def readEWI():

	try: 
		os.remove(EWIDATAFILE)
	except:
		if PRINT: print "file already deleted"

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
		
	if MSG.type == 'note_on' and MSG.velocity <100:
		MSG.note = octave1[MSG.note]
		MSG.velocity = 100	
		print "note={0}4 velocity={1}".format(pitches[MSG.note], MSG.velocity)	
	elif MSG.type == 'note_on' and MSG.velocity >=100:
		MSG.note = octave2[MSG.note]
		MSG.velocity = 100	
		print "note={0}5 velocity={1}".format(pitches[MSG.note], MSG.velocity)	
	
	OUTPORT.send(MSG) 

	# If the MIDI message is for a new note-on,
	# the next section adds an extra "note-off" for the previous note played
	# This is needed because the EWI misses note-off commands occasionally.
	if NOTEOFF:
        	if MSG.type == 'note_on' and MSG.velocity >0:
			if MSG.note != HELDMSG.note:
				usleep(500.0) # introduce a small delay
				OUTPORT.send(HELDMSG.copy(velocity=0))
				#if PRINT: print "Noteoff sent for note "+str(HELDMSG.note)
				HELDMSG = MSG	
	return

# =========================================================================
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


# read the ewi config
readEWI()

FIRSTTIME = True
CHKPRESETS = True

#===================
# Main loop --------
#===================

while True:
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


#===================
# End of Main loop -
#===================
 	


