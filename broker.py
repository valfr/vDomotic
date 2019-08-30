#!/usr/bin/env python3
from datetime import datetime
import paho.mqtt.client as mqtt
from systemd import journal
import json

global devicesXIAOMIdoorSensors
global devicesXIAOMImotionSensors
global devicesXIAOMImotionSensorsv2
global devicesSHELLYht
global devicesSHELLYswitch25
global shellyHistory
global shellyCompteur


def on_connect(client, userdata, flags, rc):
	connectionMsg = "VALFR BROKER Connected with result code "+str(rc)+"\n"
	#print(connectionMsg)
	journal.write(connectionMsg)
	client.subscribe("#")
	subscribeMsg = "VALFR BROKER subscribe to #\n"
	journal.write(subscribeMsg)
	fichierLog = open("/mnt/ram/broker.txt", "a")
	fichierLog.write(connectionMsg)
	fichierLog.write(subscribeMsg)
	fichierLog.close()

def on_message(client, userdata, message):
	global devicesXIAOMIdoorSensors
	global devicesXIAOMImotionSensors
	global devicesXIAOMImotionSensorsv2
	global devicesSHELLYht
	global devicesSHELLYswitch25
	global shellyHistory
	global shellyCompteur
	#print("received message =",str(message.payload.decode("utf-8")))
	#print("message topic=",message.topic)
	#print("message qos=",message.qos)
	#print("message retain flag=",message.retain)
	#LOG-FILE-RAM
	fichierLog = open("/mnt/ram/broker.txt", "a")
	fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "$BROKER$" + message.topic + "$" + str(message.payload.decode("utf-8")) + "\n")
	fichierLog.close()
	#LOG-SERVICE
	#journal.write("VALFRBROKER$" + message.topic + "$" + str(message.payload.decode("utf-8")))
	#WORK
	#SHELLIES-ON
	for deviceID, deviceName in devicesSHELLYht.items():
		if message.topic == "shellies/"+deviceID+"/sensor/temperature":
			shellyHistory = str(message.payload.decode("utf-8"))
			shellyCompteur = str(message.payload.decode("utf-8"))
		if message.topic == "shellies/"+deviceID+"/sensor/humidity":
			shellyHistory = shellyHistory + " - " + str(message.payload.decode("utf-8"))
			shellyCompteur = shellyCompteur + "-" + str(message.payload.decode("utf-8"))
		if message.topic == "shellies/"+deviceID+"/sensor/battery":
			shellyHistory = shellyHistory + " - " + str(message.payload.decode("utf-8"))  
			fichier = open("/mnt/ram/history.txt", "a")
			fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " + shellyHistory + "\n")
			fichier.close()
			shellyHistory = ""
			shellyCompteur = shellyCompteur + "-" + datetime.today().strftime('%d/%m %H:%M')
			fichier = open("/mnt/ram/compteur.txt", "w")
			fichier.write(shellyCompteur)
			fichier.close()
			fichierLog = open("/mnt/ram/broker.txt", "a")
			fichierLog.write("Work$SHELLY$" + shellyCompteur+ "\n")
			fichierLog.close()
			shellyCompteur = ""
	#SHELLIES-OFF
	
	
	#XIAOMI-ON
	#Devices list  
	#devicesXIAOMIdoorSensors = { '0x00158d0002435273':'bureau','0x00158d00027b495f':'porte' }
	#devicesXIAOMImotionSensors = { '0x00158d000222fabd':'motion' }
	#DOOR SENSORS work 
	for deviceID, deviceName in devicesXIAOMIdoorSensors.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['contact']).lower()
			if deviceState == "true":
				fichier = open("/mnt/ram/"+deviceID+"_lastClose.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "false":		
				fichier = open("/mnt/ram/"+deviceID+"_lastOpen.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			fichierLog = open("/mnt/ram/history.txt", "a")
			fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " +deviceName+" - close="+deviceState+"\n")
			fichierLog.close()
			fichierLog = open("/mnt/ram/broker.txt", "a")
			fichierLog.write("Work$XIAOMI$door$"+deviceName+"$"+deviceState+"\n")
			fichierLog.close()
	#MOTION SENSORS work 
	for deviceID, deviceName in devicesXIAOMImotionSensors.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['occupancy']).lower()
			if deviceState == "true":
				fichier = open("/mnt/ram/"+deviceID+"_lastDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "false":
				fichier = open("/mnt/ram/"+deviceID+"_lastEndOfDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			fichierLog = open("/mnt/ram/history.txt", "a")
			fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " +deviceName+" - motion="+deviceState+"\n")
			fichierLog.close()
			fichierLog = open("/mnt/ram/broker.txt", "a")
			fichierLog.write("Work$XIAOMI$motion$"+deviceName+"$"+deviceState+"\n")
			fichierLog.close()
	#MOTION SENSORS V2 - luminosity work 
	for deviceID, deviceName in devicesXIAOMImotionSensorsv2.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['occupancy']).lower()
			deviceLuminosity = str(python_obj['illuminance']).lower()
			if deviceState == "true":
				fichier = open("/mnt/ram/"+deviceID+"_lastDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "false":
				fichier = open("/mnt/ram/"+deviceID+"_lastEndOfDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			fichierLog = open("/mnt/ram/history.txt", "a")
			fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " +deviceName+" - motion="+deviceState+"\n")
			fichierLog.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " +deviceName+" - luminosity="+deviceLuminosity+"\n")
			fichierLog.close()
			fichierLog = open("/mnt/ram/broker.txt", "a")
			fichierLog.write("Work$XIAOMI$motionV2$"+deviceName+"$"+deviceState+"\n")
			fichierLog.write("Work$XIAOMI$motionV2$"+deviceName+"$"+deviceLuminosity+"\n")
			fichierLog.close()
	#XIAOMI-OFF


#MAIN
global devicesXIAOMIdoorSensors
global devicesXIAOMImotionSensors
global devicesXIAOMImotionSensorsv2
global devicesSHELLYht
global devicesSHELLYswitch25
devicesXIAOMIdoorSensors = dict()
devicesXIAOMImotionSensors = dict()
devicesXIAOMImotionSensorsv2 = dict()
devicesSHELLYht = dict()
devicesSHELLYswitch25 = dict()

startupMsg = "VALFR BROKER v1.5 starting up at " + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "\n"
journal.write(startupMsg)
fichierLog = open("/mnt/ram/broker.txt", "a")
fichierLog.write(startupMsg)
with open("/home/data/devices.txt") as f :
	for line in f :
		line = line.replace("\n","")
		data = line.split('!')
		if data[0] == "XIAOMIdoor":
			devicesXIAOMIdoorSensors[data[1]]=data[2]
		if data[0] == "XIAOMImotion":
			devicesXIAOMImotionSensors[data[1]]=data[2]
		if data[0] == "XIAOMImotionv2":
			devicesXIAOMImotionSensorsv2[data[1]]=data[2]
		if data[0] == "SHELLYht":
			devicesSHELLYht[data[1]]=data[2]
		if data[0] == "SHELLYswitch25":
			devicesSHELLYswitch25[data[1]]=data[2]
fichierLog.write(str(len(devicesXIAOMIdoorSensors))+" 'XIAOMIdoor' devices loaded\n")
fichierLog.write(str(len(devicesXIAOMImotionSensors))+" 'XIAOMImotion' devices loaded\n")
fichierLog.write(str(len(devicesXIAOMImotionSensorsv2))+" 'XIAOMImotionV2' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYht))+" 'SHELLYht' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYswitch25))+" 'SHELLYswitch25' devices loaded\n")
fichierLog.close()
client = mqtt.Client()
client.connect("localhost",1883,60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
