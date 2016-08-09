#!/bin/bash
set -e

CFG="-r 10:server1:6000 -r 20:server2:6000 -r 30:server3:6000"
if [ "$ROLE" = 'client' ]; then
	sleep 15
	exec bin/client -k $CLIENTKEY $CFG 2>> $LOG
elif [ "$ROLE" = 'server' ]; then
	sleep 10
	exec bin/server -i $SERVERID $CFG 2>> $LOG
else
	echo "please specify either 'client' or 'server' in \$ROLE"
	exit 1
fi
