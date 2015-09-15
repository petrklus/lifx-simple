# lifx-simple
Controlling LiFX bulbs using command line. Supports colour setting with 2.0 firmware

Supported actions
-----
Colour setting via including hue, saturation, brightness and temperature. Sends packet multiple times based on the retries defined in the file itself. Hue ranges between 0-360, saturation and brightness between 0 and 100 and temperature between 2500 and 9000.

Example usage
----

Setting hue to 120, saturation to 50, brightness to 100 and temperature to 3500K
```./set_colour.py 192.168.2.222 120 50 100 3500```


Requirements
-----
- Python 2.7
- Knowledge of the IP address of the bulb. You can configure your router to assign static IPs to the bulbs, this eliminates any need of discovery

Tested on Linux (raspberry PI) and Mac OS 10.9


Resources
-----
- http://lan.developer.lifx.com/docs/
- https://community.lifx.com/t/building-a-lifx-packet/59
- https://community.lifx.com/t/controlling-lights-with-bash/31
