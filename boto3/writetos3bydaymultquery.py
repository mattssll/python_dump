import boto3
from configs.s3config import AWS_S3_PUBLIC_KEY,AWS_S3_SECRET_KEY
from io import StringIO
import pandas as pd
from google.cloud import bigquery
from google.cloud import bigquery_storage
import datetime
import asyncio
import aioboto3
from boto3.dynamodb.conditions import Key

class Boto3ReadWrite:
    def getsorteddatesdf(self, timestampcolumn, schemaandtable):
            client = bigquery.Client()
            dfdates = (
                client.query(f"select distinct cast(date({timestampcolumn}) as string) as timestamp from {schemaandtable}")
                .result()
                .to_dataframe()
            )
            dfdt = dfdates[timestampcolumn].unique().tolist()
            dfdt.sort()
            return dfdt

    def csvtos3(i,dfsample,s3client,bucket,prefix,day):
        buffers = 'buffers'+str(i)
        buffers = StringIO()
        dfsample = dfsample.to_csv(buffers, index=False, encoding='latin-1')
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




    def sqltos3clientwriter(self, bucket, prefix, query, fileformat, schemaandtable):#, paths3, helper):
        # bq and s3 client
        client = bigquery.Client()
        s3client = boto3.client(
            "s3",
            aws_access_key_id=AWS_S3_PUBLIC_KEY,
            aws_secret_access_key=AWS_S3_SECRET_KEY
            )
        # get data from query and put in df
        querydates = "select distinct timestamp from " + schemaandtable
        sorted_dates = Boto3ReadWrite.getsorteddatesdf('self', 'timestamp', schemaandtable)
        i=1
        ii=i
        for day in sorted_dates:
            # bigquery
            df = (
                client.query(query.format(day))
                .result()
                .to_dataframe()
            )
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

        

boto = Boto3ReadWrite()
schemaandtable = "custom_metrics_abi.chimera_messages"
boto.sqltos3clientwriter(bucket='ftp-abinbev', 
                    query=f"select * from " + schemaandtable + " where date(timestamp) = '{}'",
                    prefix='test/chimera_',
                    fileformat='csvandjson',
                    schemaandtable=schemaandtable)


# %%
