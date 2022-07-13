from dynamodb_json import json_util as json

from common.model import dynamodb


def get_batch_items(items):
    # CAN ONLY DO 100 ITEMS AT A TIME
    response = dynamodb.batch_get_item(
        RequestItems={
            'items': {
                'Keys': [{"id": {"N": str(item)}} for item in items],
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


def fetch_characters():
    characters = dynamodb.scan(TableName="characters")["Items"]
    for i, character in enumerate(characters):
        characters[i] = fetch_character(character)
    return characters[::-1]
