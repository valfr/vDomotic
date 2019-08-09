#!/usr/bin/env python3
from datetime import datetime
import paho.mqtt.client as mqtt
from systemd import journal
import json

global shellyHistory
global shellyCompteur
global toto

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
	#print("received message =",str(message.payload.decode("utf-8")))
	#print("message topic=",message.topic)
	#print("message qos=",message.qos)
	#print("message retain flag=",message.retain)
	#LOG
	maSortie = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "$BROKER$" + message.topic + "$" + str(message.payload.decode("utf-8")) + "\n"
	#LOG-FILE-RAM
	fichierLog = open("/mnt/ram/broker.txt", "a")
	fichierLog.write(maSortie)
	fichierLog.close()
	#LOG-SERVICE
	#journal.write("VALFRBROKER$" + message.topic + "$" + str(message.payload.decode("utf-8")))
	#WORK
	#SHELLIES-ON
	global shellyHistory
	global shellyCompteur
	if message.topic == "shellies/shellyht-E016D8/sensor/temperature":
		shellyHistory = str(message.payload.decode("utf-8"))
		shellyCompteur = str(message.payload.decode("utf-8"))
	if message.topic == "shellies/shellyht-E016D8/sensor/humidity":
		shellyHistory = shellyHistory + " - " + str(message.payload.decode("utf-8"))
		shellyCompteur = shellyCompteur + "-" + str(message.payload.decode("utf-8"))
	if message.topic == "shellies/shellyht-E016D8/sensor/battery":
		shellyHistory = shellyHistory + " - " + str(message.payload.decode("utf-8"))
		maSortie =  datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " + shellyHistory + "\n" 
		fichier = open("/mnt/ram/history.txt", "a")
		fichier.write(maSortie)
		fichier.close()
		shellyHistory = ""
		shellyCompteur = shellyCompteur + "-" + datetime.today().strftime('%d/%m %H:%M')
		fichier = open("/mnt/ram/compteur.txt", "w")
		fichier.write(shellyCompteur)
		fichier.close()
		fichierLog = open("/mnt/ram/broker.txt", "a")
		fichierLog.write("Worker$SHELLY$" + shellyCompteur+ "\n")
		fichierLog.close()
		shellyCompteur = ""
	#SHELLIES-OFF
	
	
	#XIAOMI-ON
	#Devices list  
	devicesXIAOMIdoorSensors = { '0x00158d0002435273':'bureau','0x00158d00027b495f':'porte' }
	devicesXIAOMImotionSensors = { '0x00158d000222fabd':'motion' }
	#DOOR SENSORS work 
	for deviceID, deviceName in devicesXIAOMIdoorSensors.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['contact']).lower()
			if deviceState == "true":
				fichier = open("/mnt/ram/"+deviceName+"_lastClose.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "false":		
				fichier = open("/mnt/ram/"+deviceName+"_lastOpen.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			fichierLog = open("/mnt/ram/broker.txt", "a")
			fichierLog.write("Worker$XIAOMI$door$"+deviceName+"$"+deviceState+"\n")
			fichierLog.close()
	#MOTION SENSORS work 
	for deviceID, deviceName in devicesXIAOMImotionSensors.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['occupancy']).lower()
			if deviceState == "true":
				fichier = open("/mnt/ram/"+deviceName+"_lastDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			elif deviceState == "false":
				fichier = open("/mnt/ram/"+deviceName+"_lastEndOfDetection.txt", "w")
				fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
				fichier.close()
			fichierLog = open("/mnt/ram/broker.txt", "a")
			fichierLog.write("Worker$XIAOMI$motion$"+deviceName+"$"+deviceState+"\n")
			fichierLog.close()
	#XIAOMI-OFF


#MAIN
startupMsg = "VALFR BROKER v1.3 starting up at " + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "\n"
journal.write(startupMsg)
fichierLog = open("/mnt/ram/broker.txt", "a")
fichierLog.write(startupMsg)
fichierLog.close()
client = mqtt.Client()
client.connect("localhost",1883,60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
