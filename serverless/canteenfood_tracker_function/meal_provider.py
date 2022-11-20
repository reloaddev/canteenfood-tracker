from datetime import datetime, timedelta
import http.client
import json

def get_available_meals():
    today = datetime.today().strftime("%Y-%m-%d")
    todayPlus14 = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")
    connection = http.client.HTTPSConnection('sls.api.stw-on.de')
    connection.request("GET", f"/v1/locations/140/menu/{today}/{todayPlus14}")
    response = connection.getresponse()
    responseData = response.read()
    meals = json.loads(responseData)["meals"]
    return meals
