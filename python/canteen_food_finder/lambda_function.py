import http.client
import boto3
import json
import os
from datetime import date, datetime, timedelta

dynamodbClient = boto3.client('dynamodb')
sesClient = boto3.client('ses')


# Mensa Lüneburg - ID: 140
# Meals Request: https://sls.api.stw-on.de/v1/locations/140/menu/2022-08-29/2022-09-01
# Soy Gyros -> Name: "Soja-Gyros mit veganem Dip"


def buildHTMLContent(meals):
    htmlContent = "Seid gegrüßt, Liebhaber der guten Kost! <br><br>"
    htmlContent += "Ich habe Euch eine äußerst frohe Kunde zu überbringen, "
    htmlContent += "denn es ist Das eingetreten, was niemand mehr erwartet hat. "
    htmlContent += "Es gibt leckeres Essen in der <b>Leuphana Kombüse</b>! <br><br>"
    htmlContent += "Folgende Delikatessen sind angekündigt: <br>"
    for meal in meals:
        name = meal["name"]
        date = meal["date"]
        htmlContent += f"<br> {name} - {date}<br>"
    htmlContent += "<br><br>Sieh selbst und staune auf https://stw-on.de/lüneburg/essen/mensa"
    return htmlContent


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


def send_emails(recipients):
    for recipient in recipients:
        print(recipient)
        meals = recipient["meals"]
        print(meals)
        if not meals:
            continue
        meal_dates = sorted(list(map(lambda meal: meal["date"], meals)))
        latest_meal_date = datetime.strptime(meal_dates[-1], "%Y-%m-%d").date()
        email_address = recipient["email"]
        notified_for = recipient["notified_for"]
        if notified_for is None or notified_for != latest_meal_date:
            try:
                sesClient.send_email(
                    Source='henrik.pruess@posteo.de',
                    Destination={
                        'ToAddresses': [email_address]
                    },
                    Message={
                        'Subject': {
                            'Data': 'Lieblingsessen im Anflug 🍔'
                        },
                        'Body': {
                            'Html': {
                                'Data': buildHTMLContent(meals)
                            }
                        }
                    }
                )
                update_recipient(recipient, latest_meal_date)
            except Exception as e:
                print(e)
        else:
            print(f"Recipient {email_address} is already informed about the latest meal")


def format_Date(unformatted_date):
    if not unformatted_date:
        return None
    date = datetime.strptime(unformatted_date, "%Y-%m-%d").date()
    return date
    
    
def get_recipients_with_available_meals(recipients, available_meals):
    for recipient in recipients:
       meal_searchterms = recipient["meals"]
       available_wanted_meals = [a for a in available_meals for m in meal_searchterms if m.casefold() in a["name"].casefold()]
       recipient["meals"] = available_wanted_meals
    return recipients


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


def get_available_meals():
    today = datetime.today().strftime("%Y-%m-%d")
    todayPlus14 = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")
    connection = http.client.HTTPSConnection('sls.api.stw-on.de')
    connection.request("GET", f"/v1/locations/140/menu/{today}/{todayPlus14}")
    response = connection.getresponse()
    responseData = response.read()
    meals = json.loads(responseData)["meals"]
    return meals


def lambda_handler(event, context):
    available_meals = get_available_meals()
    if not available_meals:
        return "No meals available", 200
    recipients = get_recipients()
    if not recipients:
        return "No recipients found", 200
    recipients_with_available_meals = get_recipients_with_available_meals(recipients, available_meals)
    if not recipients_with_available_meals:
        return "No relevant meals found", 200
    send_emails(recipients_with_available_meals)
    return "Recipients notified", 200