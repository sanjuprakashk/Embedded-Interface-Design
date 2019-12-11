#!/usr/bin/python3 
import pyaudio
import wave
import os
import boto3
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import copy

client = boto3.client('lex-runtime', region_name="us-east-1")

def button_callback(channel):
    print("Button was pushed!")
    #setup audio input stream
    sleep (1)
    os.system('arecord -D plughw:1,0 -d 3 -r 16000 -f S16_LE -t wav test1.wav &&  aplay test1.wav')

    #CONVERTING SPEECH TO TEXT USING AMAZON LEX
    obj = wave.open('/home/pi/Desktop/Embedded-Interface-Design/Project5/test1.wav','rb')
    response_lex = client.post_content(
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
    
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter

GPIO.cleanup() # Clean up
