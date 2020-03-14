# Import python packages.
import pandas
import boto3
from datetime import date
import io
from sqlalchemy import create_engine

# Download file from s3 bucket into pandas dataframe.
bucket_name = "360ichilis"
#key = "Chilis DV Report-" + str(date.today()).replace('-', '') + '.csv'
key = "Chilis DV Report-" + '20180804' + '.csv'
cred_file = '/Users/brian.luong/OneDrive - Dentsu Aegis Network/Projects/Chilis/aws_credentials.txt'
creds = open(cred_file, 'r')
creds_list = creds.read().splitlines()
access_key = creds_list[0]
secret_key = creds_list[1]

try:
    s3 = boto3.client(
        's3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
    )
except:
    print('Connection to S3 failed.')

try:
#    print('Reading Data From S3')
#    s3_file = s3.get_object(Bucket=bucket_name, Key=key)
#    open_file = pandas.read_csv(io.BytesIO(s3_file['Body'].read()))
    open_file = pandas.read_csv('/Users/brian.luong/Downloads/Chilis DV Report-20180804.csv')
except:
    print('File download failed.')

# Rearranging open dataframe to match database columns.
open_file = open_file[[
    'Campaign',
    'Date',
    'Media Property',
    'Media Type',
    'Placement Code',
    'Placement Name',
    'Allowed Impressions',
    'Authentic Impressions',
    'Blocks',
    'Monitored Impressions',
    'Requests',
    'Unique Incidents',
    'Brand Safe Impressions',
    'Brand Safety Blocks',
    'Fraud/SIVT Blocks',
    'Fraud/SIVT Free Impressions',
    'Fraud/SIVT Incidents',
    'In Geo Impressions',
    'Out of Geo Blocks',
    'Out of Geo Incidents',
    'Authentic Display Viewable Impressions',
    'Display Measured Impressions',
    'Display Viewable Impressions',
    'Video Measured Impressions',
    'Video Viewable Impressions',
    ]]

# Set up database connection.
host = "10.19.9.117"
port = "5432"
database = "postgres"
username = "brian_luong"
password = "sideways_rose_streetcar"
table = "chilis.stg_doubleverify"

try:
    print('Connecting to DB')
    engine = create_engine('postgresql://' + username + ':' + password + '@' + host + ':' + port + "/" + database)
    conn = engine.raw_connection()
    cur = conn.cursor()
except:
    print ("Database connection failed")

# Load data into database.
try:
    print('Loading Data To DB')
    output = io.StringIO()
    open_file.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    print(open_file.Date.unique())
    cur.copy_from(output, table, null="")
    conn.commit()
    cur.close()
    conn.close()
except:
    print ("Loading data failed")