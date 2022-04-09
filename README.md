# vDomotic (work in progress)
Light way domotic with MQTT &amp; Zigbee &amp; Wifi
Using local python script to manage all direct interaction between IOT Xiaomi & Shelly & Philips HUE

## best configuration
Raspberry Pi with Zigbee dongle
 Zigbee2mqtt
 Mosquitto
 Homebridge
  Shelly plugin
  Z2M plugin
 Broker daemon
 


# broker.py
This script is acting to distribute actions directly between devices.
You can acitvate a relay or turn on a light with this local python script (no need for external connectivity).
Work only with local Wifi (for shellies) + Zigbee (for Xiamo & HUE)

=> running as daemon
=> catch all MQTT request
=> generate action for sensors
=> output state can be write into file to request it with external website


# worker.py
=> running as daemon clock
=> launch action (minimum schedule is 1 second)



# Supported devices 

Broker

=> Shelly HT

=> Shelly 2.5 - Roller or Relay

=> Shelly Door Sensor

=> Xiaomi Door Sensor

=> Xiaomi Motion Sensor v1

=> Xiaomi Motion Sensor v2

=> Philips HUE lights

Worker

=> Shelly 2.5 - Roller

