#!/usr/bin/python

#Gets and sets data in the JV1010
#needs Midi adapter (CH345)

import mido
import time

SYNTHPORTFILE = "/home/aron/ewi/data/synthport.txt"       # the path to the file with the synth port name
SENDMIDI = True
PRINT = False


FILE = open(SYNTHPORTFILE,'r')
SYNTHPORT = (FILE.readline()).replace("\n","")
FILE.close()


# USE HEX - Respose will be in decimal
ID = ['41','10','6A']		# the ID details of the JV-1010
RQ = ['11']			# 11 to request data
DT = ['12']			# 12 to send data
ADDRESS1 = ['11']		# User patch = 11
ADDRESS2 = ['0C']        	# Patch number -1
ADDRESS3 = ['00','27']        	# the address of the item
SIZE1 = ['00','00','00']	# usually just zeros
SIZE2 = ['04']			# the number of items of info req'd 
#VALUE = ['01', '01', '01', '01', '01', '09']	# the value(s) to set item(s) to
VALUE = ['00']

DATA = ID+RQ+ADDRESS1+ADDRESS2+ADDRESS3+SIZE1+SIZE2	# enable to request data
#DATA = ID+DT+ADDRESS1+ADDRESS2+ADDRESS3+VALUE	# enable to send data
if SENDMIDI:
        INNOTSET = True         # to make sure only one connection is made
        OUTNOTSET = True        # ditto
        for PORT in mido.get_output_names():
                if PRINT: print PORT
                if OUTNOTSET and SYNTHPORT in PORT :
                        OUTPORT = mido.open_output( PORT)
                        INPORT = mido.open_input( PORT)
                        OUTNOTSET = False
			INNOTSET = False
                        print "Midi ports opened - ",PORT
	if OUTNOTSET:
		print "Port opening failed"
	else:
        	for INMSG in INPORT.iter_pending(): 	# clear port
			print "clearing port"
SUM = 0
for N in range (0,len(DATA)):

	DATA[N] = int(DATA[N],16)	# convert hex to int. Data must be in integers
	if N > 3:
		SUM += DATA[N]
CSUM = 128 - SUM % 128		# calculate the checksum
DATA.append(CSUM)
OUTMSG = mido.Message('sysex', data=DATA)
OUTPORT.send(OUTMSG)
print "Sent:     ",OUTMSG


for N in range (0,3):
	time.sleep(0.5)
        for INMSG in INPORT.iter_pending():
                print "Received: ",INMSG	 
INPORT.close()
OUTPORT.close()
