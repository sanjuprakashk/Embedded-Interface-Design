#!/usr/bin/python3 

'''
lambdafunction.py: This file contains the code that 

@authors: Sanju Prakash Kannioth, Srinath Shanmuganadhan

@date: 10/23/2019

@references: https://docs.aws.amazon.com/lambda/latest/dg/with-sns-example.html
https://startupnextdoor.com/adding-to-sqs-queue-using-aws-lambda-and-a-serverless-api-endpoint/
''' 

from __future__ import print_function
  
import json
import boto3
  
print('Loading function')
  
def lambda_handler(event, context):
  
    # Parse the JSON message 
    eventText = json.dumps(event);

    # Print the parsed JSON message to the console; you can view this text in the Monitoring tab in the Lambda console or in the CloudWatch Logs console
    print('Received event: ', eventText)
  
    # Create an SNS client
    sns = boto3.client('sns')
    
     # Create an SQS client
    sqs = boto3.resource('sqs')
    
    if event['id']=='alert':
      # Publish a message to the specified topic
      response = sns.publish (
        TopicArn = 'arn:aws:sns:us-east-1:987678846235:My_IoT_SNS_Topic',
        Message = eventText,
      )
    else:
      # Send message to SQS Queue
      queue = sqs.get_queue_by_name(QueueName='EID_Project3_SQS')
      response = queue.send_message(MessageBody=json.dumps(event))
