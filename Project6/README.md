# EID Project 6

## Developers
Srinath Shanmuganadhan  
Sanju Prakash Kannioth

## Notes and Installation Instructions

sudo apt update
sudo apt upgrade

### py_qt
sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools  
sudo apt-get install qttools5-dev-tools

### my_sql and Mariadb
sudo apt-get install mariadb-server-10.0  
sudo apt-get install python3-mysql.connector

sudo mysql -u root -p -h localhost  
	*enter password*  
	CREATE DATABASE super_project;  
	USE eid_project1;  
	CREATE USER 'srisan'@'localhost' IDENTIFIED BY 'srisan1234';  
	GRANT ALL PRIVILEGES ON super_project.* TO 'srisan'@'localhost';  
	FLUSH PRIVILEGES
	quit  

sudo service mysql restart  

### setting up pyaudio
	sudo apt-get install git
	sudo git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
	sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
	sudo apt-get install python-dev
	cd pyaudio
	sudo python setup.py install
	
### AWS python setup
	pip3 install boto3
	
### node js
	npm install websocket

	
## Instruction to run program
 

## Project Work

### Srinath Shanmuganadhan:
### Work 
	AWS lex, Audio, database, Node.js



### Sanju Prakash Kannioth
### Work
	AWS poly, SQS, Camera, pyQt, HTML client

## References
https://www.youtube.com/watch?v=Gy0C9g16DW0&feature=youtu.be
https://classes.engineering.wustl.edu/ese205/core/index.php?title=Audio_Input_and_Output_from_USB_Microphone_%2B_Raspberry_Pi
https://docs.aws.amazon.com/lex/latest/dg/API_runtime_PostContent.html
https://metacpan.org/pod/Paws::LexRuntime::PostContent


