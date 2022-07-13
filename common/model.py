import boto3
import os

dynamodb = boto3.client("dynamodb", region_name=os.getenv("REGION"), aws_access_key_id=os.getenv("ACCESS_KEY"),
                          aws_secret_access_key=os.getenv("SECRET_KEY"))


def create_table():
    characters = dynamodb.create_table(
        TableName='characters',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName='characters')

    items = dynamodb.create_table(
        TableName='items',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 20,
            'WriteCapacityUnits': 20
        }
    )
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName='items')