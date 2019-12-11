#!/usr/bin/python3 
import pyaudio
import wave
import os
import boto3
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import copy
import picamera
import json
import random

latestLabel = ' '

def button_callback(channel):
    global latestLabel
    print("Button was pushed!")
    #setup audio input stream
    sleep (1)
    os.system('arecord -D plughw:1,0 -d 3 -r 16000 -f S16_LE -t wav test1.wav &&  aplay test1.wav')

    #CONVERTING SPEECH TO TEXT USING AMAZON LEX
    obj = wave.open('/home/pi/Desktop/Embedded-Interface-Design/Project5/test1.wav','rb')
    
    lex_client = boto3.client('lex-runtime', region_name="us-east-1")
    response_lex = lex_client.post_content(
        botName='MagicWand',
        botAlias='MagicWand',
        userId='test',
        contentType='audio/l16; rate=16000; channels=1',
        accept='text/plain; charset=utf-8',
        inputStream=obj.readframes(96044)
    )
    
    response = response_lex['message']
    if response == "Sorry, can you please repeat that?":
        response = 'Invalid'
        
    print(response)
    
    if response == 'Identifio':
        camera = picamera.PiCamera()
        camera.vflip = True
        camera.capture('test_img.jpg')
        aws_client = boto3.client("rekognition",
                          # aws_access_key_id =access_key_id,
                          # aws_secret_access_key = secret_access_key,
                          region_name='us-east-1')
        photo = "test_img.jpg"

        with open(photo, "rb") as source_image:
            source_bytes = source_image.read()

        response = aws_client.detect_labels(Image={'Bytes': source_bytes}, 
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
        
        latestLabel = response['Labels'][0]['Name']

        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
            
    elif response == 'Correcto' or response == 'Wrongo':
        sqs_client = boto3.client('sqs', region_name='us-east-1')

        queueUrl = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"

        label = response['Labels'][0]['Name']
        sendToSqs = json.dumps([{"voiceCommand": response}, {"Label" : str(latestLabel)}])

        response_sqs = sqs_client.send_message(
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
    else:
        sqs_client = boto3.client('sqs', region_name='us-east-1')

        queueUrl = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"
        
        sendToSqs = json.dumps([{"voiceCommand": "Invalid"}, {"Label" : str(latestLabel)}])

        response_sqs = sqs_client.send_message(
            QueueUrl=queueUrl,
            MessageBody=sendToSqs,
            MessageGroupId='wand',
            MessageDeduplicationId=str(random.random())            
        )

    

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up
