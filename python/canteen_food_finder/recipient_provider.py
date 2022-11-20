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
        print("Database SCAN failed", exc)
        raise
    return recipients


def get_recipients_with_available_meals(available_meals):
    recipients = get_recipients()
    for recipient in recipients:
        meal_searchterms = recipient["meals"]
        available_wanted_meals = [a for a in available_meals for m in meal_searchterms if m.casefold() in a["name"].casefold()]
        available_wanted_meals = list(map(lambda m: {
            "name": m["name"],
            "date": m["date"]
        }, available_wanted_meals))
        recipient["meals"] = available_wanted_meals
    recipients_with_available_meals = list(filter(lambda r: r["meals"], recipients))
    return recipients_with_available_meals
