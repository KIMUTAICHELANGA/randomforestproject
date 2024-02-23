import os
import yaml
import boto3
import logging
import requests

logging.basicConfig(level=logging.INFO)
api_client = boto3.client('apigateway')

def get_api_url():
    list_of_apis = api_client.get_rest_apis()
    api_id = list_of_apis['items'][0]['id']

    aws_region = boto3.session.Session().region_name

    api_url = f'https://{api_id}.execute-api.{aws_region}.amazonaws.com/prod'
    return api_url

def test_endpoint():
    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
        logging.info('API works')
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    
if __name__ == '__main__':
    with open('config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    # get endpoint name and config environment
    logging.info("Get api name from config")
    api_name = config['api_name']

    api_url = get_api_url()

    # send a test datapoint
    test_payload = {
        "columns": [
            "MedInc",
            "HouseAge",
            "AveRooms",
            "AveBedrms",
            "Population",
            "AveOccup",
            "Latitude",
            "Longitude",
        ],
        "index": [0],
        "data": [
            [8.3252, 41, 6.9841269841, 1.0238095238, 322, 2.5555555556, 37.88, -122.23]
        ],
    }

    results = test_api(api_url, test_payload)