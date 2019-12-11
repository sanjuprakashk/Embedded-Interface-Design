#!/usr/bin/python3

import picamera
import boto3
import json
import random
import os

''' 
https://www.geeksforgeeks.org/random-numbers-in-python/
https://stackoverflow.com/questions/27276135/python-random-system-time-seed
'''
import time
random.seed(time.time())

camera = picamera.PiCamera()
camera.vflip = True
camera.capture('test_img.jpg')


client = boto3.client("rekognition",
                      # aws_access_key_id =access_key_id,
                      # aws_secret_access_key = secret_access_key,
                      region_name='us-east-1')
photo = "test_img.jpg"

with open(photo, "rb") as source_image:
    source_bytes = source_image.read()

response = client.detect_labels(Image={'Bytes': source_bytes}, 
                                MaxLabels=1)

print(response['Labels'])

polly_client = boto3.Session(
    # aws_access_key_id=,                     
    # aws_secret_access_key=,
    region_name='us-east-1').client('polly')

response_polly = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = 'Wand says '+response['Labels'][0]['Name'])

file = open('speech.mp3', 'wb')
file.write(response_polly['AudioStream'].read())
file.close()

import pygame
pygame.mixer.init()
pygame.mixer.music.load("speech.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

sqs = boto3.client('sqs', region_name='us-east-1')

queueUrl = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"

label = response['Labels'][0]['Name']
sendToSqs = json.dumps([{"voiceCommand": "Wrongo"}, {"Label" : str(response['Labels'][0]['Name'])}])

response_sqs = sqs.send_message(
    QueueUrl=queueUrl,
    MessageBody=sendToSqs,
    MessageGroupId='wand',
    MessageDeduplicationId=str(random.random())
    
)

os.rename('test_img.jpg', label+".jpg")
bucket_name = "test-bucket-eid-123"
object_name = label+".jpg"
file_name = object_name

s3_client = boto3.client('s3')
try:
    response = s3_client.upload_file(file_name, bucket_name, object_name)
except:
    print('s3 upload error')
