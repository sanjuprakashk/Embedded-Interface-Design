from PyQt5 import QtWidgets, QtGui, QtCore
from eid_project1_ui import Ui_Dialog
import sys
import Adafruit_DHT

class eid_project1(QtWidgets.QDialog):
	def __init__(self):
		super(eid_project1, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		self.Units = 'C'
		
		self.tempVal = 0
		self.humVal = 0
		
		self.tempLimit = 100
		self.humLimit = 100
		
		self.sensorReadingCount = 0
		
		self.ui.tempLimitLine.setText("0.0")
		self.ui.humLimitLine.setText("0.0")
		
		self.ui.tempLimitLine.setText("100.0")
		self.ui.humLimitLine.setText("100.0") 
			
		self.ui.setTempLimitButton.clicked.connect(self.setTempLimit)
		
		self.ui.setHumLimitButton.clicked.connect(self.setHumLimit)
		
		self.ui.changeUnitsButton.clicked.connect(self.changeUnits)
		
		self.ui.immediateValButton.clicked.connect(self.getImmediateVal)
		
		
		
		''' https://www.programcreek.com/python/example/99607/PyQt5.QtCore.QTimer '''
		self.periodicTimer = QtCore.QTimer(self)
		self.periodicTimer.timeout.connect(self.sensorUpdate)
		self.periodicTimer.start(10000)
		
	def changeUnits(self):
		if(self.Units == 'C'):
			self.Units = 'F'
		else:
			self.Units = 'C'
		
		self.updateDisplay()
	
	def setTempLimit(self):
		self.tempLimit = float(self.ui.tempLimitLine.text())
		self.updateDisplay()
		
	def setHumLimit(self):
		self.humLimit = float(self.ui.humLimitLine.text())
		self.updateDisplay()
	
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
		self.ui.timestampDisplayLine.setText(str(QtCore.QTime.currentTime().toString(QtCore.Qt.DefaultLocaleLongDate)))
		
		print("Humidity limit = ", humLimit)
		print("Temperature limit = ", tempLimit)
		
		self.ui.tempDisplayLine.setText(str(tempVal) + " " + self.Units)
		self.ui.humDisplayLine.setText(str(humVal) + " %")
		
	def updateError(self):
		self.ui.tempDisplayLine.setText("Error")
		self.ui.humDisplayLine.setText("Error")
	
	def getImmediateVal(self):
		self.humVal , self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4, delay_seconds=0.2)
		
		if self.humVal is not None and self.tempVal  is not None:
			self.updateDisplay()
		else:
			self.updateError()
	
	def sensorUpdate(self):
		''' https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py '''
		self.humVal , self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4, delay_seconds=0.2)
		self.sensorReadingCount = self.sensorReadingCount + 1
		
		if self.humVal is not None and self.tempVal  is not None:
			self.updateDisplay()
		else:
			self.updateError()
		
		if(self.sensorReadingCount == 5):
			self.periodicTimer.stop()
			#sys.exit(1)


app = QtWidgets.QApplication([])
application = eid_project1()
application.show()
app.exec()
