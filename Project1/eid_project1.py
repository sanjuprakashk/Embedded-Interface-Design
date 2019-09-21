#!/usr/bin/python3 

from PyQt5 import QtWidgets, QtGui, QtCore
from eid_project1_ui import Ui_Dialog
import sys
import Adafruit_DHT
import mysql.connector
import pyqtgraph as pg

class eid_project1(QtWidgets.QDialog):
	def __init__(self):
		super(eid_project1, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		self.mariadb_connection = mysql.connector.connect(user='srinath', password='srinath', database='test')
		
		self.cursor = self.mariadb_connection.cursor()
		
		self.Units = 'C'
		
		self.tempVal = 0
		self.humVal = 0
		
		self.tempLimit = 100
		self.humLimit = 100
		
		self.sensorReadingCount = 0
		self.timeStamp = 0
		
		self.ui.tempLimitLine.setText("0.0")
		self.ui.humLimitLine.setText("0.0")
		
		self.ui.tempLimitLine.setText("100.0")
		self.ui.humLimitLine.setText("100.0") 
			
		self.ui.setTempLimitButton.clicked.connect(self.setTempLimit)
		
		self.ui.setHumLimitButton.clicked.connect(self.setHumLimit)
		
		self.ui.changeUnitsButton.clicked.connect(self.changeUnits)
		
		self.ui.immediateValButton.clicked.connect(self.getImmediateVal)
		
		self.ui.getTempPlotButton.clicked.connect(self.get_temperature)
		
		self.ui.getHumPlotButton.clicked.connect(self.get_humidity)
		
		self.create_table()
		
		
		
		''' https://www.programcreek.com/python/example/99607/PyQt5.QtCore.QTimer '''
		self.periodicTimer = QtCore.QTimer(self)
		self.periodicTimer.timeout.connect(self.sensorUpdate)
		self.periodicTimer.start(1000)

# Function the change units from F to C and vice-versa
	def changeUnits(self):
		if(self.Units == 'C'):
			self.Units = 'F'
		else:
			self.Units = 'C'
		
		self.updateDisplay()
	
#Function to set temperature limit
	def setTempLimit(self):
		self.tempLimit = float(self.ui.tempLimitLine.text())
		self.updateDisplay()
		
#Function to set humidity limit
	def setHumLimit(self):
		self.humLimit = float(self.ui.humLimitLine.text())
		self.updateDisplay()

#Function to update display
	def updateDisplay(self):
		humLimit = float("{0:.2f}".format(self.humLimit))
		humVal  = float("{0:.2f}".format(self.humVal))
			
					
		if(self.Units == 'C'):
			tempVal  = float("{0:.2f}".format(self.tempVal))
			tempLimit = float("{0:.2f}".format(self.tempLimit))
		else:
			tempVal  = float("{0:.2f}".format((self.tempVal * 9/5)+32))
			tempLimit = float("{0:.2f}".format((self.tempLimit * 9/5)+32))
		
		if(humVal >= humLimit):
			self.ui.humExceededLine.setText("Humidity exceeded")
		else:
			self.ui.humExceededLine.setText("Humidity in range")
		
		if(tempVal >= tempLimit):
			self.ui.tempExceededLine.setText("Temperature exceeded")
		else:
			self.ui.tempExceededLine.setText("Temperature in range")
			
		#self.ui.tempLimitLine.setText(str(tempLimit))
		#self.ui.humLimitLine.setText(str(humLimit)) 
		self.ui.timestampDisplayLine.setText(str(self.timeStamp))
		
		print("Humidity limit = ", humLimit)
		print("Temperature limit = ", tempLimit)
		
		self.ui.tempDisplayLine.setText(str(tempVal) + " " + self.Units)
		self.ui.humDisplayLine.setText(str(humVal) + " %")

#Function to set ERROR	
	def updateError(self):
		self.ui.tempDisplayLine.setText("Error")
		self.ui.humDisplayLine.setText("Error")

#Function to get Immediate value from sensor	
	def getImmediateVal(self):
		self.humVal , self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4, delay_seconds=0.2)
		
		self.timeStamp = QtCore.QTime.currentTime().toString(QtCore.Qt.DefaultLocaleLongDate)
		
		if self.humVal is not None and self.tempVal  is not None:
			self.updateDisplay()
		else:
			self.updateError()

#Function to update the sensor for every 15 seconds	
	def sensorUpdate(self):
		''' https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py '''
		self.humVal , self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4, delay_seconds=0.2)
		self.sensorReadingCount = self.sensorReadingCount + 1
		
		if self.humVal is not None and self.tempVal  is not None:
			self.updateDisplay()
		else:
			self.updateError()
		
		self.timeStamp = QtCore.QTime.currentTime().toString(QtCore.Qt.DefaultLocaleLongDate)
		self.put_humidity(self.humVal, self.timeStamp)
		self.put_temperature(self.tempVal, self.timeStamp)
		if(self.sensorReadingCount == 30):
			self.periodicTimer.stop()
			self.mariadb_connection.close()
			sys.exit(1)
	
#Function to create SQL table in DB if it not exist
	def create_table(self):
		humd_table_exist = "SHOW TABLES LIKE 'HUMID1'"
		self.cursor.execute(humd_table_exist)
		result_hum = self.cursor.fetchone()
		if result_hum:
			print ('there is a table named HUMID1')
		else:
			# there are no tables named "HUMID1"
			self.cursor.execute("CREATE TABLE HUMID1(id INT NOT NULL AUTO_INCREMENT, Humd VARCHAR(20) NOT NULL, time_stamp VARCHAR(20) NOT NULL, PRIMARY KEY (id));")
		
		temp_table_exist = "SHOW TABLES LIKE 'TEMP1'"
		self.cursor.execute(temp_table_exist)
		result_temp = self.cursor.fetchone()
		if result_temp:
			print ('there is a table named TEMP1')
		else:
			# there are no tables named "TEMP1"
			self.cursor.execute("CREATE TABLE TEMP1(id INT NOT NULL AUTO_INCREMENT, Temp VARCHAR(20) NOT NULL, time_stamp VARCHAR(20) NOT NULL, PRIMARY KEY (id));")
		
#Function to put humidity entries into DB	
	def put_humidity(self,humdVal,humdTime):
		self.cursor.execute("INSERT INTO HUMID1 (Humd, time_stamp) VALUES (%s, %s)", (humdVal, humdTime))
		print("Record inserted successfully into HUMID1 table")
		self.mariadb_connection.commit()

#Function to put temperature entries into DB	
	def put_temperature(self, tempVal,tempTime):
		self.cursor.execute("INSERT INTO TEMP1 (Temp, time_stamp) VALUES (%s, %s)", (tempVal, tempTime))
		print("Record inserted successfully into TEMP1 table")
		self.mariadb_connection.commit()

#Function to get humidity entry and plot humidity graph
	def get_humidity(self):
		#https://pythonprogramminglanguage.com/pyqtgraph-plot/
		x = range(0,10)
		plt = pg.plot()
		plt.setWindowTitle('Humidity plot')
		
		
		fetch_humid = "SELECT * FROM HUMID1 ORDER BY id DESC LIMIT 10"
		self.cursor.execute(fetch_humid)
		hum_values = self.cursor.fetchall()
		hum_list = [x[1] for x in hum_values]
		hum_list = list(map(float, hum_list))
		if(self.Units == 'F'):
			hum_list = [((i *  9/5)+32) for i in hum_list]
		print (hum_list)
		plt.plot(x, hum_list, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='red')
		
		return hum_list

#Function to get temperature entry and plot temperature graph	
	def get_temperature(self):
		x = range(0,10)
		plt = pg.plot()
		plt.setWindowTitle('Temperature plot')
		fetch_temp = "SELECT * FROM TEMP1 ORDER BY id DESC LIMIT 10"
		self.cursor.execute(fetch_temp)
		temp_values = self.cursor.fetchall()
		temp_list = [x[1] for x in temp_values]
		temp_list = list(map(float, temp_list))
		if(self.Units == 'F'):
			temp_list = [((i *  9/5)+32) for i in temp_list]
		print (temp_list)
		
		plt.plot(x, temp_list, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='blue')
		
		return temp_list


app = QtWidgets.QApplication([])
application = eid_project1()
application.show()
app.exec()

