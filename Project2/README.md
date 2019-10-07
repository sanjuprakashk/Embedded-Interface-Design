# EID Project 2

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
sudo apt update
sudo apt upgrade

### node.js and npm
npm init
npm install
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
Restart your terminal
npm install node
nvm install 10.16.3
npm install webserver  

### tonado
pip3 install tornado    
pip3 install asyncio  

## Instruction to run program
From this directory do - python3 eid_project2.py  

## Project Work

### Srinath Shanmuganadhan:
Worked with the Node js server

### Sanju Prakash Kannioth  
Worked with Tornado Webserver and HTML Client

## Error Conditions

If server is not running, clicking of button on the HTML will pop up Error message that the required server is unavailable
If the DHT22 does not respond, error is displayed on the HTML page

## Extra credit
Completed implementation of displaying graph of last 10 Humidity readings from the python app on the HTML page  

## References  
https://www.w3schools.com/nodejs/nodejs_mysql.asp  
https://www.pubnub.com/blog/nodejs-websocket-programming-examples/  
https://os.mbed.com/cookbook/Websockets-Server  
http://www.tornadoweb.org/en/stable/  
https://wiki.python.org/moin/WebServers  
https://stackoverflow.com/questions/46680654/how-to-read-a-python-dictionary-from-the-jquery 
https://stackoverflow.com/questions/43248211/parse-json-data-with-jquery  
https://www.youtube.com/watch?v=MRVHxQ2SiOM  
https://www.mssqltips.com  
https://www.w3schools.com  
https://canvasjs.com/html5-javascript-line-chart/  

