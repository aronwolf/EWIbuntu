#!/bin/bash
# This sends a MIDI note to the router.py control program to
# initiate a read of the EWI config

# find the midi port for the virtual port
LIST=`amidi -l |grep "Virtual Raw"`
set -- $LIST
VMIDI=$2

if [ "VMIDI" != "" ]
	then
		# send enable request (a dummy note-on)
		amidi -p $VMIDI -S "9A 40 00"
	fi
