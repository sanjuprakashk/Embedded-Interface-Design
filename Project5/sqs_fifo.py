'''

https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-sqs.html

'''
import boto3

# Get the service resource
sqs = boto3.client('sqs', region_name='us-east-1')

# Get the queue
queueUrl = "https://sqs.us-east-1.amazonaws.com/837538385441/magic_wand.fifo"


response = sqs.send_message(
    QueueUrl=queueUrl,
    MessageBody="testing321",
    MessageGroupId='test1',
    MessageDeduplicationId='1'
)

# The response is NOT a resource, but gives you a message ID and MD5
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))