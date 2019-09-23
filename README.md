# EID Project 1

## Developers
Srinath Shanmuganadhan  
Sanju Prakash Kannioth

## Installation Instructions

sudo apt update
sudo apt upgrade

### py_qt
sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools  
sudo apt-get install qttools5-dev-tools

### py_qt graph  
pip3 install pyqtgraph

### DHT library  
pip3 install Adafruit_DHT

### my_sql and Mariadb
sudo apt-get install mariadb-server-10.0  
sudo apt-get install python3-mysql.connector  

sudo mysql -u root -p -h localhost  
	*enter password*  
	CREATE DATABASE eid_project1;  
	USE eid_project1;  
	CREATE USER 'sansri'@'localhost' IDENTIFIED BY 'sansri1234';  
	GRANT ALL PRIVILEGES ON eid_project1.* TO 'sansri'@'localhost';  
	quit  

sudo service mysql restart  

### Sensor Connection
Connect DHT22 sensor voltage pin to pin 1 on the RPI  
Connect DHT22 sensor gnd pin to pin 6 on the RPI  
Connect DHT22 sensor data pin to pin 7 on the RPI  


## Project Work

### Srinath Shanmuganadhan:
Worked with the SQL setup and all work related to DB

### Work
Creation of DB, adding user and granting user privilges to the DB  
Adding the humidity and temperature values into the DB   
Extracting the last 10 entries from the db for humidity and temperature  


### Sanju Prakash Kannioth
Worked on pyqt design and sensor interfacing  

### Work
Created GUI using qt designer  
Interfaced DHT22 sensor  
Integrated PyQt ui with sensor  

## Project Additions  
Clicking the change units button will change the temperature from Celcius to Farenheit 
and vice-versa

##References
https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py  
https://pythonprogramminglanguage.com/pyqtgraph-plot/  
https://stackoverflow.com/  
https://askubuntu.com/questions/1014947/mysql-connector-python-importerror-no-module-named-mysql  
https://www.youtube.com/watch?v=lCfSKtPADYw  
https://www.mssqltips.com  
https://www.w3schools.com
