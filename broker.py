#!/usr/bin/env python3
from datetime import datetime
import paho.mqtt.client as mqtt
from systemd import journal
import json
import requests

global pathLogs
global pathData  
global doLogs             
global devicesXIAOMIdoorSensors
global devicesXIAOMImotionSensors
global devicesXIAOMIswitchD1s1
global devicesXIAOMIswitchD1s1target
global devicesXIAOMIswitchD1s1scene
global devicesXIAOMIswitchD1s2
global devicesXIAOMIswitchD1s2target
global devicesXIAOMIswitchD1s2scene
global devicesSHELLYht
global devicesSHELLYdw
global devicesSHELLYroller25
global devicesSHELLYswitch25s1
global devicesSHELLYswitch25s1target
global devicesSHELLYswitch25s1scene
global devicesSHELLYswitch25s2
global devicesSHELLYswitch25s2target
global devicesSHELLYswitch25s2scene
global devicesSHELLYrelay25r1
global devicesSHELLYrelay25r2
global devicesVALFRpi
global devicesHUEwhite
global realtimeHUEwhite
global devicesHUEcolorAmbiance
global realtimeHUEcolorAmbiance
global realtimeHUEcolorAmbianceColorHue
global realtimeHUEcolorAmbianceColorSaturation
global realtimeHUEcolorAmbianceColorTemp
global devicesSHELLYplugS
global realtimeSHELLYplugS
global devicesSHELLYrelayOne
global realtimeSHELLYrelayOne
global devicesSHELLYrelay1pm
global realtimeSHELLYrelay1pm
global shellyHistory
global shellyCompteur


def on_connect(client, userdata, flags, rc):
	connectionMsg = "VALFR BROKER Connected with result code "+str(rc)+"\n"
	#print(connectionMsg)
	journal.write(connectionMsg)
	client.subscribe("#")
	fichierLog = open(pathLogs+"broker.txt", "a")
	fichierLog.write(connectionMsg)
	fichierLog.close()


def on_message(client, userdata, message):
	global pathLogs
	global pathData  
	global doLogs  	
	global devicesXIAOMIdoorSensors
	global devicesXIAOMImotionSensors
	global devicesXIAOMIswitchD1s1
	global devicesXIAOMIswitchD1s1target
	global devicesXIAOMIswitchD1s1scene
	global devicesXIAOMIswitchD1s2
	global devicesXIAOMIswitchD1s2target
	global devicesXIAOMIswitchD1s2scene
	global devicesSHELLYht
	global devicesSHELLYdw
	global devicesSHELLYroller25
	global devicesSHELLYswitch25s1
	global devicesSHELLYswitch25s1target
	global devicesSHELLYswitch25s1scene
	global devicesSHELLYswitch25s2
	global devicesSHELLYswitch25s2target
	global devicesSHELLYswitch25s2scene
	global devicesSHELLYrelay25r1
	global devicesSHELLYrelay25r2
	global devicesVALFRpi
	global devicesHUEwhite
	global realtimeHUEwhite
	global devicesHUEcolorAmbiance
	global realtimeHUEcolorAmbiance
	global realtimeHUEcolorAmbianceColorHue
	global realtimeHUEcolorAmbianceColorSaturation
	global realtimeHUEcolorAmbianceColorTemp
	global devicesSHELLYplugS
	global realtimeSHELLYplugS
	global devicesSHELLYrelayOne
	global realtimeSHELLYrelayOne
	global devicesSHELLYrelay1pm
	global realtimeSHELLYrelay1pm
	global shellyHistory
	global shellyCompteur
	#print("received message =",str(message.payload.decode("utf-8")))
	#print("message topic=",message.topic)
	#print("message qos=",message.qos)
	#print("message retain flag=",message.retain)
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
			#shellyCompteur = shellyHistory
            #shellyTempOnly = shellyHistory
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
			#fichier = open(pathData+deviceID+"_battery.txt", "w")
			#fichier.write(str(message.payload.decode("utf-8")))
			#fichier.close()
			fichier = open(pathData+deviceID+"_datetime.txt", "w")
			fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
			fichier.close()
			shellyHistory = shellyHistory + " - " + str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_history.txt", "a")
            #fichier = open(pathData+"temp-led.txt", "a")
			fichier.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " + shellyHistory + "\n")
			fichier.close()
			#shellyCompteur = shellyCompteur + "-" + datetime.today().strftime('%d/%m %H:%M')
			#fichier = open(pathData+deviceID+"_temperature.txt", "w")
			#fichier.write(shellyCompteur)
			#fichier.close()
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$" + shellyHistory+ "\n")
				fichierLog.close()
			shellyHistory = ""
			#shellyCompteur = ""
            #shellyCompteur = shellyCompteur + "-" + datetime.today().strftime('%d/%m %H:%M')
            #fichier = open(pathData+deviceID+"_temperature.txt", "w")
            #fichier.write(shellyCompteur)
            #fichier.close()
            #fichierLog = open(pathLogs+"broker.txt", "a")
            #fichierLog.write("Work$SHELLY$" + shellyCompteur+ "\n")
            #fichierLog.close()
            #url_string = 'http://192.168.0.83:8086/write?db=chauffage'
            #data_string = 'temperature,sonde='+deviceID+' value='+shellyTempOnly
            #r = requests.post(url_string, data=data_string)
            #shellyCompteur = ""
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
			if doLogs:
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
	#SHELLIES-PlugS
	for deviceID, deviceName in devicesSHELLYplugS.items():
		if message.topic == "shellies/"+deviceID+"/relay/0":
			deviceRelayCommand = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_relay_command.txt", "w")
			fichier.write(deviceRelayCommand)
			fichier.close()
			if deviceRelayCommand == "on":
				realtimeSHELLYplugS[deviceID]="on"
			if deviceRelayCommand == "off":
				realtimeSHELLYplugS[deviceID]="off"
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$PlugS$"+deviceName+"$Relay_Command$"+deviceRelayCommand+"\n")
				fichierLog.close()
	#SHELLIES-One
	for deviceID, deviceName in devicesSHELLYrelayOne.items():
		if message.topic == "shellies/"+deviceID+"/relay/0":
			deviceRelayCommand = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_relay_command.txt", "w")
			fichier.write(deviceRelayCommand)
			fichier.close()
			if deviceRelayCommand == "on":
				realtimeSHELLYrelayOne[deviceID]="on"
			if deviceRelayCommand == "off":
				realtimeSHELLYrelayOne[deviceID]="off"
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$One$"+deviceName+"$Relay_Command$"+deviceRelayCommand+"\n")
				fichierLog.close()
	#SHELLIES-OnePM
	for deviceID, deviceName in devicesSHELLYrelay1pm.items():
		if message.topic == "shellies/"+deviceID+"/relay/0":
			deviceRelayCommand = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_relay_command.txt", "w")
			fichier.write(deviceRelayCommand)
			fichier.close()
			if deviceRelayCommand == "on":
				realtimeSHELLYrelay1pm[deviceID]="on"
			if deviceRelayCommand == "off":
				realtimeSHELLYrelay1pm[deviceID]="off"
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$OnePM$"+deviceName+"$Relay_Command$"+deviceRelayCommand+"\n")
				fichierLog.close()
	#SHELLIES-Switch25s
	for deviceID, deviceName in devicesSHELLYswitch25s1.items():
		if message.topic == "shellies/"+deviceID+"/input/0":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				if devicesSHELLYswitch25s1scene[deviceID]=="HUE":
					scene_Switch_HUE(client,"short",deviceID,"short",deviceName,devicesSHELLYswitch25s1target,realtimeHUEwhite)
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25r2$"+deviceName+"$action$"+deviceInput+"$short\n")
				fichierLog.close()
		if message.topic == "shellies/"+deviceID+"/longpush/0":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				if devicesSHELLYswitch25s1scene[deviceID]=="HUE":
					scene_Switch_HUE(client,"long",deviceID,"long_long",deviceName,devicesSHELLYswitch25s1target,realtimeHUEwhite)
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25r1$"+deviceName+"$action$"+deviceInput+"$long\n")
				fichierLog.close()
	for deviceID, deviceName in devicesSHELLYswitch25s2.items():
		if message.topic == "shellies/"+deviceID+"/input/1":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				if devicesSHELLYswitch25s2scene[deviceID]=="HUE":
					scene_Switch_HUE(client,"short",deviceID,"short",deviceName,devicesSHELLYswitch25s2target,realtimeHUEwhite)
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25r2$"+deviceName+"$action$"+deviceInput+"$short\n")
				fichierLog.close()
		if message.topic == "shellies/"+deviceID+"/longpush/1":
			deviceInput = str(message.payload.decode("utf-8"))
			if deviceInput == "1":
				if devicesSHELLYswitch25s2scene[deviceID]=="HUE":
					scene_Switch_HUE(client,"long",deviceID,"long_long",deviceName,devicesSHELLYswitch25s2target,realtimeHUEwhite)
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25r2$"+deviceName+"$action$"+deviceInput+"$long\n")
				fichierLog.close()
	#SHELLIES-Relay25r
	for deviceID, deviceName in devicesSHELLYrelay25r1.items():
		if message.topic == "shellies/"+deviceID+"/relay/0":
			deviceRelayCommand = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_relay1_command.txt", "w")
			fichier.write(deviceRelayCommand)
			fichier.close()
			if deviceRelayCommand == "on":
				realtimeSHELLYplugS[deviceID]="on"
			if deviceRelayCommand == "off":
				realtimeSHELLYplugS[deviceID]="off"
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25$R1$"+deviceName+"$Relay_Command$"+deviceRelayCommand+"\n")
				fichierLog.close()
	for deviceID, deviceName in devicesSHELLYrelay25r2.items():
		if message.topic == "shellies/"+deviceID+"/relay/1":
			deviceRelayCommand = str(message.payload.decode("utf-8"))
			fichier = open(pathData+deviceID+"_relay2_command.txt", "w")
			fichier.write(deviceRelayCommand)
			fichier.close()
			if deviceRelayCommand == "on":
				realtimeSHELLYplugS[deviceID]="on"
			if deviceRelayCommand == "off":
				realtimeSHELLYplugS[deviceID]="off"
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$SHELLY$relay25$R2$"+deviceName+"$Relay_Command$"+deviceRelayCommand+"\n")
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
			if doLogs:
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
			if doLogs:
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
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$XIAOMI$motion$"+deviceName+"$"+deviceState+"\n")
				fichierLog.write("Work$XIAOMI$luminosity$"+deviceName+"$"+deviceLuminosity+"\n")																	   
				fichierLog.close()
	#switch D1 work
	for deviceID, deviceName in devicesXIAOMIswitchD1s1.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['action']).lower()
			
			if devicesXIAOMIswitchD1s1scene[deviceID]=="HUE":
				scene_Switch_HUE(client,"single_left",deviceID,deviceState,deviceName,devicesXIAOMIswitchD1s1target,realtimeHUEwhite)
			if devicesXIAOMIswitchD1s1scene[deviceID]=="HUE1COLOR":
				scene_Switch_HUE1COLOR(client,"single_left",deviceID,deviceState,deviceName,devicesXIAOMIswitchD1s1target,realtimeHUEwhite)
			if devicesXIAOMIswitchD1s1scene[deviceID]=="ShellyRelay":
				scene_Switch_Relay(client,"single_left",deviceID,deviceState,deviceName,devicesXIAOMIswitchD1s1target,realtimeSHELLYplugS)
			
			if hasattr(python_obj, 'battery'):
				deviceBattery = str(python_obj['battery']).lower()
				fichier = open(pathData+deviceID+"_battery.txt", "w")
				fichier.write(deviceBattery)
				fichier.close()
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$XIAOMI$switchD1$"+deviceName+"$action$left_switch$"+deviceState+"\n")
				fichierLog.close()
	for deviceID, deviceName in devicesXIAOMIswitchD1s2.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceState = str(python_obj['action']).lower()
			
			if devicesXIAOMIswitchD1s2scene[deviceID]=="HUE":
				scene_Switch_HUE(client,"single_right",deviceID,deviceState,deviceName,devicesXIAOMIswitchD1s2target,realtimeHUEwhite)
			if devicesXIAOMIswitchD1s2scene[deviceID]=="HUE1COLOR":
				scene_Switch_HUE1COLOR(client,"single_right",deviceID,deviceState,deviceName,devicesXIAOMIswitchD1s2target,realtimeHUEwhite)
			if devicesXIAOMIswitchD1s2scene[deviceID]=="ShellyRelay":
				scene_Switch_Relay(client,"single_right",deviceID,deviceState,deviceName,devicesXIAOMIswitchD1s2target,realtimeSHELLYplugS)

			if hasattr(python_obj, 'battery'):
				deviceBattery = str(python_obj['battery']).lower()
				fichier = open(pathData+deviceID+"_battery.txt", "w")
				fichier.write(deviceBattery)
				fichier.close()
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$XIAOMI$switchD1$"+deviceName+"$action$right_switch$"+deviceState+"\n")
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
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$HUE$white$"+deviceName+"$Brightness$"+deviceBrightness+"\n")
				fichierLog.close()
	#HUE Color Ambiance work
	for deviceID, deviceName in devicesHUEcolorAmbiance.items():
		if message.topic == "zigbee2mqtt/"+deviceID:
			python_obj = json.loads(str(message.payload.decode("utf-8")))
			deviceBrightness = str(python_obj['brightness']).lower()
			fichier = open(pathData+deviceID+"_brightness.txt", "w")
			fichier.write(deviceBrightness)
			fichier.close()
			deviceColorTemp = str(python_obj['color_temp']).lower()
			fichier = open(pathData+deviceID+"_colorTemp.txt", "w")
			fichier.write(deviceColorTemp)
			fichier.close()
			#bright
			if deviceBrightness == "0" or deviceBrightness == "1":
				realtimeHUEwhite[deviceID]="75"
			elif deviceBrightness == "75":
				realtimeHUEwhite[deviceID]="150"
			elif deviceBrightness == "150":
				realtimeHUEwhite[deviceID]="254"
			else:
				realtimeHUEwhite[deviceID]="0"
			#color
			if realtimeHUEcolorAmbianceColorHue[deviceID] == "get":
				realtimeHUEcolorAmbianceColorHue[deviceID]="29"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="88"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="get"
			elif realtimeHUEcolorAmbianceColorHue[deviceID] == "29":
				realtimeHUEcolorAmbianceColorHue[deviceID]="212"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="10"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="153"
			elif realtimeHUEcolorAmbianceColorHue[deviceID] == "212":
				realtimeHUEcolorAmbianceColorHue[deviceID]="57"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="27"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="get"
			elif realtimeHUEcolorAmbianceColorHue[deviceID] == "57":
				realtimeHUEcolorAmbianceColorHue[deviceID]="44"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="29"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="get"
			elif realtimeHUEcolorAmbianceColorHue[deviceID] == "44":
				realtimeHUEcolorAmbianceColorHue[deviceID]="234"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="99"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="get"
			elif realtimeHUEcolorAmbianceColorHue[deviceID] == "234":
				realtimeHUEcolorAmbianceColorHue[deviceID]="396"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="63"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="get"
			elif realtimeHUEcolorAmbianceColorHue[deviceID] == "396":
				realtimeHUEcolorAmbianceColorHue[deviceID]="29"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="88"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="get"
			else:
				realtimeHUEcolorAmbianceColorHue[deviceID]="29"
				realtimeHUEcolorAmbianceColorSaturation[deviceID]="88"
				realtimeHUEcolorAmbianceColorTemp[deviceID]="get"
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$HUE$white$"+deviceName+"$Brightness$"+deviceBrightness+"\n")
				fichierLog.close()
	#HUE-OFF


#SCENES functions
def scene_Switch_HUE(client,left_right,deviceID,deviceState,deviceName,devideCiblesTarget,realtimeHUEwhite):
	if deviceState == left_right:
		cbiles = devideCiblesTarget[deviceID].split(',')
		for cibleID in cbiles:
			client.publish("zigbee2mqtt/"+cibleID+"/set", '{"brightness": '+realtimeHUEwhite[cibleID]+'}', qos=0, retain=False)
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$scene_Switch_HUE$"+left_right+"$"+deviceName+"$"+deviceState+"$Allumer vers "+cibleID+"\n")
				fichierLog.close()	
		if doLogs:
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$scene_Switch_HUE$"+left_right+"$"+deviceName+"$"+deviceState+"$Allumer vers "+devideCiblesTarget[deviceID]+"\n")
			fichierLog.close()	
	if deviceState == "hold_right" or deviceState == "hold_left" or deviceState == "long_long":
		cbiles = devideCiblesTarget[deviceID].split(',')
		for cibleID in cbiles:
			client.publish("zigbee2mqtt/"+cibleID+"/set", '{"brightness": 0}', qos=0, retain=False)
		if doLogs:
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$scene_Switch_HUE$"+left_right+"_long$"+deviceName+"$"+deviceState+"$Eteindre\n")
			fichierLog.close()	

def scene_Switch_HUE1COLOR(client,left_right,deviceID,deviceState,deviceName,devideCiblesTarget,realtimeHUEwhite):
	if deviceState == left_right:
		if deviceState == "single_left":
			cbiles = devideCiblesTarget[deviceID].split(',')
			for cibleID in cbiles:
				client.publish("zigbee2mqtt/"+cibleID+"/set", '{"brightness": '+realtimeHUEwhite[cibleID]+'}', qos=0, retain=False)
				if doLogs:
					fichierLog = open(pathLogs+"broker.txt", "a")
					fichierLog.write("Work$scene_Switch_HUE$"+left_right+"$"+deviceName+"$"+deviceState+"$Allumer vers "+cibleID+"\n")
					fichierLog.close()	
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$scene_Switch_HUE$"+left_right+"$"+deviceName+"$"+deviceState+"$Allumer vers "+devideCiblesTarget[deviceID]+"\n")
				fichierLog.close()	
		if deviceState == "single_right":
			cbiles = devideCiblesTarget[deviceID].split(',')
			for cibleID in cbiles:
				#client.publish("zigbee2mqtt/"+cibleID+"/set", '{"color_temp": '+realtimeHUEcolorAmbiance[cibleID]+'}', qos=0, retain=False)
				if realtimeHUEcolorAmbianceColorTemp[cibleID] == "get":
					client.publish("zigbee2mqtt/"+cibleID+"/set", '{"color":{"hue":'+realtimeHUEcolorAmbianceColorHue[cibleID]+',"saturation":'+realtimeHUEcolorAmbianceColorSaturation[cibleID]+'}}', qos=0, retain=False)
				else:
					client.publish("zigbee2mqtt/"+cibleID+"/set", '{"color_temp": '+realtimeHUEcolorAmbianceColorTemp[cibleID]+'}', qos=0, retain=False)
				if doLogs:
					fichierLog = open(pathLogs+"broker.txt", "a")
					fichierLog.write("Work$scene_Switch_HUE$"+left_right+"$"+deviceName+"$"+deviceState+"$Allumer vers "+cibleID+"\n")
					fichierLog.close()	
			if doLogs:
				fichierLog = open(pathLogs+"broker.txt", "a")
				fichierLog.write("Work$scene_Switch_HUE$"+left_right+"$"+deviceName+"$"+deviceState+"$Allumer vers "+devideCiblesTarget[deviceID]+"\n")
				fichierLog.close()
	if deviceState == "hold_left" or deviceState == "long_long":
		cbiles = devideCiblesTarget[deviceID].split(',')
		for cibleID in cbiles:
			client.publish("zigbee2mqtt/"+cibleID+"/set", '{"brightness": 0}', qos=0, retain=False)
		if doLogs:
			fichierLog = open(pathLogs+"broker.txt", "a")
			fichierLog.write("Work$scene_Switch_HUE$"+left_right+"_long$"+deviceName+"$"+deviceState+"$Eteindre\n")
			fichierLog.close()	

def scene_Switch_Relay(client,left_right,deviceID,deviceState,deviceName,devideCiblesTarget,realtimeSHELLYplugS):
	if deviceState == left_right:
		cbiles = devideCiblesTarget[deviceID].split(',')
		for cibleIDrelay in cbiles:
			cibleData = cibleIDrelay.split(':')
			cibleID = cibleData[0]
			relayID = cibleData[1]
			if realtimeSHELLYplugS[cibleID]=="off":
				client.publish("shellies/"+cibleID+"/relay/"+relayID+"/command", 'on', qos=0, retain=False)
				if doLogs:
					fichierLog = open(pathLogs+"broker.txt", "a")
					fichierLog.write("Work$scene_Switch_Relay$"+left_right+"$"+deviceName+"$"+deviceState+"$Allumer vers "+devideCiblesTarget[deviceID]+"\n")
					fichierLog.close()	
			else:
				client.publish("shellies/"+cibleID+"/relay/"+relayID+"/command", 'off', qos=0, retain=False)
				if doLogs:
					fichierLog = open(pathLogs+"broker.txt", "a")
					fichierLog.write("Work$scene_Switch_Relay$"+left_right+"$"+deviceName+"$"+deviceState+"$eteindre vers "+devideCiblesTarget[deviceID]+"\n")
					fichierLog.close()	
#	if deviceState == left_right+"_long":
#		cbiles = devideCiblesTarget[deviceID].split(',')
#		for cibleID in cbiles:
#			client.publish("zigbee2mqtt/"+cibleID+"/set", '{"brightness": 0}', qos=0, retain=False)
#		if doLogs:
#			fichierLog = open(pathLogs+"broker.txt", "a")
#			fichierLog.write("Work$scene_Switch_Relay$"+left_right+"_long$"+deviceName+"$"+deviceState+"$Eteindre\n")
#			fichierLog.close()	
			
#END SCENES functions


#MAIN
global pathLogs
global pathData  
global doLogs      
global devicesXIAOMIdoorSensors
global devicesXIAOMImotionSensors
global devicesXIAOMIswitchD1s1
global devicesXIAOMIswitchD1s1target
global devicesXIAOMIswitchD1s1scene
global devicesXIAOMIswitchD1s2
global devicesXIAOMIswitchD1s2target
global devicesXIAOMIswitchD1s2scene
global devicesSHELLYht
global devicesSHELLYdw
global devicesSHELLYroller25
global devicesSHELLYswitch25s1
global devicesSHELLYswitch25s1target
global devicesSHELLYswitch25s1scene
global devicesSHELLYswitch25s2
global devicesSHELLYswitch25s2target
global devicesSHELLYswitch25s2scene
global devicesSHELLYrelay25r1
global devicesSHELLYrelay25r2
global devicesVALFRpi
global devicesHUEwhite
global realtimeHUEwhite
global devicesHUEcolorAmbiance
global realtimeHUEcolorAmbiance
global realtimeHUEcolorAmbianceColorHue
global realtimeHUEcolorAmbianceColorTemp
global realtimeHUEcolorAmbianceColorSaturation
global devicesSHELLYplugS
global realtimeSHELLYplugS
global devicesSHELLYrelayOne
global realtimeSHELLYrelayOne
global devicesSHELLYrelay1pm
global realtimeSHELLYrelay1pm
devicesXIAOMIdoorSensors = dict()
devicesXIAOMImotionSensors = dict()
devicesXIAOMIswitchD1s1 = dict()
devicesXIAOMIswitchD1s1target = dict()
devicesXIAOMIswitchD1s1scene = dict()
devicesXIAOMIswitchD1s2 = dict()
devicesXIAOMIswitchD1s2target = dict()
devicesXIAOMIswitchD1s2scene = dict()
devicesSHELLYht = dict()
devicesSHELLYdw = dict()
devicesSHELLYroller25 = dict()
devicesSHELLYswitch25s1 = dict()
devicesSHELLYswitch25s1target = dict()
devicesSHELLYswitch25s1scene = dict()
devicesSHELLYswitch25s2 = dict()
devicesSHELLYswitch25s2target = dict()
devicesSHELLYswitch25s2scene = dict()
devicesSHELLYrelay25r1 = dict()
devicesSHELLYrelay25r2 = dict()
devicesVALFRpi = dict()
devicesHUEwhite = dict()
realtimeHUEwhite = dict()
devicesHUEcolorAmbiance = dict()
realtimeHUEcolorAmbiance = dict()
realtimeHUEcolorAmbianceColorTemp = dict()
realtimeHUEcolorAmbianceColorHue = dict()
realtimeHUEcolorAmbianceColorSaturation = dict()
devicesSHELLYplugS = dict()
realtimeSHELLYplugS = dict()
devicesSHELLYrelayOne = dict()
realtimeSHELLYrelayOne = dict()
devicesSHELLYrelay1pm = dict()
realtimeSHELLYrelay1pm = dict()
#pathLogs = "/mnt/ram/"
#pathData = "/mnt/ram/"
pathLogs = "/home/logs/" 
pathData = "/home/data/iot/" 
doLogs = False

startupMsg = "VALFR BROKER v3.6 starting up at " + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "\n"
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
		if data[0] == "XIAOMIswitchD1s1":
			devicesXIAOMIswitchD1s1[data[1]]=data[2]
			devicesXIAOMIswitchD1s1scene[data[1]]=data[3]
			devicesXIAOMIswitchD1s1target[data[1]]=data[4]
		if data[0] == "XIAOMIswitchD1s2":
			devicesXIAOMIswitchD1s2[data[1]]=data[2]
			devicesXIAOMIswitchD1s2scene[data[1]]=data[3]
			devicesXIAOMIswitchD1s2target[data[1]]=data[4]
		if data[0] == "SHELLYht":
			devicesSHELLYht[data[1]]=data[2]
		if data[0] == "SHELLYdw":
			devicesSHELLYdw[data[1]]=data[2]
		if data[0] == "SHELLYroller25":
			devicesSHELLYroller25[data[1]]=data[2]
		if data[0] == "SHELLYswitch25s1":
			devicesSHELLYswitch25s1[data[1]]=data[2]
			devicesSHELLYswitch25s1scene[data[1]]=data[3]
			devicesSHELLYswitch25s1target[data[1]]=data[4]
		if data[0] == "SHELLYswitch25s2":
			devicesSHELLYswitch25s2[data[1]]=data[2]
			devicesSHELLYswitch25s2scene[data[1]]=data[3]
			devicesSHELLYswitch25s2target[data[1]]=data[4]
		if data[0] == "SHELLYrelay25r1":
			devicesSHELLYrelay25r1[data[1]]=data[2]
		if data[0] == "SHELLYrelay25r2":
			devicesSHELLYrelay25r2[data[1]]=data[2]
		if data[0] == "valfrpi":
			devicesVALFRpi[data[1]]=data[2]
		if data[0] == "HUEwhite":
			devicesHUEwhite[data[1]]=data[2]
			realtimeHUEwhite[data[1]]="get"
		if data[0] == "HUEcolorAmbiance":
			devicesHUEcolorAmbiance[data[1]]=data[2]
			realtimeHUEcolorAmbiance[data[1]]="get"
			realtimeHUEcolorAmbianceColorTemp[data[1]]="get"
			realtimeHUEcolorAmbianceColorHue[data[1]]="get"
			realtimeHUEcolorAmbianceColorSaturation[data[1]]="get"
		if data[0] == "SHELLYplugS":
			devicesSHELLYplugS[data[1]]=data[2]
			realtimeSHELLYplugS[data[1]]="get"
		if data[0] == "SHELLYrelayOne":
			devicesSHELLYrelayOne[data[1]]=data[2]
			realtimeSHELLYrelayOne[data[1]]="get"
		if data[0] == "SHELLYrelay1pm":
			devicesSHELLYrelay1pm[data[1]]=data[2]
			realtimeSHELLYrelay1pm[data[1]]="get"
fichierLog.write(str(len(devicesXIAOMIdoorSensors))+" 'XIAOMIdoor' devices loaded\n")
fichierLog.write(str(len(devicesXIAOMImotionSensors))+" 'XIAOMImotion' devices loaded\n")
fichierLog.write(str(len(devicesXIAOMIswitchD1s1))+" 'XIAOMIswitchD1' devices loaded (switch left)\n")
fichierLog.write(str(len(devicesXIAOMIswitchD1s2))+" 'XIAOMIswitchD1' devices loaded (switch right)\n")
fichierLog.write(str(len(devicesSHELLYht))+" 'SHELLYht' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYdw))+" 'SHELLYdw' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYroller25))+" 'SHELLYroller25' devices loaded (roller mode)\n")
fichierLog.write(str(len(devicesSHELLYswitch25s1))+" 'SHELLYswitch25' devices loaded (switch 1)\n")
fichierLog.write(str(len(devicesSHELLYswitch25s2))+" 'SHELLYswitch25' devices loaded (switch 2)\n")
fichierLog.write(str(len(devicesSHELLYrelay25r1))+" 'SHELLYrelay25' devices loaded (relay 1)\n")
fichierLog.write(str(len(devicesSHELLYrelay25r2))+" 'SHELLYrelay25' devices loaded (relay 2)\n")
fichierLog.write(str(len(devicesVALFRpi))+" 'valfrpi' devices loaded\n")
fichierLog.write(str(len(devicesHUEwhite))+" 'HUEwhite' devices loaded\n")
fichierLog.write(str(len(devicesHUEcolorAmbiance))+" 'HUEcolorAmbiance' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYplugS))+" 'SHELLYplugS' devices loaded\n")
fichierLog.write(str(len(devicesSHELLYrelayOne))+" 'SHELLYrelayOne' devices loaded (blue)\n")
fichierLog.write(str(len(devicesSHELLYrelay1pm))+" 'SHELLYrelay1pm' devices loaded (red)\n")
fichierLog.close()
#starting up MQTT
client = mqtt.Client()
client.connect("localhost",1883,60)
client.on_connect = on_connect
client.on_message = on_message
#In-Real-Time sync & checking 
for key in realtimeHUEwhite:
	client.publish("zigbee2mqtt/"+key+"/get", '{"brightness": "0"}', qos=0, retain=False)
for key in realtimeHUEcolorAmbiance:
	client.publish("zigbee2mqtt/"+key+"/get", '{"brightness": "0"}', qos=0, retain=False)
for key in realtimeSHELLYplugS:
	#client.publish("shellies/"+key+"/relay/0/command", 'off', qos=0, retain=False)
	client.publish("shellies/"+key+"/status", 'off', qos=0, retain=False)
for key in realtimeSHELLYrelayOne:
	#client.publish("shellies/"+key+"/relay/0/command", 'off', qos=0, retain=False)
	client.publish("shellies/"+key+"/status", 'off', qos=0, retain=False)
for key in realtimeSHELLYrelay1pm:
	#client.publish("shellies/"+key+"/relay/0/command", 'off', qos=0, retain=False)
	client.publish("shellies/"+key+"/status", 'off', qos=0, retain=False)
for key in devicesSHELLYrelay25r1:
	#client.publish("shellies/"+key+"/relay/0/command", 'off', qos=0, retain=False)
	client.publish("shellies/"+key+"/status", 'off', qos=0, retain=False)
for key in devicesSHELLYrelay25r2:
	#client.publish("shellies/"+key+"/relay/1/command", 'off', qos=0, retain=False)
	client.publish("shellies/"+key+"/status", 'off', qos=0, retain=False)
	#NB : shellies doesnt get status by MQTT - only = http://192.168.0.13/settings/0?mqtt_update_period=0
subscribeMsg = "VALFR BROKER In-RealTime devices checking\n"
journal.write(subscribeMsg)
fichierLog = open(pathLogs+"broker.txt", "a")
fichierLog.write(subscribeMsg)
fichierLog.close()
#Ready processing messages forever !
client.loop_forever()
