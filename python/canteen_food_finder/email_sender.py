import boto3
from datetime import datetime

sesClient = boto3.client('ses')

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


def send_emails(recipients):
    for recipient in recipients:
        meals = recipient["meals"]
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