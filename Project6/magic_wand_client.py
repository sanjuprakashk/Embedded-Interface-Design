#!/usr/bin/python3 

'''
magic_wand_client.py: This file contains the code that does all the client services

@developers: Sanju Prakash Kannioth, Srinath Shanmuganadhan
@date: 12/11/2019
@references: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
             https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html#sqs
             https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html
             https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-runtime.html
             https://www.geeksforgeeks.org/random-numbers-in-python/
             https://stackoverflow.com/questions/27276135/python-random-system-time-seed
''' 

import pyaudio
import wave
import os
import boto3
import RPi.GPIO as GPIO
from time import sleep
import picamera
import json
import random

latestLabel = 'default'
# Instatiate the camera
camera = picamera.PiCamera()
debounceVar = 0



def button_callback():
    ''' 
    function that contains all client functionalties
    '''
    global latestLabel
    global camera
    global debounceVar
    sleep(1)
    if debounceVar == 1:
        debounceVar = 0
        return
    debounceVar = 1
    print("Button was pushed!")
    #setup audio input stream
    #sleep (1)
    
    # Turn on microphone and read for 3 secs
    os.system('arecord -D plughw:1,0 -d 3 -r 16000 -f S16_LE -t wav test1.wav &&  aplay test1.wav')

    #converting speech to text on amazon lex
    obj = wave.open(os.getcwd()+'/test1.wav','rb')
    
    # client object for lex
    lex_client = boto3.client('lex-runtime', region_name="us-east-1")
    response_lex = lex_client.post_content(
        botName='MagicWand',
        botAlias='MagicWand',
        userId='test',
        contentType='audio/l16; rate=16000; channels=1',
        accept='text/plain; charset=utf-8',
        inputStream=obj.readframes(96044)
    )
    
    # aws lex response
    response = response_lex['message']
    if response == "Sorry, can you please repeat that?":
        response = 'Invalid'
        
    print(response)
    
    if response == 'Identifio':
        camera.capture('test_img.jpg')
        
        # client object for rekognition client
        aws_client = boto3.client("rekognition",
                          region_name='us-east-1')
        photo = "test_img.jpg"

        # get bytes of image to send to rekoginition
        with open(photo, "rb") as source_image:
            source_bytes = source_image.read()

         # aws rekognition response
        response = aws_client.detect_labels(Image={'Bytes': source_bytes}, 
                                        MaxLabels=1)

        print(response['Labels'])


        # client object for aws polly client
        polly_client = boto3.Session(region_name='us-east-1').client('polly')

         # aws polly response
        response_polly = polly_client.synthesize_speech(VoiceId='Joanna',
                        OutputFormat='mp3', 
                        Text = 'Wand says '+response['Labels'][0]['Name'])

        file = open('speech.mp3', 'wb')
        file.write(response_polly['AudioStream'].read())
        file.close()
        
        latestLabel = response['Labels'][0]['Name']

        # playback recorded audio
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

            
    elif response == 'Correcto' or response == 'Wrongo':
        # client object for sqs
        sqs_client = boto3.client('sqs', region_name='us-east-1')

        queueUrl = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"

        sendToSqs = json.dumps([{"voiceCommand": response}, {"Label" : str(latestLabel)}])
        label = latestLabel

         # aws sqs response
        response_sqs = sqs_client.send_message(
            QueueUrl=queueUrl,
            MessageBody=sendToSqs,
            MessageGroupId='wand',
            MessageDeduplicationId=str(random.random())            
        )

        # rename to avoid overwriting in s3 bucket
        os.rename('test_img.jpg', label+".jpg")
        bucket_name = "test-bucket-eid-123"
        object_name = label+".jpg"
        file_name = object_name

        s3_client = boto3.client('s3')
        try:
            # aws s3 response
            response = s3_client.upload_file(file_name, bucket_name, object_name)
        except:
            print('s3 upload error')
    else:
        sqs_client = boto3.client('sqs', region_name='us-east-1')

        queueUrl = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"
        
        sendToSqs = json.dumps([{"voiceCommand": "Invalid"}, {"Label" : str(latestLabel)}])

        # aws sqs response
        response_sqs = sqs_client.send_message(
            QueueUrl=queueUrl,
            MessageBody=sendToSqs,
            MessageGroupId='wand',
            MessageDeduplicationId=str(random.random())
            )
    debounceVar = 0


button = 10 # GPIO pin number that attaches to the buttton
    
# setup gpio pin as input
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Loop until button press, do functions, loop again
while(True):
    button_state = GPIO.input(button)
    if  button_state == True:
        button_callback()
        while GPIO.input(button) == True:
            time.sleep(1)


GPIO.cleanup() # Clean up
