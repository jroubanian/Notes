#This script connects to an S3 bucket and downloads contents to a local directory

# Importing required modules
import boto3
import botocore

# Adding Credentials

BUCKET_NAME = '360i-infra-test' # replace with your bucket name
KEY = 'awscloud.jpg' # replace with your object key

s3 = boto3.resource('s3')

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'awscloud_local.jpg')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise