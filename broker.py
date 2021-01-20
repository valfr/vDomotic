#!/usr/bin/env python3
from datetime import datetime
import paho.mqtt.client as mqtt
from systemd import journal
import json
import requests

global pathLogs
global pathData              
global devicesXIAOMIdoorSensors
global devicesXIAOMImotionSensors
global devicesSHELLYht
global devicesSHELLYdw
global devicesSHELLYswitch25
global devicesSHELLYrelay25r1
global devicesSHELLYrelay25r1target
global devicesSHELLYrelay25r2
global devicesSHELLYrelay25r2target
global devicesVALFRpi
global devicesHUEwhite
global realtimeHUEwhite
global shellyHistory
global shellyCompteur


def on_connect(client, userdata, flags, rc):
	connectionMsg = "VALFR BROKER Connected with result code "+str(rc)+"\n"
	journal.write(connectionMsg)
	client.subscribe("#")
	subscribeMsg = "VALFR BROKER subscribe to #\n"
	journal.write(subscribeMsg)
	fichierLog = open(pathLogs+"broker.txt", "a")
	fichierLog.write(connectionMsg)
	fichierLog.write(subscribeMsg)
	fichierLog.close()


def on_message(client, userdata, message):
	global pathLogs
	global pathData                 
	global devicesXIAOMIdoorSensors
	global devicesXIAOMImotionSensors
	global devicesSHELLYht
	global devicesSHELLYdw
	global devicesSHELLYswitch25
	global devicesSHELLYrelay25r1
	global devicesSHELLYrelay25r1target
	global devicesSHELLYrelay25r2
	global devicesSHELLYrelay25r2target
	global devicesVALFRpi
	global devicesHUEwhite
	global realtimeHUEwhite
	global shellyHistory
	global shellyCompteur
	#LOG-FILE-RAM
	#fichierLog = open(pathLogs+"broker.txt", "a")
	#fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "$BROKER$" + message.topic + "$" + str(message.payload.decode("utf-8")) + "\n")
	#fichierLog.close()
	#LOG-SERVICE
	#journal.write("VALFRBROKER$" + message.topic + "$" + str(message.payload.decode("utf-8")))
	#WORK
	#SHELLIES-ON
	#SHELLIES-HumidityTemperature
	for deviceID, deviceName in devicesSHELLYht.items():
		if message.topic == "shellies/"+deviceID+"/sensor/temperature":
			shellyHistory = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_temperature.txt", "w")
			fichier.write(str(message.payload.decode("utf-8")))
			fichier.close()
		if message.topic == "shellies/"+deviceID+"/sensor/humidity":
			shellyHistory = shellyHistory + " - " + str(message.payload.decode("utf-8"))
			#shellyCompteur = shellyCompteur + "-" + str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_humidity.txt", "w")
			fichier.write(str(message.payload.decode("utf-8")))
			fichier.close()
		if message.topic == "shellies/"+deviceID+"/sensor/battery":
			fichier = open(pathData+deviceID+"_datetime.txt", "w")
			fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
			fichier.close()
			shellyHistory = shellyHistory + " - " + str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_history.txt", "a")
			fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " + shellyHistory + "\n")
			fichier.close()
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$SHELLY$" + shellyHistory+ "\n")
			fichierLog.close()
			shellyHistory = ""
	#SHELLIES-DoorW
	for deviceID, deviceName in devicesSHELLYdw.items():
		if message.topic == "shellies/"+deviceID+"/sensor/state":
			deviceState = str(message.payload.decode("utf-8"))
			if deviceState == "close":
				fichier = open(pathData+deviceID+"_lastClose.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "open":
				fichier = open(pathData+deviceID+"_lastOpen.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$SHELLIES$door$"+deviceName+"$"+deviceState+"\n")
			fichierLog.close()
		if message.topic == "shellies/"+deviceID+"/sensor/battery":
			deviceBattery = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_battery.txt", "w")
			fichier.write(deviceBattery)
			fichier.close()
		if message.topic == "shellies/"+deviceID+"/sensor/lux":
			deviceLuminosity = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_luminosity.txt", "w")
			fichier.write(deviceLuminosity)
			fichier.close()
	#SHELLIES-Relay25s
	for deviceID, deviceName in devicesSHELLYrelay25r1.items():
		if message.topic == "shellies/"+deviceID+"/input/0":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				client.publish("zigbee2mqtt/"+devicesSHELLYrelay25r1target[deviceID]+"/set", '{"brightness": '+realtimeHUEwhite[devicesSHELLYrelay25r1target[deviceID]]+'}', qos=0, retain=False)
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25$"+deviceName+"$"+deviceInput+"$Allumer vers "+realtimeHUEwhite[devicesSHELLYrelay25r1target[deviceID]]+"\n")
				fichierLog.close()
		if message.topic == "shellies/"+deviceID+"/longpush/0":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				client.publish("zigbee2mqtt/"+devicesSHELLYrelay25r1target[deviceID]+"/set", '{"brightness": 0}', qos=0, retain=False)
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25$"+deviceName+"$"+deviceInput+"$Eteindre\n")
				fichierLog.close()
	for deviceID, deviceName in devicesSHELLYrelay25r2.items():
		if message.topic == "shellies/"+deviceID+"/input/1":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				client.publish("zigbee2mqtt/"+devicesSHELLYrelay25r2target[deviceID]+"/set", '{"brightness": '+realtimeHUEwhite[devicesSHELLYrelay25r2target[deviceID]]+'}', qos=0, retain=False)
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25$"+deviceName+"$"+deviceInput+"$Allumer vers "+realtimeHUEwhite[devicesSHELLYrelay25r2target[deviceID]]+"\n")
				fichierLog.close()
		if message.topic == "shellies/"+deviceID+"/longpush/1":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				client.publish("zigbee2mqtt/"+devicesSHELLYrelay25r2target[deviceID]+"/set", '{"brightness": 0}', qos=0, retain=False)
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25$"+deviceName+"$"+deviceInput+"$Eteindre\n")
				fichierLog.close()
	#SHELLIES-OFF

	#VALFRPI-ON
	for deviceID, deviceName in devicesVALFRpi.items():
		if message.topic == "valfrpi/"+deviceID+"/temperature":
			piTemperature = str(message.payload.decode("utf-8")) + "-" + datetime.today().strftime('%d/%m %H:%M')
			fichier = open(pathData+deviceID+"_temperature.txt", "w")
			fichier.write(str(message.payload.decode("utf-8")))
			fichier.close()
			fichier = open(pathData+deviceID+"_datetime.txt", "w")
			fichier.write(datetime.today().strftime('%d/%m %H:%M'))
			fichier.close()
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$valfrpi$" + piTemperature + "\n")
			fichierLog.close()
	#VALFRPI-OFF


	#XIAOMI-ON
	#DOOR SENSORS work
	for deviceID, deviceName in devicesXIAOMIdoorSensors.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['contact']).lower()
			if deviceState == "true":
				fichier = open(pathData+deviceID+"_lastClose.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "false":
				fichier = open(pathData+deviceID+"_lastOpen.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			deviceBattery = str(python_obj['battery']).lower()
			fichier = open(pathData+deviceID+"_battery.txt", "w")
			fichier.write(deviceBattery)
			fichier.close()
			fichierLog = open(pathLogs+"history.txt", "a")
			fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " +deviceName+" - close="+deviceState+"\n")
			fichierLog.close()
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$XIAOMI$door$"+deviceName+"$"+deviceState+"\n")
			fichierLog.close()
	#MOTION SENSORS work
	for deviceID, deviceName in devicesXIAOMImotionSensors.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['occupancy']).lower()
			#sensor v2 with luminosity
			deviceLuminosity="99999999"
			if 'illuminance' in python_obj: 
				deviceLuminosity = str(python_obj['illuminance']).lower()
				fichier = open(pathData+deviceID+"_luminosity.txt", "w")
				fichier.write(deviceLuminosity)
				fichier.close()				 
			if deviceState == "true":
				fichier = open(pathData+deviceID+"_lastDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "false":
				fichier = open(pathData+deviceID+"_lastEndOfDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			deviceBattery = str(python_obj['battery']).lower()
			fichier = open(pathData+deviceID+"_battery.txt", "w")
			fichier.write(deviceBattery)
			fichier.close()
			fichierLog = open(pathLogs+"history.txt", "a")
			fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " +deviceName+" - motion="+deviceState+"\n")
			fichierLog.close()
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$XIAOMI$motion$"+deviceName+"$"+deviceState+"\n")
			fichierLog.write("Work$XIAOMI$luminosity$"+deviceName+"$"+deviceLuminosity+"\n")																	   
			fichierLog.close()
	#XIAOMI-OFF


	#HUE-ON
	#HUE WHITE work
	for deviceID, deviceName in devicesHUEwhite.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceBrightness = str(python_obj['brightness']).lower()
			fichier = open(pathData+deviceID+"_brightness.txt", "w")
			fichier.write(deviceBrightness)
			fichier.close()
			if deviceBrightness == "0" or deviceBrightness == "1":
				realtimeHUEwhite[deviceID]="75"
			elif deviceBrightness == "75":
				realtimeHUEwhite[deviceID]="150"
			elif deviceBrightness == "150":
				realtimeHUEwhite[deviceID]="254"
			else:
				realtimeHUEwhite[deviceID]="0"
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$HUE$white$"+deviceName+"$Brightness$"+deviceBrightness+"\n")
			fichierLog.close()
	#HUE-OFF



#MAIN
global pathLogs
global pathData        
global devicesXIAOMIdoorSensors
global devicesXIAOMImotionSensors
global devicesSHELLYht
global devicesSHELLYdw
global devicesSHELLYswitch25
global devicesSHELLYrelay25r1
global devicesSHELLYrelay25r1target
global devicesSHELLYrelay25r2
global devicesSHELLYrelay25r2target
global devicesVALFRpi
global devicesHUEwhite
global realtimeHUEwhite
devicesXIAOMIdoorSensors = dict()
devicesXIAOMImotionSensors = dict()
devicesSHELLYht = dict()
devicesSHELLYdw = dict()
devicesSHELLYswitch25 = dict()
devicesSHELLYrelay25r1 = dict()
devicesSHELLYrelay25r1target = dict()
devicesSHELLYrelay25r2 = dict()
devicesSHELLYrelay25r2target = dict()
devicesVALFRpi = dict()
devicesHUEwhite = dict()
realtimeHUEwhite = dict()
pathLogs = "/mnt/ram/"
pathData = "/mnt/ram/"

startupMsg = "VALFR BROKER v2.3 starting up at " + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "\n"
journal.write(startupMsg)
fichierLog = open(pathLogs+"broker.txt", "a")
fichierLog.write(startupMsg)
with open("/home/data/devices.txt") as f :
	for line in f :
		line = line.replace("\n","")
		data = line.split('!')
		if data[0] == "XIAOMIdoor":
			devicesXIAOMIdoorSensors[data[1]]=data[2]
		if data[0] == "XIAOMImotion":
			devicesXIAOMImotionSensors[data[1]]=data[2]
		if data[0] == "SHELLYht":
			devicesSHELLYht[data[1]]=data[2]
		if data[0] == "SHELLYdw":
			devicesSHELLYdw[data[1]]=data[2]
		if data[0] == "SHELLYswitch25":
			devicesSHELLYswitch25[data[1]]=data[2]
		if data[0] == "SHELLYrelay25r1":
			devicesSHELLYrelay25r1[data[1]]=data[2]
			devicesSHELLYrelay25r1target[data[1]]=data[3]
		if data[0] == "SHELLYrelay25r2":
			devicesSHELLYrelay25r2[data[1]]=data[2]
			devicesSHELLYrelay25r2target[data[1]]=data[3]
		if data[0] == "valfrpi":
			devicesVALFRpi[data[1]]=data[2]
		if data[0] == "HUEwhite":
			devicesHUEwhite[data[1]]=data[2]
			realtimeHUEwhite[data[1]]="get"
fichierLog.write(str(len(devicesXIAOMIdoorSensors))+" 'XIAOMIdoor' devices loaded\n")
fichierLog.write(str(len(devicesXIAOMImotionSensors))+" 'XIAOMImotion' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYht))+" 'SHELLYht' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYdw))+" 'SHELLYdw' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYswitch25))+" 'SHELLYswitch25' devices loaded (roller mode)\n")
fichierLog.write(str(len(devicesSHELLYrelay25r1))+" 'SHELLYrelay25' devices loaded (relay 1)\n")
fichierLog.write(str(len(devicesSHELLYrelay25r2))+" 'SHELLYrelay25' devices loaded (relay 2)\n")
fichierLog.write(str(len(devicesVALFRpi))+" 'valfrpi' devices loaded\n")
fichierLog.write(str(len(devicesHUEwhite))+" 'HUEwhite' devices loaded\n")
fichierLog.close()
#starting up MQTT
client = mqtt.Client()
client.connect("localhost",1883,60)
client.on_connect = on_connect
client.on_message = on_message
#In-Real-Time sync & checking 
for key in realtimeHUEwhite:
	client.publish("zigbee2mqtt/"+key+"/get", '{"brightness": "0"}', qos=0, retain=False)
subscribeMsg = "VALFR BROKER In-RealTime devices checking\n"
journal.write(subscribeMsg)
fichierLog = open(pathLogs+"broker.txt", "a")
fichierLog.write(subscribeMsg)
fichierLog.close()
#Ready processing messages forever !
client.loop_forever()
