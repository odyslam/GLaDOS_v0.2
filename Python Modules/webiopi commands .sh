sudo webiopi -d -c /etc/webiopi/config start webiopi in debug mode (log to console same for wheezy & Jessie

ctrl+c close webiopi service that is running in debug mode

sudo systemctl start webiopi  previously  sudo /etc/init.d/webiopi start = start webiopi service in background .. log to var/log/webiopi

sudo systemctl stop webiopi  previously  sudo /etc/init.d/webiopi stop = stop webiopi service in background

sudo systemctl enable webiopi  previously  sudo update-rc.d webiopi defaults = start at boot

sudo systemctl disable webiopi  previously  sudo update-rc.d webiopi remove = disable start at boot

tail -f -n 50 /var/log/webiopi   view running log on console in background mode