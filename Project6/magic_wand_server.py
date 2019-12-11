#!/usr/bin/python3 

'''
magic_wand_server.py: This file contains the code that does all the server services

@developers: Sanju Prakash Kannioth, Srinath Shanmuganadhan
@date: 12/11/2019
@references: https://www.youtube.com/watch?v=D0iCHFXHb_g
			 EID Projects 1,2,3
''' 
from PyQt5 import QtWidgets, QtGui, QtCore
from server_ui import Ui_Dialog
import sys
import boto3
import json
import mysql.connector

class magic_wand_server(QtWidgets.QDialog):
	def __init__(self):
		''' 
		Initialization of GUI
		'''
		super(magic_wand_server, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		# Variables to store percentage data for images
		self.percentImagesCorrect = 0
		self.percentImagesWrong = 0
		
		# Variables to store percentage data for voice commands
		self.percentVoiceCorrect = 0
		self.percentVoiceWrong = 0
		

		self.numImagesCorrect = 0
		self.numVoiceCorrect = 0
		self.numVoiceWrong = 0
		
		self.counter = 1;
		
		# Variables to store latest label obtained
		self.latestLabel = 'default'
		
		self.total_messages = 0
		self.totalImages = 0
		
		self.ui.getImageButton.clicked.connect(self.getImage)
		self.ui.getPercentButton.clicked.connect(self.getPercentData)
		
		self.mariadb_connection = mysql.connector.connect(user='srisan', password='srisan1234', database='super_project')
		self.cursor = self.mariadb_connection.cursor()
		self.create_table()
		
	def getPercentData(self):
		''' 
		function that updates percentage data for images and voice commands
		'''

		# valid voice commands
		valid_voice_commands = ['Identifio', 'Wrongo', 'Correcto']
		invalid_voice_commands = 'Invalid'
		
		sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"
		sqs_client = boto3.client('sqs', region_name='us-east-1')
		num_msgs=1
		wait_time=0
		visibility_time=5
		
		doneFlag = 0
		
		# loop over all available entries in the SQS queue
		while(doneFlag == 0):
			try:
				msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
											  MaxNumberOfMessages=num_msgs,
											  WaitTimeSeconds=wait_time,
											  VisibilityTimeout=visibility_time)
			
				index = 0
				msgs = msgs['Messages']
				voice_command_correct = self.numVoiceCorrect
				image_command_correct = self.numImagesCorrect
				# loop over each message received and extract the body of the response
				for i in msgs:
					self.total_messages = self.total_messages + 1
					incoming_message = json.loads(msgs[index]['Body'])
					sqs_client.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=msgs[index]['ReceiptHandle'])
					#print(incoming_message)
					voice_command = incoming_message[0]['voiceCommand']
					index = index + 1
					if voice_command in valid_voice_commands:
						voice_command_correct = voice_command_correct + 1
						if(voice_command == 'Correcto'):
							self.latestLabel = incoming_message[1]['Label']
							self.totalImages = self.totalImages + 1
							image_command_correct = image_command_correct + 1
							#print("Image correct. Label = "+ str(self.latestLabel))
						elif(voice_command == 'Wrongo'):
							self.latestLabel = incoming_message[1]['Label']
							self.totalImages = self.totalImages + 1
							#print("Image wrong. Label = "+ str(self.latestLabel))
					
						else:
							pass
						print(voice_command)
					self.numImagesCorrect = image_command_correct
					self.numVoiceCorrect = voice_command_correct
					if(self.total_messages == 0):
						pass
					else:
						self.percentVoiceCorrect = (float(voice_command_correct / self.total_messages) * 100)
						self.percentVoiceWrong = 100 - self.percentVoiceCorrect

					if(self.totalImages == 0):
						pass
					else:
						self.percentImagesCorrect = (float(image_command_correct / self.totalImages) * 100)
						self.percentImagesWrong = 100 - self.percentImagesCorrect
					self.put_data(self.latestLabel, self.percentImagesCorrect, self.percentImagesWrong, self.percentVoiceCorrect, self.percentVoiceWrong)
				
			except:
				doneFlag = 1

		# update GUI with percentage data
		if(self.total_messages == 0):
			pass
		else:
			self.percentVoiceCorrect = (float(voice_command_correct / self.total_messages) * 100)
			self.percentVoiceWrong = 100 - self.percentVoiceCorrect
			self.ui.lcdPercentCorrectVoice.display(self.percentVoiceCorrect)
			self.ui.lcdPercentWrongVoice.display(self.percentVoiceWrong)
		
		if(self.totalImages == 0):
			pass
		else:
			self.percentImagesCorrect = (float(image_command_correct / self.totalImages) * 100)
			self.percentImagesWrong = 100 - self.percentImagesCorrect
		
			self.ui.lcdPercentCorrectImages.display(self.percentImagesCorrect)
			self.ui.lcdPercentWrongImages.display(self.percentImagesWrong)
				
		self.ui.imageLabel.setText(str(self.latestLabel))
		
		doneFlag = 0
		
	def getImage(self):
		''' 
		function that gets latest image from s3 bucket and displays it on GUI
		'''

		try:
			s3 = boto3.resource('s3', region_name='us-east-1')
			bucket_name = "test-bucket-eid-123"
			object_name = self.latestLabel+".jpg"
			print(object_name)
			s3.Bucket(bucket_name).download_file(object_name, object_name)
			self.ui.imageView.setPixmap(QtGui.QPixmap(object_name))
		except:
			pass
		
	def create_table(self):
		''' 
		function that creates mysql db if it does not exist
		'''

		magicwand_table_exist = "SHOW TABLES LIKE 'MAGICWAND1'"
		self.cursor.execute(magicwand_table_exist)
		result_magicwand = self.cursor.fetchone()
		if result_magicwand:
			print ('there is a table named MAGICWAND1')
		else:
			print ('there are no tables named "MAGICWAND1"')
			self.cursor.execute("CREATE TABLE MAGICWAND1(id INT NOT NULL AUTO_INCREMENT, Label VARCHAR(20) NOT NULL, Image_correct VARCHAR(20) NOT NULL, Image_wrong VARCHAR(20) NOT NULL, Voice_correct VARCHAR(20) NOT NULL, Voice_wrong VARCHAR(20) NOT NULL, PRIMARY KEY (id));")
	
	def put_data(self, label, img_correct, img_wrong,voice_correct, voice_wrong):
		''' 
		function to data into mysql db
		'''
		self.cursor.execute("INSERT INTO MAGICWAND1 (Label, Image_correct, Image_wrong, Voice_correct, Voice_wrong) VALUES (%s, %s, %s, %s, %s)", (label, img_correct, img_wrong, voice_correct, voice_wrong))
		print("Record inserted successfully into MAGICWAND able")
		self.mariadb_connection.commit()


def main():
	'''
	Main function that executes the GUI 
	'''
	app = QtWidgets.QApplication([])
	application = magic_wand_server()
	application.show()
	app.exec()
	
	
	#mariadb_connection.close()


if __name__ == "__main__":
	main()
