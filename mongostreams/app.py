import os
import pymongo
from bson.json_util import dumps


client = pymongo.MongoClient(os.environ['CHANGE_STREAM_DB'])
db = client.teststreams
try:
    resume_token = None
    pipeline = [{'$match': {'operationType': 'insert'}}]
    with db.streams.watch(pipeline) as stream:
        for insert_change in stream:
            print(insert_change)
            resume_token = insert_change['_id']
except pymongo.errors.PyMongoError:
    # The ChangeStream encountered an unrecoverable error or the
    # resume attempt failed to recreate the cursor.
    if resume_token is None:
        # There is no usable resume token because there was a
        # failure during ChangeStream initialization.
        logging.error('...')
    else:
        # Use the interrupted ChangeStream's resume token to create
        # a new ChangeStream. The new stream will continue from the
        # last seen insert change without missing any events.
        with db.collection.watch(
                pipeline, resume_after=resume_token) as stream:
            for insert_change in stream:
                print(insert_change)