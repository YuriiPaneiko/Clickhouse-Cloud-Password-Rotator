import requests
import boto3
import json
import os

secrets_manager = boto3.client('secretsmanager')
API_KEY = secrets_manager.get_secret_value(
    SecretId="clickhouse_cloud_token")['SecretString']

CONFIGURATION = os.environ['CONFIGURATION']
ENVIRONMENT = os.environ['ENVIRONMENT']
CL_CLOUD_API = os.environ['CL_CLOUD_API']
ORGANIZATION_ID = os.environ['ORGANIZATION_ID']
SERVICE_NAME = os.environ['SERVICE_NAME']

secret_name = CONFIGURATION + "-" + \
    ENVIRONMENT + "-clickhouse-credentials"

headers = {
    'Authorization': 'Basic ' + API_KEY
}

def get_service_id(CL_CLOUD_API, ORGANIZATION_ID, headers):
    global service_id
    services_list = requests.request(
        "GET", CL_CLOUD_API + "/organizations/" + ORGANIZATION_ID + "/services/", headers=headers)

    services_list = json.loads(services_list.text)['result']

    for service in services_list:
        if service['name'] == SERVICE_NAME:
            service_id = service['id']
    return service_id


def change_password(CL_CLOUD_API, ORGANIZATION_ID, service_id, headers):
    global new_password
    req = requests.request('PATCH', CL_CLOUD_API + "/organizations/" +
                           ORGANIZATION_ID + "/services/" + service_id + "/password", headers=headers)
    res = json.loads(req.text)['result']
    new_password = res["password"]
    return new_password


def update_secret():
    secret_value = json.loads(secrets_manager.get_secret_value(
        SecretId=secret_name)['SecretString'])
    secret_value['password'] = new_password

    secrets_manager.update_secret(
        SecretId=secret_name,
        SecretString=json.dumps(secret_value)
    )


def lambda_handler(event, context):
    get_service_id(CL_CLOUD_API=CL_CLOUD_API,
                   ORGANIZATION_ID=ORGANIZATION_ID, headers=headers)
    change_password(CL_CLOUD_API=CL_CLOUD_API,
                    ORGANIZATION_ID=ORGANIZATION_ID, service_id=service_id, headers=headers)
    update_secret()