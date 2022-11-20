import functions_framework
import requests
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
import os
from datetime import date, datetime, timedelta
import sqlalchemy


# Mensa Lüneburg - ID: 140
# Meals Request: https://sls.api.stw-on.de/v1/locations/140/menu/2022-08-29/2022-09-01
# Soy Gyros -> Name: "Soja-Gyros mit veganem Dip", Id: 41761


def buildHTMLContent(soyGyrosMeals):
    htmlContent = "Seid gegrüßt, Liebhaber der guten Kost! <br><br>"
    htmlContent += "Ich habe Euch eine äußerst frohe Kunde zu überbringen, "
    htmlContent += "denn es ist Das eingetreten, was niemand mehr erwartet hat. "
    htmlContent += "Es gibt <b>Soja Gyros</b> in der <b>Leuphana Kombüse</b>! <br><br>"
    htmlContent += "Die Delikatesse ist für folgende Daten angekündigt: <br>"
    for meal in soyGyrosMeals:
        date = meal["date"]
        htmlContent += f"<br> {date}"
    htmlContent += "<br><br>Sieh selbst und staune auf https://stw-on.de/lüneburg/essen/mensa"
    return htmlContent


def updateRecipient(email_address, latestGyrosDate):
    stmt = sqlalchemy.text(f"""UPDATE recipient
                               SET notified_for = '{latestGyrosDate.strftime("%Y-%m-%d")}'
                               WHERE email = '{email_address}';""")
    print(stmt)
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername="postgresql+pg8000",
        username="postgres",
        password=os.environ.get("POSTGRESQL_PW", "Not set."),
        database="gyros",
        query=dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format("soygyrosfinder:europe-west3:gyros")})
      )
    )
    try:
        result = db.connect().execute(stmt)
        print(result)
    except Exception as exc:
        print("Database error", exc)


def sendEmails(recipients, gyrosMeals):
    gyrosDates = sorted(list(map(lambda gyrosMeal: gyrosMeal["date"], gyrosMeals)))
    if not gyrosDates:
        return
    latestGyrosDate = datetime.strptime(gyrosDates[-1], "%Y-%m-%d").date()
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY", "Not set."))
    for recipient in recipients:
        email_address = recipient[0]
        notified_for = recipient[1]
        if notified_for is None or notified_for != latestGyrosDate:
            message = Mail(
                to_emails=email_address,
                from_email=Email("pruess.henrik@gmail.com", "Soja Gyros Tracker"),
                subject="Es gibt Soja Gyros 🌱",
                html_content=buildHTMLContent(gyrosMeals)
            )
            sg.send(message)
            updateRecipient(email_address, latestGyrosDate)
        else:
          print(f"Recipient {email_address} is already informed about the latest meal")


def queryRecipients():
    stmt = sqlalchemy.text("SELECT * FROM recipient;")
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername="postgresql+pg8000",
        username="postgres",
        password=os.environ.get("POSTGRESQL_PW", "Not set."),
        database="gyros",
        query=dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format("soygyrosfinder:europe-west3:gyros")})
      )
    )
    try:
        recipients = db.connect().execute(stmt)
    except Exception as exc:
        print("Database error", exc)
        recipients = []
    return recipients


def queryGyrosMeals():
    today = datetime.today().strftime("%Y-%m-%d")
    todayPlus14 = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")
    response = requests.get(
      f"https://sls.api.stw-on.de/v1/locations/140/menu/{today}/{todayPlus14}"
    )
    allMeals = json.loads(response.text)["meals"]
    # Id 41761 identifies meal "Soja-Gyros mit veganem Dip"
    return list(filter(lambda meal: "Soja-Gyros" in meal["name"], allMeals))


@functions_framework.http
def find_soy_gyros(request):
    gyrosMeals = queryGyrosMeals()
    if not gyrosMeals:
        return "No gyros meals found", 200
    recipients = queryRecipients()
    if not recipients:
        return "No recipients found", 200
    sendEmails(recipients, gyrosMeals)
    return "Recipients notified", 200
