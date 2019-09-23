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
		
		self.mariadb_connection = mysql.connector.connect(user='sansri', password='sansri1234', database='eid_project1')
		
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
		
		self.ui.getTempPlotButton.clicked.connect(self.getTemperatureValFromDb)
		
		self.ui.getHumPlotButton.clicked.connect(self.getHumidityValFromDb)
		
		self.createTableInDb()
		
			
		''' https://www.programcreek.com/python/example/99607/PyQt5.QtCore.QTimer '''
		self.periodicTimer = QtCore.QTimer(self)
		self.periodicTimer.timeout.connect(self.sensorUpdate)
		self.periodicTimer.start(15000)

# Function the change units from Faren to Celcius and vice-versa
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
			
		self.ui.tempLimitLine.setText(str(tempLimit))
		self.ui.humLimitLine.setText(str(humLimit)) 
		
		self.ui.timestampDisplayLine.setText(str(self.timeStamp))
		
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
	
#Function to create SQL table for Temperature and humidity in DB if it not exist
	def createTableInDb(self):
		humd_table_exist = "SHOW TABLES LIKE 'HUMID'"
		self.cursor.execute(humd_table_exist)
		result_hum = self.cursor.fetchone()
		
		if result_hum:
			print ('There is a table named HUMID')
		else:
			# there are no tables named "HUMID" thus creating a table
			self.cursor.execute("CREATE TABLE HUMID(id INT NOT NULL AUTO_INCREMENT, Humd VARCHAR(20) NOT NULL, time_stamp VARCHAR(20) NOT NULL, PRIMARY KEY (id));")
		
		temp_table_exist = "SHOW TABLES LIKE 'TEMP'"
		self.cursor.execute(temp_table_exist)
		
		result_temp = self.cursor.fetchone()
		
		if result_temp:
			print ('there is a table named TEMP')
		else:
			# there are no tables named "TEMP" thus creating a atble
			self.cursor.execute("CREATE TABLE TEMP(id INT NOT NULL AUTO_INCREMENT, Temp VARCHAR(20) NOT NULL, time_stamp VARCHAR(20) NOT NULL, PRIMARY KEY (id));")
		
#Function to put humidity entries into DB	
	def putHumidityValInDb(self,humdVal,humdTime):
		self.cursor.execute("INSERT INTO HUMID (Humd, time_stamp) VALUES (%s, %s)", (humdVal, humdTime))
				
		self.mariadb_connection.commit()

#Function to put temperature entries into DB	
	def putTemperatureValInDb(self, tempVal,tempTime):
		
		self.cursor.execute("INSERT INTO TEMP (Temp, time_stamp) VALUES (%s, %s)", (tempVal, tempTime))
		self.mariadb_connection.commit()

#Function to get humidity entry and plot humidity graph
	def getHumidityValFromDb(self):
		#https://pythonprogramminglanguage.com/pyqtgraph-plot/
		self.hum_plt = pg.plot(title="Humidity Plot")
		self.hum_plt.showGrid(x=True,y=True)
		
		self.hum_plt.setLabel('left', 'Humidity', units='%')
		self.hum_plt.setLabel('bottom', 'Number', units='')
						
		fetch_humid = "SELECT * FROM HUMID ORDER BY id DESC LIMIT 10"
		self.cursor.execute(fetch_humid)
		
		hum_values = self.cursor.fetchall()
		hum_list = [temp[1] for temp in hum_values]
		hum_list = list(map(float, hum_list))
		hum_list.reverse()
		
		x = range(0,len(hum_list))
		if(self.Units == 'F'):
			hum_list = [((i *  9/5)+32) for i in hum_list]
		
		self.hum_plt.plot(x, hum_list, pen='r', symbolPen='b', symbolBrush=0.2)
		
		return hum_list

#Function to get temperature entry and plot temperature graph	
	def getTemperatureValFromDb(self):
		self.temp_plt = pg.plot(title="Temperature Plot")
		self.temp_plt.showGrid(x=True,y=True)
		
		self.temp_plt.setLabel('left', 'Temperature', units=self.Units)
		self.temp_plt.setLabel('bottom', 'Number', units='')
				
		fetch_temp = "SELECT * FROM TEMP ORDER BY id DESC LIMIT 10"
		self.cursor.execute(fetch_temp)
		
		temp_values = self.cursor.fetchall()
		temp_list = [temp[1] for temp in temp_values]
		temp_list = list(map(float, temp_list))
		temp_list.reverse()
		
		x = range(0,len(temp_list))
		
		if(self.Units == 'F'):
			temp_list = [((i *  9/5)+32) for i in temp_list]

		self.temp_plt.plot(x, temp_list, pen='b', symbolPen='b', symbolBrush=0.2)
		
		return temp_list

def main():
	app = QtWidgets.QApplication([])
	application = eid_project1()
	application.show()
	app.exec()


if __name__ == "__main__":
	main()

