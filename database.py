import boto3
import os

from dynamodb_json import json_util as json

dynamodb = boto3.client("dynamodb", region_name=os.getenv("REGION"), aws_access_key_id=os.getenv("ACCESS_KEY"),
                        aws_secret_access_key=os.getenv("SECRET_KEY"))
dynamodb_resource = boto3.resource("dynamodb", region_name=os.getenv("REGION"),
                                   aws_access_key_id=os.getenv("ACCESS_KEY"),
                                   aws_secret_access_key=os.getenv("SECRET_KEY"))


def get_batch_items(items):
    # CAN ONLY DO 100 ITEMS AT A TIME
    response = dynamodb.batch_get_item(
        RequestItems={
            'items': {
                'Keys': [{"id": {"S": item}} for item in items],
                'ConsistentRead': True
            }
        },
        ReturnConsumedCapacity='TOTAL'
    )["Responses"]["items"]
    return json.loads(response)


def fetch_character(character):
    character = json.loads(character)
    character["items"] = get_batch_items(character["items"])
    return character


def fetch_data():
    characters = dynamodb.scan(TableName="characters")["Items"]
    for i, character in enumerate(characters):
        characters[i] = fetch_character(character)
    return characters[::-1]
