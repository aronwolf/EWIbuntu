#!/bin/bash

# Checks the Bluetooth LE connection and adjusts
# the connection parameters to minimise latency


CTIME=5	# Seconds between checks
OLDHANDLE=0

while true
	do
	sleep $CTIME
	STATUS=`sudo hcitool con`	#to find the handle number
	#echo $STATUS
	set -- $STATUS
	HANDLE=`echo ${6}`
	#echo $HANDLE
	if [ $HANDLE -gt 0 ] && [ $HANDLE != $OLDHANDLE ]
		then		# we have a valid handle and the connection is not the same
		sudo hcitool lecup --handle $HANDLE --min 6 --max 10 --latency 0 --timeout 500
		OLDHANDLE=$HANDLE
	fi

	done
