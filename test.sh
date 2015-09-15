
/bin/echo -e "$(cat alloff.echo)" > /dev/udp/192.168.2.219/56700
/bin/echo "$(cat alloff.echo)" > /dev/udp/192.168.2.219/56700

/bin/echo "$(cat alloff.echo)" | nc -u 192.168.2.255 56700