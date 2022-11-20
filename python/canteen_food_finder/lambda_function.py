from meal_provider import get_available_meals
from recipient_provider import get_recipients
from email_sender import send_emails


# Mensa Lüneburg - ID: 140
# Meals Request: https://sls.api.stw-on.de/v1/locations/140/menu/2022-08-29/2022-09-01
# Soy Gyros -> Name: "Soja-Gyros mit veganem Dip"


def get_recipients_with_available_meals(recipients, available_meals):
    for recipient in recipients:
       meal_searchterms = recipient["meals"]
       available_wanted_meals = [a for a in available_meals for m in meal_searchterms if m.casefold() in a["name"].casefold()]
       recipient["meals"] = available_wanted_meals
    return recipients


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