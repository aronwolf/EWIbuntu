#!/bin/bash
# runs the midi router program
# restarts it if it crashes


while true
	do
	nice -20 /home/aron/ewi/scripts/router.py
	sleep 5
	done
