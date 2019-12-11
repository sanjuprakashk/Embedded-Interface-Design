from PyQt5 import QtWidgets, QtGui, QtCore
from server_ui import Ui_Dialog
import sys
import boto3
import json

class magic_wand_server(QtWidgets.QDialog):
	def __init__(self):
		''' 
		Initialization of GUI
		'''
		super(magic_wand_server, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		self.percentImagesCorrect = 0
		self.percentImagesWrong = 0
		
		self.percentVoiceCorrect = 0
		self.percentVoiceWrong = 0
		
		self.numImagesCorrect = 0
		
		self.numVoiceCorrect = 0
		self.numVoiceWrong = 0
		
		self.counter = 1;
		
		self.latestLabel = ' '
		
		self.total_messages = 0
		self.totalImages = 0
		
		self.ui.getImageButton.clicked.connect(self.getImage)
		self.ui.getPercentButton.clicked.connect(self.getPercentData)
		
	def getPercentData(self):
		valid_voice_commands = ['Identifio', 'Wrongo', 'Correcto']
		invalid_voice_commands = 'Invalid'
		
		sqs_queue_url = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"
		sqs_client = boto3.client('sqs', region_name='us-east-1')
		num_msgs=1
		wait_time=0
		visibility_time=5
		
		doneFlag = 0
	
		voice_command_correct = 0
		image_command_correct = 0
		
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
				
			except:
				doneFlag = 1
				print("erorr")
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
		s3 = boto3.resource('s3', region_name='us-east-1')
		bucket_name = "test-bucket-eid-123"
		object_name = self.latestLabel+".jpg"
		print(object_name)
		s3.Bucket(bucket_name).download_file(object_name, object_name)
		self.ui.imageView.setPixmap(QtGui.QPixmap(object_name))

def main():
	'''
	Main function that executes the GUI 
	'''
	app = QtWidgets.QApplication([])
	application = magic_wand_server()
	application.show()
	app.exec()


if __name__ == "__main__":
	main()
