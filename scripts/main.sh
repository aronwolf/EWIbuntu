#!/bin/bash
# starts and stops the router program
# controlled by a status file set by the web frontend

RUNOLD="STOP"
sleep 5

while true
	do
		RUN=`cat ../data/status.txt`
		if [ "$RUN" != "$RUNOLD" ]
			then
			if [ "$RUN" = "RUN" ]
				then
				../scripts/ewipi.sh start
				else
				../scripts/ewipi.sh stop
				sleep 4
				fi
			fi
		
		RUNOLD=$RUN

	sleep 1
	done
