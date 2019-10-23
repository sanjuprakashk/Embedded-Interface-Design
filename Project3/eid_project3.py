#!/usr/bin/python3 

'''
eid_project3.py: This file contains the code that spawns the GUI
                 for project 3

@authors: Sanju Prakash Kannioth, Srinath Shanmuganadhan

@date: 09/23/2019

@references: https://askubuntu.com/questions/1014947/mysql-connector-python-importerror-no-module-named-mysql  
             https://www.youtube.com/watch?v=lCfSKtPADYw  
             https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py  
             https://pythonprogramminglanguage.com/pyqtgraph-plot/
             https://www.programcreek.com/python/example/99607/PyQt5.QtCore.QTimer
''' 

from PyQt5 import QtWidgets, QtGui, QtCore
from eid_project3_ui import Ui_Dialog
import sys
import Adafruit_DHT
import mysql.connector
import pyqtgraph as pg

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime


class eid_project1(QtWidgets.QDialog):
	''' 
	eid_project1 class containing initialization of GUI and callback functions 
	'''
	
	def __init__(self):
		''' 
		Initialization of GUI
		'''
		super(eid_project1, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		# DB connection object
		self.mariadb_connection = mysql.connector.connect(user='sansri', \
		                                                  password='sansri1234', \
		                                                  database='eid_project1')
		
		self.cursor = self.mariadb_connection.cursor()
		
		self.Units = 'C' # Variable to store correct measurement unit selection
		
		self.tempVal = 0 # Vraible to store temperature value
		self.humVal = 0 # Vraible to store humidity value
		
		self.tempLimit = 100 # Vraible to store temperature limit
		self.humLimit = 100 # Vraible to store humidity limit
		
		self.sensorReadingCount = 0 # Vraible to store number of readings obtained
		self.timeStamp = 0 # Vraible to store timestamp
		
		self.ui.tempLimitLine.setText("0.0")
		self.ui.humLimitLine.setText("0.0")
		
		self.ui.tempLimitLine.setText("100.0")
		self.ui.humLimitLine.setText("100.0") 
			
		self.ui.setTempLimitButton.clicked.connect(self.setTempLimit)
		
		self.ui.setHumLimitButton.clicked.connect(self.setHumLimit)
		
		self.ui.changeUnitsButton.clicked.connect(self.changeUnits)
		
		self.ui.immediateValButton.clicked.connect(self.getImmediateVal)
		
		self.ui.getTempPlotButton.clicked.connect(self.getTemperatureValFromDb)
		
		self.ui.getHumPlotButton.clicked.connect(self.getHumidityValFromDb)
		
		self.createTableInDb()
		
		self.periodicTimer = QtCore.QTimer(self)
		self.periodicTimer.timeout.connect(self.sensorUpdate)
		self.periodicTimer.start(15000)
		
		# AWS IoT certificate based connection
		self.myMQTTClient = AWSIoTMQTTClient("Temperature")
		self.myMQTTClient.configureEndpoint("a2gca9kkhv4ts6-ats.iot.us-east-1.amazonaws.com", 8883)
		self.myMQTTClient.configureCredentials("/home/pi/Desktop/AWS_certificates/Amazon_Root_CA_1.pem", "/home/pi/Desktop/AWS_certificates/5d2c3527b4-private.pem.key", "/home/pi/Desktop/AWS_certificates/5d2c3527b4-certificate.pem.crt")
		self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
		self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
		self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

		#connect to MQTT
		self.myMQTTClient.connect()
	
	def changeUnits(self):
		'''
		Function the change units from Faren to Celcius and vice-versa
		'''
		if(self.Units == 'C'):
			self.Units = 'F'
		else:
			self.Units = 'C'
		
		self.updateDisplay()
	
	
	def setTempLimit(self):
		'''
		Function to set temperature limit
		'''
		self.tempLimit = float(self.ui.tempLimitLine.text())
		self.updateDisplay()
		
	
	def setHumLimit(self):
		'''
		Function to set humidity limit
		'''
		self.humLimit = float(self.ui.humLimitLine.text())
		self.updateDisplay()

	
	def updateDisplay(self):
		'''
		Function to update display and send data to MQTT
		'''
		humLimit = float("{0:.2f}".format(self.humLimit))
		humVal  = float("{0:.2f}".format(self.humVal))
							
		if(self.Units == 'C'):
			tempVal  = float("{0:.2f}".format(self.tempVal))
			tempLimit = float("{0:.2f}".format(self.tempLimit))
		else:
			tempVal  = float("{0:.2f}".format((self.tempVal * 9/5) + 32))
			tempLimit = float("{0:.2f}".format((self.tempLimit * 9/5) + 32))
		
		if(humVal >= humLimit):
			self.ui.humExceededLine.setText("Humidity exceeded")
			payload = '{ "id":"alert", "Timestamp": "'+ (str(self.timeStamp)) + '", "Humidity Alert Level": "'+ str(humVal) +'", "Humidity Trigger Level": "'+ str(humLimit) +'" }'
			print (payload)
			self.myMQTTClient.publish("sensorstate",payload, 0)
		else:
			self.ui.humExceededLine.setText("Humidity in range")
		
		if(tempVal >= tempLimit):
			self.ui.tempExceededLine.setText("Temperature exceeded")
			payload = '{ "id":"alert", "Timestamp": "'+ (str(self.timeStamp)) + '", "Temperature Alert Level": "'+ str(tempVal) +'", "Temperature Trigger Level": "'+ str(tempLimit) +'" }'
			print (payload)
			self.myMQTTClient.publish("sensorstate",payload, 0)

		else:
			self.ui.tempExceededLine.setText("Temperature in range")
			
		self.ui.tempLimitLine.setText(str(tempLimit))
		self.ui.humLimitLine.setText(str(humLimit))
		
		self.ui.timestampDisplayLine.setText(str(self.timeStamp))
		
		self.ui.tempDisplayLine.setText(str(tempVal) + " " + self.Units)
		self.ui.humDisplayLine.setText(str(humVal) + " %")
		
		payload = '{ "id":"data", "Timestamp": "'+ (str(self.timeStamp)) + '", "Temperature": "'+ str(tempVal) +'", "Humidity": "'+ str(humVal) +'" }'
		print (payload)
		self.myMQTTClient.publish("sensorstate",payload, 0)


	def updateError(self):
		'''
		Function to set ERROR
		'''
		self.ui.tempDisplayLine.setText("Error")
		self.ui.humDisplayLine.setText("Error")

	
	def getImmediateVal(self):
		'''
		Function to get Immediate value from sensor
		'''
		self.humVal , self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4, \
		                                                     delay_seconds=0.2)
		
		self.timeStamp = QtCore.QTime.currentTime().toString(QtCore.Qt.DefaultLocaleLongDate)
		
		if self.humVal is not None and self.tempVal  is not None:
			self.updateDisplay()
		else:
			self.updateError()

	
	def sensorUpdate(self):
		'''
		Function to update the sensor for every 15 seconds
		'''
		self.humVal , self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4, \
			                                                 delay_seconds=0.2)
		self.sensorReadingCount = self.sensorReadingCount + 1
		
		self.timeStamp = QtCore.QTime.currentTime().toString(QtCore.Qt.DefaultLocaleLongDate)
		
		if self.humVal is not None and self.tempVal  is not None:
			self.updateDisplay()
		else:
			self.updateError()
		
		self.putHumidityValInDb(self.humVal, self.timeStamp)
		self.putTemperatureValInDb(self.tempVal, self.timeStamp)
		
		if(self.sensorReadingCount == 30):
			self.periodicTimer.stop()
			self.mariadb_connection.close()
			sys.exit(1)
	
	
	def createTableInDb(self):
		'''
		Function to create SQL table for Temperature and humidity in DB if it not exist
		'''
		humd_table_exist = "SHOW TABLES LIKE 'HUMID'"
		self.cursor.execute(humd_table_exist)
		result_hum = self.cursor.fetchone()
		
		if result_hum:
			print ('There is a table named HUMID')
		else:
			# there are no tables named "HUMID" thus creating a table
			self.cursor.execute("CREATE TABLE HUMID(id INT NOT NULL AUTO_INCREMENT, \
				                                    Humd VARCHAR(20) NOT NULL, \
				                                    time_stamp VARCHAR(20) NOT NULL, \
				                                    PRIMARY KEY (id));")
		
		temp_table_exist = "SHOW TABLES LIKE 'TEMP'"
		self.cursor.execute(temp_table_exist)
		
		result_temp = self.cursor.fetchone()
		
		if result_temp:
			print ('there is a table named TEMP')
		else:
			# there are no tables named "TEMP" thus creating a table
			self.cursor.execute("CREATE TABLE TEMP(id INT NOT NULL AUTO_INCREMENT, \
				                                   Temp VARCHAR(20) NOT NULL, \
				                                   time_stamp VARCHAR(20) NOT NULL, \
				                                   PRIMARY KEY (id));")
		
	
	def putHumidityValInDb(self, humdVal, humdTime):
		'''
		Function to put humidity entries into DB
		'''
		self.cursor.execute("INSERT INTO HUMID (Humd, time_stamp) \
			                 VALUES (%s, %s)", (humdVal, humdTime))
				
		self.mariadb_connection.commit()

		
	def putTemperatureValInDb(self, tempVal, tempTime):
		'''
		Function to put temperature entries into DB
		'''	
		self.cursor.execute("INSERT INTO TEMP (Temp, time_stamp) \
			                 VALUES (%s, %s)", (tempVal, tempTime))
		self.mariadb_connection.commit()

	
	def getHumidityValFromDb(self):
		'''
		Function to get humidity entry DB and plot humidity graph
		'''
		self.hum_plt = pg.plot(title="Humidity Plot")
		self.hum_plt.showGrid(x=True,y=True)
		
		self.hum_plt.setLabel('left', 'Humidity', units='%')
		self.hum_plt.setLabel('bottom', 'Number', units='')
						
		fetch_humid = "SELECT * FROM HUMID ORDER BY id DESC LIMIT 10"
		self.cursor.execute(fetch_humid)
		
		hum_values = self.cursor.fetchall()
		# Populate humidity list with last 10 temperature values from db
		hum_list = [temp[1] for temp in hum_values]
		hum_list = list(map(float, hum_list))
		# Reverse the list as it needs to be plotted in reverse order
		hum_list.reverse()
		
		x = range(0,len(hum_list))

		if(self.Units == 'F'):
			hum_list = [((i *  9/5) + 32) for i in hum_list]
		
		self.hum_plt.plot(x, hum_list, pen='r', symbolPen='b', symbolBrush=0.2)
		
		return hum_list

	
	def getTemperatureValFromDb(self):
		'''
		Function to get temperature entry from DB and plot temperature graph
		'''
		self.temp_plt = pg.plot(title="Temperature Plot")
		self.temp_plt.showGrid(x=True,y=True)
		
		self.temp_plt.setLabel('left', 'Temperature', units=self.Units)
		self.temp_plt.setLabel('bottom', 'Number', units='')
				
		fetch_temp = "SELECT * FROM TEMP ORDER BY id DESC LIMIT 10"
		self.cursor.execute(fetch_temp)
		
		temp_values = self.cursor.fetchall()
		# Populate temperory list with last 10 temperature values from db
		temp_list = [temp[1] for temp in temp_values] 
		temp_list = list(map(float, temp_list))
		# Reverse the list as it needs to be plotted in reverse order
		temp_list.reverse()
		
		x = range(0,len(temp_list))
		
		if(self.Units == 'F'):
			temp_list = [((i *  9/5) + 32) for i in temp_list]

		self.temp_plt.plot(x, temp_list, pen='b', symbolPen='b', symbolBrush=0.2)
		
		return temp_list


def main():
	'''
	Main function that executes the GUI 
	'''
	app = QtWidgets.QApplication([])
	application = eid_project1()
	application.show()
	app.exec()


if __name__ == "__main__":
	main()

