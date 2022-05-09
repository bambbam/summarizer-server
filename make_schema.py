import boto3


def create_user_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName="User",
        KeySchema=[
            {"AttributeName": "username", "KeyType": "HASH"},  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "username", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    return table


def create_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName="Video",
        KeySchema=[
            {"AttributeName": "key", "KeyType": "HASH"},  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "key", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    return table


if __name__ == "__main__":
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    user_table = create_user_table(dynamodb=dynamodb)
    print("userTable status:", user_table.table_status)
    video_table = create_movie_table(dynamodb=dynamodb)
    print("videoTable status:", video_table.table_status)
