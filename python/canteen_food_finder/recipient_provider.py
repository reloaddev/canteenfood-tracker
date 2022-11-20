import boto3
from datetime import date, datetime

dynamodbClient = boto3.client('dynamodb')


def format_Date(unformatted_date):
    if not unformatted_date:
        return None
    date = datetime.strptime(unformatted_date, "%Y-%m-%d").date()
    return date


def get_recipients():
    try:
        scanResult = dynamodbClient.scan(TableName="Recipient")
        raw_recipients = scanResult["Items"]
        recipients = list(map(lambda r: {
            "email": r["Email"]["S"],
            "meals": r["Meals"]["SS"],
            "notified_for": format_Date(r["Notified_For"]["S"])
        }, raw_recipients))
    except Exception as exc:
        print("Database error", exc)
        emails = []
    return recipients


def update_recipient(recipient, last_meal_date):
    email_address = recipient["email"] 
    last_meal_date_str = last_meal_date.strftime("%Y-%m-%d")
    try:
        response = dynamodbClient.update_item(
            TableName="Recipient",
            Key={"Email": {"S": email_address}},
            UpdateExpression="set Notified_For = :n",
            ExpressionAttributeValues={
                ":n": {"S": last_meal_date_str},
            },
            ReturnValues="UPDATED_NEW"
        )
    except:
        print("DynamoDB update failed")
        raise