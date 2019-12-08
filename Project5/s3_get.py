'''

https://docs.aws.amazon.com/code-samples/latest/catalog/python-s3-get_object.py.html
https://boto3.amazonaws.com/v1/documentation/api/1.9.42/guide/s3-example-download-file.html

'''

import boto3
import matplotlib.pyplot as plt

# Get the service resource
s3 = boto3.resource('s3', region_name='us-east-1')

bucket_name = "test-bucket-eid-123"
object_name = "2.jpg"

# response = s3.get_object(Bucket=bucket_name, Key=object_name)

s3.Bucket(bucket_name).download_file(object_name, object_name)

# response.download_file("test.jpg")

# print(stream)

photo = "test_img.jpg"

with open(object_name, "rb") as source_image:
    source_bytes = source_image.read()

    
# plt.figure(0)
# plt.imshow(source_bytes)