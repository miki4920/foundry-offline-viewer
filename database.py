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


def truncate_table(table_name):
    table = dynamodb_resource.Table(table_name)
    table_key_names = [key.get("AttributeName") for key in table.key_schema]
    projection_expression = ", ".join('#' + key for key in table_key_names)
    expression_attr_names = {'#' + key: key for key in table_key_names}
    page = table.scan(ProjectionExpression=projection_expression, ExpressionAttributeNames=expression_attr_names)
    with table.batch_writer() as batch:
        while page["Count"] > 0:
            for item_keys in page["Items"]:
                batch.delete_item(Key=item_keys)
            if 'LastEvaluatedKey' in page:
                page = table.scan(
                    ProjectionExpression=projection_expression, ExpressionAttributeNames=expression_attr_names,
                    ExclusiveStartKey=page['LastEvaluatedKey'])
            else:
                break
