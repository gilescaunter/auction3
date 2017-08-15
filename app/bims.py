import requests
import json
from flask import g

#All you need here to connect to Bims and get information
#Log the user in and return the token to use for all other requests
def authenticate_user():
    url = "https://bims-uat.bca.com/api/v1/integration/auths"
    headers = {
      'x-client': "vw_user",
      'x-clientsession': "0123456789123456",
      'x-expire': "0",
      'authorization': "Basic dndfdXNlcjpMc1BxWThPbTJrY2U4MDI0OTMwNA==",
      'cache-control': "no-cache",
    }
    response = requests.request("POST", url, headers=headers, verify=False)

    jti_token = "No Token Yet"

    if response.status_code == 200:
        print "Logged in!"
        json_result = json.loads(response.text)
        jti_token = json_result['result']['jti']

        #print(response.text)
    elif response.status_code == 400:
        print "Bad Login Request"
    else:
        print "Not Authorised"

    return jti_token

#Get a list of vehicles
def get_vehicles():
    url = "https://bims-uat.bca.com/api/v1/vehicles"

    headers = {
        'authorization': g.jtiToken,
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers, verify = False)

    return(response.text)

#print a list of vehicles in a sale event
def get_event_vehicles(event_id):
    url = "https://bims-uat.bca.com/api/v1/saleevents/" + event_id + "/vehicles"

    headers = {
        'authorization': g.jtiToken,
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    #print(response.text)
    response_json2 = json.loads(response.text)
    if response.status_code == 200:
        for vehicle_ids in response_json2['result']:
            return vehicle_ids['regNo']
    else:
        return "No Vehicle Found in event: " + event_id



# Get a list of salesevents and print the vehicles in them
def get_salesevents():

    url = "https://bims-uat.bca.com/api/v1/saleevents"

    headers = {
        'authorization': g.jtiToken,
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

    response = requests.request("GET", url, headers=headers, verify = False)
    if response.status_code == 200:
        #print(response.text)
        response_json1 = json.loads(response.text)

        auctions = []

        for sale_ids in response_json1['result']:
            dicRow = {'id':sale_ids['id'], 'capacity': str(sale_ids['capacity']), 'regNo' : get_event_vehicles(sale_ids['id'])}
            auctions.insert(dicRow)
        return auctions
    else:
        return "No Sales Events / Error getting sales events"

