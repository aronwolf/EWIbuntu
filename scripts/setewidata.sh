#!/bin/bash
# This sends a MIDI note to the router.py control program to
# initiate a writing of a new configuration to the EWI

# find the midi port for the virtual port

PRESET=$1
LIST=`amidi -l |grep "Virtual Raw"`
set -- $LIST
VMIDI=$2

if [ "VMIDI" != "" ]
	then
		if [ $PRESET == 0 ]
			then
			# send enable request (a dummy note-on)
			amidi -p $VMIDI -S "9A 41 00"
			fi
		if [ $PRESET == 1 ]
			then
			# send enable request (a dummy note-on)
			amidi -p $VMIDI -S "9A 42 00"
			fi
		if [ $PRESET == 2 ]
			then
			# send enable request (a dummy note-on)
			amidi -p $VMIDI -S "9A 43 00"
			fi
		if [ $PRESET == 3 ]
			then
			# send enable request (a dummy note-on)
			amidi -p $VMIDI -S "9A 44 00"
			fi
		if [ $PRESET == 4 ]
			then
			# send enable request (a dummy note-on)
			amidi -p $VMIDI -S "9A 45 00"
			fi
		sleep 3
	fi
