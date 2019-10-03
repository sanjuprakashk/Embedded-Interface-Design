from PyQt5 import QtWidgets, QtGui, QtCore
from eid_project2_ui import Ui_Dialog
import sys
import Adafruit_DHT
import mysql.connector
import pyqtgraph as pg

import threading

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import asyncio


class eid_project2(QtWidgets.QDialog):
    '''
    eid_project2 class containing initialization of GUI and callback functions
    '''
    def __init__(self):
        '''
        Initialization of GUI
        '''
        super(eid_project2, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # DB connection object
        self.mariadb_connection = mysql.connector.connect(user='sansri',
                                                          password='sansri1234',
                                                          database='eid_project1')

        self.cursor = self.mariadb_connection.cursor()

        self.Units = 'C'  # Variable to store correct measurement unit selection

        self.tempVal = 0  # Vraible to store temperature value
        self.humVal = 0  # Vraible to store humidity value

        self.tempLimit = 100  # Vraible to store temperature limit
        self.humLimit = 100  # Vraible to store humidity limit

        self.sensorReadingCount = 0  # Vraible to store number of readings obtained
        self.timeStamp = 0  # Vraible to store timestamp

        self.getFromTornado = 0
        self.tornadoTempVal = ""
        self.tornadoHumVal = ""

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
        Function to update display
        '''
        humLimit = float("{0:.2f}".format(self.humLimit))
        humVal = float("{0:.2f}".format(self.humVal))

        if(self.Units == 'C'):
            tempVal = float("{0:.2f}".format(self.tempVal))
            tempLimit = float("{0:.2f}".format(self.tempLimit))
        else:
            tempVal = float("{0:.2f}".format((self.tempVal * 9/5) + 32))
            tempLimit = float("{0:.2f}".format((self.tempLimit * 9/5) + 32))

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
        self.humVal, self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4,
                                                             delay_seconds=0.2)

        self.timeStamp = QtCore.QTime.currentTime().toString(
            QtCore.Qt.DefaultLocaleLongDate)

        if self.humVal is not None and self.tempVal is not None:
            if(self.getFromTornado == 0):
                self.updateDisplay()
            else:
                 self.tornadoTempVal = str(self.tempVal)
                 self.tornadoHumVal = str(self.humVal)
                 self.getFromTornado = 0
        else:
            if(self.getFromTornado == 0):
                self.updateError()
            else:
                 self.tornadoTempVal = "Error"
                 self.tornadoHumVal = "Error"
                 self.getFromTornado = 0

    def sensorUpdate(self):
        '''
        Function to update the sensor for every 15 seconds
        '''
        self.humVal, self.tempVal = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4,
                                                             delay_seconds=0.2)
        self.sensorReadingCount = self.sensorReadingCount + 1

        self.timeStamp = QtCore.QTime.currentTime().toString(
            QtCore.Qt.DefaultLocaleLongDate)

        if self.humVal is not None and self.tempVal is not None:
            self.updateDisplay()
            self.putHumidityValInDb(self.humVal, self.timeStamp)
            self.putTemperatureValInDb(self.tempVal, self.timeStamp)
        else:
            self.updateError()

        

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
            print('There is a table named HUMID')
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
            print('there is a table named TEMP')
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
        self.hum_plt.showGrid(x=True, y=True)

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

        x = range(0, len(hum_list))

        if(self.Units == 'F'):
            hum_list = [((i * 9/5) + 32) for i in hum_list]

        self.hum_plt.plot(x, hum_list, pen='r', symbolPen='b', symbolBrush=0.2)

        return hum_list

    def getTemperatureValFromDb(self):
        '''
        Function to get temperature entry from DB and plot temperature graph
        '''
        self.temp_plt = pg.plot(title="Temperature Plot")
        self.temp_plt.showGrid(x=True, y=True)

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

        x = range(0, len(temp_list))

        if(self.Units == 'F'):
            temp_list = [((i * 9/5) + 32) for i in temp_list]

        self.temp_plt.plot(x, temp_list, pen='b',
                           symbolPen='b', symbolBrush=0.2)

        return temp_list


class WSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, guiObject):
        self.guiObject = guiObject

    def open(self):
        print('new connection')

    def on_message(self, message):
        if(message == "Get Temperature"):
            self.guiObject.getFromTornado = 1
            self.guiObject.getImmediateVal()
            self.write_message(str(self.guiObject.tornadoTempVal))
        elif(message == "Get Humidity"):
            self.guiObject.getFromTornado = 1
            self.guiObject.getImmediateVal()
            self.write_message(str(self.guiObject.tornadoHumVal))

    def on_close(self):
        print ('connection closed')

    def check_origin(self, origin):
        return True


def thread_tornado(application):
    asyncio.set_event_loop(asyncio.new_event_loop())
    application = tornado.web.Application([
    (r'/ws', WSHandler, {'guiObject': application}),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

def main():
    '''
    Main function that executes the GUI 
    '''
    app = QtWidgets.QApplication([])
    application = eid_project2()
    application.show()

    # thread1 = threading.Thread(target=thread_qt, args=(application,))
    thread2 = threading.Thread(target=thread_tornado, args=(application,))

    thread2.setDaemon(True)

    # thread1.start()
    thread2.start()

    app.exec()
    
    # thread2.join()

if __name__ == "__main__":
    main()

