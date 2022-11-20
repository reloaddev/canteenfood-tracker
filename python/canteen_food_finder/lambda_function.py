from meal_provider import get_available_meals
from recipient_provider import get_recipients_with_available_meals
from email_sender import send_emails


# Mensa Lüneburg - ID: 140
# Meals Request: https://sls.api.stw-on.de/v1/locations/140/menu/2022-08-29/2022-09-01
# Soy Gyros -> Name: "Soja-Gyros mit veganem Dip"
   

def lambda_handler(event, context):
    available_meals = get_available_meals()
    if not available_meals:
        return "No meals available", 200
    recipients = get_recipients_with_available_meals(available_meals)
    if not recipients:
        return "No recipients found", 200
    send_emails(recipients)
    return "Recipients notified", 200
