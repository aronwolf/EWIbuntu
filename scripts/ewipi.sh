#!/bin/bash

# Script to launch the various programs for EWI-USB with USB or Bluetooth adapter.


# Set parameters
MODE=`cat ../data/mode.txt`		# Bluetooth or USB mode

export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket

case $1 in

  start )
	# just in case something was running, kill it and clean up

    	killall btcon.sh
    	killall router.sh
    	killall router.py
	

	# Start the midi router program
	../scripts/router.sh &
		
	if [ $MODE == "BT" ]
		then
		# Start the Bluetooth connection parameter setting program
		../scripts/btcon.sh &
		fi
		
    # check if all is running
 	sleep 1
   	if pgrep router.py
    		then
      		echo Router is running.
    	else
      		echo Router is not running.
    	fi

    ;;

  stop )
    	killall btcon.sh
    	killall router.sh
    	killall router.py

    	echo Router stopped.
    ;;

  * )
    	echo Please specify start or stop...
    ;;
esac

