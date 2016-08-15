#!/bin/sh
# WebIOPi unistall script
set -e
WEBIOPI_PATH=/etc/webiopi
WEBIOPI_UNINSTALL_PATH=${WEBIOPI_PATH}/uninstall
service cron stop
service webiopi stop
systemctl disable webiopi

#webiopi python code removed
cat "${uninstallpath}/installed_components" | xargs rm -rf

rm -rf /usr/share/webiopi
rm -rf /usr/bin/webiopi
rm -rf /etc/init.d/webiopi
rm -rf /usr/bin/webiopi-passwd

#remove folder path
rm -rf "${WEBIOPI_PATH}"
service cron start