#!/usr/bin/env python3
from datetime import datetime
import paho.mqtt.client as mqtt
from systemd import journal
import json
import time
import sys
from threading import Thread
import os

myRules=[]

class LoadRules(Thread):
	def __init__(self, pathFichier):
		Thread.__init__(self)
		self.pathFichier = pathFichier

	def run(self):
		tmpMyRules=[]
		with open(self.pathFichier) as f :
			for line in f :
				if len(line) > 2:
					line = line.replace("\n","")
					tmpMyRules.append(line)
		global myRules
		myRules=tmpMyRules
		#print(str(len(myRules))+" rules loaded")


class Stores(Thread):
	def __init__(self, storeID, storeAction):
		Thread.__init__(self)
		self.storeAction = str(storeAction)
		self.storeID = str(storeID)

	def run(self):
		#print("store action = "+self.storeAction)
		if self.storeAction == "open" or self.storeAction == "close":
			os.system("mosquitto_pub -h localhost -t shellies/"+self.storeID+"/roller/0/command -m "+self.storeAction);
		if self.storeAction[0:3] == "pos":
			os.system("mosquitto_pub -h localhost -t shellies/"+self.storeID+"/roller/0/command/pos -m "+self.storeAction.replace("pos",""));
		fichierLog = open("/mnt/ram/worker.txt", "a")
		fichierLog.write("Action$SHELLY$stores$"+self.storeID+"$"+self.storeAction+"\n")
		fichierLog.close()

#MAIN
startupMsg = "VALFR WORKER v1.0 starting up at " + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "\n"
journal.write(startupMsg)
fichierLog = open("/mnt/ram/worker.txt", "a")
fichierLog.write(startupMsg)
fichierLog.close()
thread_0 = LoadRules("/home/data/rules-worker.txt")
thread_0.daemon = True
thread_0.start()

while True:
	#print(datetime.today().strftime('%Y-%m-%d %H:%M:%S')+" ")
	#if datetime.today().strftime('%S') == "10" or datetime.today().strftime('%S') == "20" or datetime.today().strftime('%S') == "30" or datetime.today().strftime('%S') == "40" or datetime.today().strftime('%S') == "50" or datetime.today().strftime('%S') == "00":
	if datetime.today().strftime('%S') == "00":
		thread_2 = LoadRules("/home/data/rules-worker.txt")
		thread_2.daemon = True
		thread_2.start()
	for rule in myRules:
		actions = rule.split("!")
		if str(actions[0]) == "once":
			if datetime.today().strftime('%Y-%m-%d %H:%M:%S') == str(actions[1]):
				if str(actions[2]) == "stores":
					thread_3 = Stores(str(actions[3]),str(actions[4]))
					thread_3.daemon = True
					thread_3.start()
	time.sleep(1)
#BYE