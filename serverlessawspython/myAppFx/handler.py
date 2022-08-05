import json

def main(event, context):

    try:
        receivedParams = event["queryStringParameters"]

        response = {
            "statusCode": 200,
            "body": json.dumps(event),
            "params": json.dumps(receivedParams)
        }
        return response
    except:
        return {"errorMsg": "you gotta return some param or this will fail"}


if __name__ == "__main__":
    main('', '')
