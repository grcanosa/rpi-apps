#!/bin/sh
### BEGIN INIT INFO
# Provides:          dashlauncher.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO


# To install make a symlink in /etc/init.d with sudo
# Then: sudo update-rc.d dashlauncher.sh defaults
case "$1" in

  stop)
    echo "Stop Dash Scanner"
    killall dash_scanner.py
    #kill "`cat /tmp/telegrambots.pid`"
    sleep 5
    killall -9 dash_scanner.py
    #killall -9 multilauncher.py
    ;;
  start)
    symlink=$(readlink -f "$0")
	  path=$(dirname $symlink)
    . $path/pass_info.sh
    #echo "Creating folder in $path/../data/log"
    #mkdir -p $path/../data/log
    $path/dash_scanner.py $path/piropos.txt $HOMEASSISTANTPASS $HOMEASSISTANTIP $FAIRYMAC &
    #echo $! > /tmp/telegrambots.pid
    ;;
  restart)
    $0 stop
    sleep 2
    $0 start
    ;;
  *)
    echo "usage: $0 { start | stop | restart }" >&2
        exit 1
        ;;
esac

: