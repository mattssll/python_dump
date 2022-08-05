import boto3
from configs.s3config import AWS_S3_PUBLIC_KEY,AWS_S3_SECRET_KEY
import pandas as pd
from google.cloud import bigquery
from google.cloud import bigquery_storage
import datetime
import io
from io import StringIO
from datetime import date
import os
#from datetime import datetime

import sys
import time
#from IOError import *

class Boto3ReadWrite:
    def createbotoclient(self):
            s3client = boto3.client(
                "s3",
                aws_access_key_id=AWS_S3_PUBLIC_KEY,
                aws_secret_access_key=AWS_S3_SECRET_KEY
                )
            return s3client

    def createbotosession(self):
            my_session = boto3.session.Session(
                aws_access_key_id=AWS_S3_PUBLIC_KEY,
                aws_secret_access_key=AWS_S3_SECRET_KEY
                )
            s3 = my_session.resource('s3')
            return s3

    def getsorteddatesdf(self, timestampcolumn, schemaandtable, offset_rework): # add something here so I can rework only something like 10 days
            client = bigquery.Client()
            dfdates = (
                client.query(f"""
                                select distinct cast(date({timestampcolumn}) as string) as timestamp 
                                from {schemaandtable} 
                                where date({timestampcolumn}) >= '{offset_rework}' """ )
                .result()
                .to_dataframe()
            )
            dfdt = dfdates[timestampcolumn].unique().tolist()
            dfdt.sort()
            return dfdt

    


    def csvtos3(i,dfsample,s3client,bucket,prefix,day):
        buffers = 'buffers'+str(i)
        buffers = StringIO()
        dfsample = dfsample.to_csv(buffers, index=False, encoding='iso-8859-1')
        print("sending file: "+str(i))
        responsecsv = s3client.put_object(
            Body=buffers.getvalue(),
            Bucket=bucket,
            Key=prefix+day+'.csv')
        print("file sent: "+str(i)+" "+prefix+day)
        buffers.close()
        return responsecsv


    def jsontos3(i,dfsample,s3client,bucket,prefix,day):
        buffers = 'buffers'+str(i)
        buffers = StringIO()
        dfsample = dfsample.to_json(buffers, orient ="table", index=False, force_ascii=False)
        print("sending file: "+str(i))
        responsecsv = s3client.put_object(
            Body=buffers.getvalue(),
            Bucket=bucket,
            Key=prefix+day+'.json')
        print("file sent: "+str(i)+" "+prefix+day)
        buffers.close()
        return responsecsv


    def sqltos3clientwriter(self, bucket, prefix, query, fileformat, schemaandtable, offset_rework):
        offset_rework_tos3 = datetime.date.today() + datetime.timedelta(offset_rework)
        offset_rework_tos3 = str(offset_rework_tos3)
        query = query.format(schemaandtable,offset_rework_tos3)
        # bq and s3 client
        client = bigquery.Client()
        s3client = boto3.client(
            "s3",
            aws_access_key_id=AWS_S3_PUBLIC_KEY,
            aws_secret_access_key=AWS_S3_SECRET_KEY
            )
        # get data from query and put in df
        df = (
                client.query(query)
                .result()
                .to_dataframe()
            )
        sorted_dates = Boto3ReadWrite.getsorteddatesdf('self', 'timestamp', schemaandtable, offset_rework_tos3)
        i=1
        ii=i
        for day in sorted_dates:
            dfsample = df[df['timestamp'].dt.date.astype(str).str.contains(day)]  
            if fileformat == 'csv':
                Boto3ReadWrite.csvtos3(i,dfsample,s3client,bucket,prefix,day)
                print("done csv number ", str(i))
                i=i+1
            elif fileformat == 'json':
                Boto3ReadWrite.jsontos3(i,dfsample,s3client,bucket,prefix,day)
                print("done json number ", str(ii))
                ii=ii+1
            elif fileformat == 'csvandjson':   
                Boto3ReadWrite.csvtos3(i,dfsample,s3client,bucket,prefix,day)
                print("done csv number ", str(i))
                i=i+1
                Boto3ReadWrite.jsontos3(i,dfsample,s3client,bucket,prefix,day)
                print("done json number ", str(ii))
                ii=ii+1


    def s3csvtobigquery(
                        self, 
                        bucket,
                        bucket_path,
                        schemaandtablegetdates, 
                        schemaandtabletoinsert,
                        project_id, 
                        timestampcolumn, 
                        prefix, 
                        offset_rework, 
                        process_mode,
                        read_from_s3tobq,
                        read_from_format,
                        timestampcolumnsconvert,
                        drop_or_delete
                        ):
        s3client = Boto3ReadWrite.createbotoclient('selfarg')
        if process_mode == 'all_objects_no_date':
            #bq part
            client = bigquery.Client()
            if drop_or_delete == "delete":
                query = f"DELETE FROM {schemaandtabletoinsert} WHERE TRUE"
            if drop_or_delete == "drop":    
                query = f"DROP TABLE {schemaandtabletoinsert}"
            try:
                print(f"log: {drop_or_delete} data/table for rework period")
                query_job = client.query(query)
                query_job.result()
                print(f"log:{drop_or_delete} data/table for rework period")
                time.sleep(3)
            except:
                print("log: table probably didn't exist to be deleted")
            # s3 actions
            s3 = Boto3ReadWrite.createbotosession('selfarg')
            my_bucket = s3.Bucket(bucket)
            objects_in_bucket = []
            for my_bucket_object in my_bucket.objects.filter(Delimiter='/', Prefix=bucket_path.split("/")[1]+"/"):
                objects_in_bucket.append(my_bucket_object.key.split("/")[-1])
            i=0
            for object in objects_in_bucket:
                if object.endswith(str(read_from_format)):                    
                    i= i+1 
                    print(f"log: sending file {i} with name: {object} to bq")
                    obj = s3client.get_object(Bucket=bucket, Key=f'{read_from_s3tobq}{object}')
                    buffers = 'buffers'+str(i)
                    buffers = io.BytesIO
                    if read_from_format == '.json':
                        df = pd.read_json(buffers(obj['Body'].read()), lines=True, convert_dates = True, dtype=False)
                    elif read_from_format == '.csv':
                        print(type(timestampcolumnsconvert["data"]))
                        df = pd.read_csv(buffers(obj['Body'].read()), 
                                        encoding="UTF-8",parse_dates=timestampcolumnsconvert["data"], date_parser=pd.to_datetime)
                        for item in timestampcolumnsconvert["data"]:
                            df[item] = df[item].dt.tz_localize(None)
                    df.fillna("", inplace = True) 
                    print(df.head(5))
                    #df.#(schemaandtabletoinsert, project_id=project_id, if_exists = 'append')
                    print(f"log: sent file {i} with name: {object} to bq")
                #except e:
             #       print(sys.exc_info()[0])



                        
            return "log: data was successfully sent to bq from s3"

        if process_mode=='daily_w_offset':
            # working dates for bq
            offset_rework_tobq = datetime.date.today() + datetime.timedelta(offset_rework)
            offset_rework_tobq = str(offset_rework_tobq)
            
            # do build client function
            
            #client.delete_table(schemaandtabletoinsert, not_found_ok=True)  # Make an API request.
            #print("Deleted table '{}'.".format(schemaandtabletoinsert))
            # make this also a function
            if drop_or_delete == "delete":
                query = f"""
                    DELETE FROM {schemaandtabletoinsert}
                    WHERE timestamp >= '{offset_rework_tobq}' """
                    
            if drop_or_delete == "drop":    
                query = f"DROP TABLE {schemaandtabletoinsert}"
            try:
                print(f"log: {drop_or_delete} data/table for rework period")
                query_job = client.query(query)
                query_job.result()
                print("log: deleted data for rework period")
                time.sleep(10)
            except:
                print("log: table probably didn't exist to be deleted")
            # sending to s3
            sorted_dates = Boto3ReadWrite.getsorteddatesdf('self', 'timestamp', schemaandtablegetdates, offset_rework_tobq)
            i=0
            for date in sorted_dates:
                i= i+1 
                try:
                    print(f"log: sending file {i} with name: {prefix}{date}.csv to bq")
                    obj = s3client.get_object(Bucket=bucket, Key=f'{prefix}{date}.csv')
                    buffers = 'buffers'+str(i)
                    buffers = io.BytesIO
                    if read_from_format == '.json':
                        df = pd.read_json(buffers(obj['Body'].read()), lines=True, encoding="UTF-8")
                    elif read_from_format == '.csv':
                        df = pd.read_csv(buffers(obj['Body'].read()), encoding="UTF-8")
                    df.fillna("", inplace = True) 
                    df.to_gbq(schemaandtabletoinsert,project_id=project_id, if_exists = 'append')
                    print(f"log: sent file {i} with name: {prefix}{date}.csv to bq")
                except:           
                    print(f"error log: failed to send file {i} with name: {prefix}{date}.csv to bq")
                    print(sys.exc_info()[0])
            return "all good"


# parameters
boto = Boto3ReadWrite()
project_id = os.getenv('PROJECT_ID', 'google_project_id')
schemaandtable = "custom_metrics_abi.chimera_messages"
prefix = 'test_all/order_sent_view'
bucket = 'ftp-abinbev'
bucket_path = 'ftp-abinbev/conversational_messages'
schemaandtabletoinsert = 'temporal.testtimestampfroms3csv'
schemaandtablegetdates = 'custom_metrics_abi.chimera_messages'
timestampcolumn = 'timestamp'
read_from_s3tobq = 'conversational_messages/'
read_from_format = '.csv'
timestampcolumnsconvert = {"data" : ["timestamp"]}# if csv, have to convert timestamp columns
process_mode = 'all_objects_no_date'
query_mode = 'all_in_one', # all_in_one or one_query_by_day # to be implemented this feature
drop_or_delete = 'drop' #
# from bq put into s3

"""
#boto.sqltos3clientwriter(bucket=bucket, 
                        query="select * from {} where date(timestamp) >= '{}' order by timestamp desc" ,
                        prefix=prefix,
                        fileformat='csvandjson',
                        schemaandtable=schemaandtable,
                        offset_rework = -7)
"""
# read from csv and put in bq
boto.s3csvtobigquery(bucket='ftp-abinbev',
                    schemaandtabletoinsert= schemaandtabletoinsert,
                    schemaandtablegetdates= schemaandtablegetdates,
                    project_id= project_id,
                    prefix=prefix,
                    offset_rework = -99999, # this var is not used in all objects no date process mode
                    process_mode = process_mode,
                    timestampcolumn= timestampcolumn,
                    bucket_path = bucket_path,
                    read_from_s3tobq = read_from_s3tobq,
                    read_from_format = read_from_format,
                    drop_or_delete = drop_or_delete,
                    timestampcolumnsconvert = timestampcolumnsconvert)
# missing to write qa metrics, do query counting for offset_rework and save it in our qa metrics as another operator

"""


def testsz(bucket,filespath):
    s3client = Boto3ReadWrite.createbotoclient('selfarg')

        #bq part
    client = bigquery.Client()
    s3 = Boto3ReadWrite.createbotosession('selfarg')
    my_bucket = s3.Bucket(bucket)
    objects_in_bucket = []
    #for my_bucket_object in my_bucket.objects.filter(Delimiter='/', Prefix=source_path_files.split("/")[1]+"/"):
     #       objects_in_bucket.append(my_bucket_object.key.split("/")[-1])
    #print(objects_in_bucket)
    for my_bucket_object in my_bucket.objects.filter(Delimiter='/', Prefix=filespath):#'#.filter(Delimiter='/', Prefix=bucket_path.split("/")[1]+"/"):
        #objects_in_bucket.append(my_bucket_object.last_modified)
        #objects_in_bucket.append(my_bucket_object.key.split("/")[-1]
        print(my_bucket_object)
    #print(max(objects_in_bucket))   
testsz(bucket = "ftp-abinbev", filespath = 'conversational_messages/')
"""