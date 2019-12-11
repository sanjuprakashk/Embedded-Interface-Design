'''

https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-sqs.html

'''
import boto3
import json

# Get the service resource
sqs = boto3.client('sqs', region_name='us-east-1')
i = 0
# Get the queue
queueUrl = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"

test_msg1 = json.dumps([{"voiceCommand": "Correcto"}, {"Label" : "car1"}, {"key4" : str(i)}])

i = i + 1
test_msg2 = json.dumps([{"voiceCommand": "Correcto"}, {"Label" : "car2"}, {"key4" : str(i)}])

i = i + 1
test_msg3 = json.dumps([{"voiceCommand": "Wrongo"}, {"Label" : "car3"}, {"key4" : str(i)}])

i = i + 1
test_msg4 = json.dumps([{"voiceCommand": "Invalid"}, {"Label" : "car4"}, {"key4" : str(i)}])

response = sqs.send_message(
    QueueUrl=queueUrl,
    MessageBody=test_msg1,
    MessageGroupId='test2'
)

response = sqs.send_message(
    QueueUrl=queueUrl,
    MessageBody=test_msg2,
    MessageGroupId='test2'
)

response = sqs.send_message(
    QueueUrl=queueUrl,
    MessageBody=test_msg3,
    MessageGroupId='test2'
)

response = sqs.send_message(
    QueueUrl=queueUrl,
    MessageBody=test_msg4,
    MessageGroupId='test2'
)
# The response is NOT a resource, but gives you a message ID and MD5
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))