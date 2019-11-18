#!/usr/bin/python3

import picamera
import boto3

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
    #             aws_access_key_id=,                     
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