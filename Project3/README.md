# EID Project 3

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

### Install AWS IoT Python SDK
git clone https://github.com/aws/aws-iot-device-sdk-python
cd aws-iot-device-sdk-python
sudo python setup.py install

## Instruction to run program
From this directory do - python3 eid_project3.py  

## Project Work

### Srinath Shanmuganadhan:
### Work
Worked with MQTT and AWS elements Iot Core, SNS,Lamda


### Sanju Prakash Kannioth
### Work
Worked with AWS elements lambda, SQS and HTML Client

## Project Additions  
Clicking button retrieves number of elements in the SQS Queue

## Project Issues
SQS reference material for HTML Client was extremely hard to find

## References
https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/getting-started-browser.html
https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SQS.html
https://stackoverflow.com/questions/55934468/get-all-messages-from-aws-sqs-in-nodejs
https://www.w3schools.com/jsref/met_table_deleterow.asp
https://www.w3schools.com/tags/att_table_align.asp
https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html
https://techblog.calvinboey.com/raspberrypi-aws-iot-python/
https://docs.aws.amazon.com/lambda/latest/dg/with-sns-example.html
https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-making-api-requests.html
https://startupnextdoor.com/adding-to-sqs-queue-using-aws-lambda-and-a-serverless-api-endpoint/


