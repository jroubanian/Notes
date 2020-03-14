# SAMPLE FTP ETL
# All imports at top of script
from __future__ import print_function # this is a good habit
from collections import OrderedDict
import os
import datetime as dt
import pysftp
import numpy as np
import pandas as pd
import psycopg2 as pg
import boto3

from dstk.utils.data_cleaning import clean_columns


# DOC STRING
"""
# What does this script do?
This script pulls files dropped in our ftp, cleans them, and loads them to a
database.

# When and How does this script run?
It runs daily at 9am as scheduled by our crontab on an ec2 instance in aws.

# What are it's outputs and where does it store data.
The script downloads files to the local machine (wherever that may be) temporarily
and cleans them before uploading to s3 and our database in aws. The local files
are deleted at the completion of script execution.

# How do I run it and what arguments does it take if any
you can run this script by calling `python sample_etl.py` when in the same
directory as the file. The file takes no arguments, but it loads environmental
variables, such as credentials, s3 paths, and database location, from
configuration files as defined below.

"""
# Set working directory to same directory as this script.
# This ensures that filepaths are relative to the same place as where the
#+ script is running.
os.setwd(os.path.abspath(os.path.dirname(__file__)))

# DEFINE ENVIRONMENTAL VARIABLES
today = dt.date.today()

# credential files
ftp_creds_fp = './config/ftp_creds'
aws_creds_fp = './config/aws_credentials'
db_creds_fp = './config/db_credentials'

# ftp filepaths
ftp_root_dir = '.'
ftp_file_name = 'Som e Dumb F__ile Name cuz cLIents are 1NSANE.csv'
ftp_file_path = os.path.join(ftp_root_dir, ftp_file_name)

# AWS filepaths
s3_bucket_name = 'my_s3_bucket'
s3_folder_path = 'ETL/reports{}/'.format(today.strftime('%b%Y'))
s3_file_name = 'data_file_{}.csv'.format(today.strftime('%Y%m%d'))
s3_filepath = os.path.join(s3_folder_path, s3_file_name)

redshift_schema = 'my_etl_schema'
redshift_table = 'example_table'

# Local Filepaths
staging_folder = './tempFiles/'
clean_file_name = 'data_file_{}.csv'.format(today.strftime('%Y%m%d'))
staging_filepath = os.path.join(staging_folder, clean_file_name)

# The expected output data dtypes
tv_dtypes_dic = OrderedDict({
    'week_of': 'datetime64[ns]',
    'timestamp': 'datetime64[ns, UTC]',
    'daypart': 'str',
    'dma_id': 'str',
    'dma_name': 'str',
    'market': 'str',
    'station_id': 'str',
    'station_name': 'str',
    'program_name': 'str',
    'ad_id': 'str',
    'ad_name': 'str',
    'ad_length': 'int',
    'cost': 'float',
    'impressions': 'int',
    'trps': 'float',
    'source_file': 'str'
})


###################
# ETL FUNCTIONS
###################

def download_ftp_file(ftp_creds_fp, remote_filepath, local_filepath):
    """
    This functions instantiates a connection to an ftp server and downloads
    the file at `remote_filepath` to local file at `local_filepath`.

    ftp_cred_fp: STR; filepath to plain text file with the host, port, user and
        password for the ftp server separated by new lines.
    remote_filepath: STR; the filepath for the file to download from the FTP
        server.
    local_filepath: STR; the local file path to write the downloaded file to.


    RETURNS: STR; the local file path where the file was downloaded.

    """
    # parse credentials
    with open(ftp_creds_fp, 'r') as f:
        ftp_host, ftp_port, ftp_user, ftp_pwd = [l for l in f]

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    # note the indentation and formatting of args to a function
    ftp = pysftp.Connection(
            host=host,
            username=user,
            password=pwd,
            port=int(port),
            cnopts=cnopts
    )

    ftp.get(remote_filepath, local_filepath)

    return local_filepath


def clean_ftp_file(filepath, clean_fp=staging_filepath):
    """
    This function performs all cleaning operations on the downloaded file.
    This can include renaming columns, parsing data types, and replacing values.

    filepath: STR; path to local file to open and clean.
    clean_fp: STR; output path to write clean file to.

    """
    # Read in filepath, making sure to parese the time as a string not an int
    #+ that way it doesn't remove leading zeros
    df = pd.read_csv(filepath, dtype={'Time Aired': str})

    # standardize columns to snake case
    df.columns = clean_columns(df)

    # rename columns to more meaningful name
    df.rename(columns = {
                        'station':'station_name',
                        'station1':'station_id',
                        'tape_aired':'ad_id',
                        'tape_name_aired':'ad_name',
                        'program_aired':'program_name',
                        'length':'ad_length',
                        'cleared': 'cost',
                        'ip2554': 'impressions',
                        'rp2554': 'trps'
            }, inplace = True)

    # fill missing values for numeric columns with 0s
    df.fillna({'trps':0, 'impressions':0, 'cost':0}, inplace=True)

    # parse timestamp as combination of date and time columns
    df['time_aired'] = df.time_aired.str.zfill(4)
    df['timestamp'] = pd.to_datetime(df.date_aired.str.cat(df.time_aired, sep=' '))

    # make sure dtypes are correct and as expected by our Database
    for col, dtype in dtype_dic.items():
        df[col] = df[col].astype(dtype)


    # Add more cleaning operations below if needed
    ############



    ############

    df.to_csv(clean_fp, index=False)

    return clean_fp

# note the vertically aligned function arguments
def load_to_s3(clean_filepath, credential_fp, s3_bucket=s3_bucket_name,
               s3_upload_path=s3_filepath):
    """
    DOCSTRING HERE
    """
    # Parse Credentials
    with open(aws_creds_fp, 'r') as f:
        aws_access_key, aws_secret_key = [l for l in f]

    # create a client
    client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )

    # upload
    client.upload_file(clean_filepath, Bucket=s3_bucket, Key=s3_upload_path)

    return s3_upload_path


def load_to_db(s3_filepath, aws_creds, db_creds, s3_bucket=s3_bucket_name,
               db_schema=redshift_schema, db_table=redshift_table):
    """
    DOCSTRING HERE
    """

    with open(aws_creds, 'r') as f:
        aws_access_key, aws_secret_key = [l for l in f]

    with open(db_creds, 'r') as f:
        host, port, dbname, user, pwd = [l for l in f]

    # Establish Connections
    conn = psycopg2.connect(host,port,dbname, user, pwd)
    cur = conn.cursor()

    copy_cmd = """
    COPY {}.{} FROM s3://{}/{}
    ACCESS_KEY_ID {}
    SECRET_ACCESS_KEY {}
    """.format(db_schema, db_table, s3_bucket, s3_filepath,
               aws_access_key, aws_secret_key)
    # Execute Copy
    cur.execute(copy_cmd)

    # Commit and Close Connections!!!
    conn.commit()
    conn.close()

    return

###################
# MAIN FUNCTION
###################

def main():
    '''
    Main function. Runs etl.
    Arguments gathered from the environment variables at top of script.
    '''

    # SETUP LOGGING
    log_level = 'INFO'
    log_fp = './logs/ftp_etl_log_{}.log'.format(today.strftime('%Y%m%d'))
    logger = logging.getLogger('ftp_etl_logger')
    logger.setLevel(log_level)
    log_handle = logging.FileHandler(log_fp)
    logger.addHandler(log_handle)

    logger.info("""

    STARTING ETL AT {}
    -------------------
    """.format(today.strftime('%Y-%m-%d %H:%M:%S')))

    logger.info("Pulling file from FTP...")
    downloaded_fp = download_ftp_file(ftp_creds_fp, ftp_file_path, staging_filepath)

    logger.info("Cleaning data file...")
    clean_fp = clean_ftp_file(downloaded_fp, clean_fp=staging_filepath)

    logger.info("Loading clean file to s3...")
    s3_upload_path = load_to_s3(clean_fp, aws_creds_fp)

    logger.info("Populating Redshift Table...")
    load_to_db(s3_upload_path, credential_fp=aws_creds_fp)

    logger.info('ETL Completed at {}'.format(dt.datetime.now()))
    logger.info('==============================================='

    return



if __name__ == '__main__':
    main(load_to_db, s)