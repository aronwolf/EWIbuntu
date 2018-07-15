#!/bin/bash
# starts and stops the router program
# controlled by a status file set by the web frontend

RUNOLD="STOP"
sleep 5

while true
	do
		RUN=`cat /home/aron/ewi/data/status.txt`
		if [ "$RUN" != "$RUNOLD" ]
			then
			if [ "$RUN" = "RUN" ]
				then
				/home/aron/ewi/scripts/ewipi.sh start
				else
				/home/aron/ewi/scripts/ewipi.sh stop
				sleep 4
				fi
			fi
		
		RUNOLD=$RUN

	sleep 1
	done
