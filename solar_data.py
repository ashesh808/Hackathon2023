import requests
import json

CACHE_FILE = "response_cache.json"
BASE_URL = "https://developer.nrel.gov/"

json_data = {}

def initialize():
    global json_data
    with open(CACHE_FILE, "r") as file:
        print("loading!")
        json_data = json.load(file)

def get_cached_response(url):
    #search file to try and find it
    if url in json_data:
        print("API CACHE: Found url in json cache! Url = ", url)
        return json_data[url]
    else:
        return None

def add_cached_response(url, response):
    if url in json_data:
        print("Error! Already found " + url + " in memory!")
    if response.status_code == 200:
        json_data[url] = response.json()
        with open(CACHE_FILE, "w") as file:
            #json.dump(json_data, file)
            w_data = json.dumps(json_data)
            file.write(w_data)

def get_data_from_zip(zip_code):
    request_url = BASE_URL + "api/solar/solar_resource/v1.json?api_key=DEMO_KEY&address=" + zip_code
    response = get_cached_response(request_url)
    if response == None:
        print("API CACHE: Given url not found in json cache! Sending get request. Url = ", request_url)
        response = requests.get(request_url)
        add_cached_response(request_url, response)
    if not isinstance(response, requests.Response) or response.status_code == 200:
        return response
    else:
        print(f"Error: {response.status_code}")
    #data = json.loads(json.dumps(jsonData))
    #return data

initialize()