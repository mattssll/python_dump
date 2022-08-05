import os
import pymongo
client = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB'])
for i in range(0, 1000000):
    print(client.teststreams.streams.insert_one({str(i): "world"+str(i) }).inserted_id)