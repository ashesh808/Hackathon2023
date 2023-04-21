import requests
import json

base_url = "https://developer.nrel.gov/"
response = requests.get(base_url + "api/solar/solar_resource/v1.json?api_key=DEMO_KEY&lat=40&lon=-105")


def get_request():
    if response.status_code == 200:
        jsonData = response.json()
        #print(jsonData)
        # Do something with the data
    else:
        print(f"Error: {response.status_code}")
    data = json.loads(json.dumps(jsonData))
    return data

data = get_request()

print("The average dni for latitude: " + data['inputs']['lat'] + " and longitude: " + data['inputs']['lon'] + " is " + str(data['outputs']['avg_dni']['annual']))
