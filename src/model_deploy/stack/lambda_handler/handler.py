import os
import boto3
import json

sagemaker = boto3.client("sagemaker-runtime")

ENDPOINT_NAME = os.environ["ENDPOINT_NAME"]

def proxy(event,context) :
    try:
        response = sagemaker.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps(event["body"]),
        )
        return {
            "statusCode": 200,
            "body": response["Body"].read().decode("utf-8"),
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e),
        }