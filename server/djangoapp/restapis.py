import datetime

import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth

from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

    except:
        # If any error occurs
        print("Network exception occurred")


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'},
                                 params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        # If any error occurs
        print("Network exception occurred")


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"],
                                   full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_with_id(url, dealer_id, **kwargs):
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealer_id)
    if json_result:
        # For each dealer object
        dealer = json_result[0]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"],
                               full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], zip=dealer["zip"])
        return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # For each dealer object
        for dealer in json_result:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            if dealer["review"] is not None:
                sentiment = analyze_review_sentiments(dealer["review"])
            if dealer["purchase_date"] is not None:
                cr_date = dealer["purchase_date"]
                cr_date = datetime.datetime.strptime(cr_date, '%m/%d/%Y')
                year = cr_date.strftime("%Y")
            else:
                year = dealer["purchase_date"]
            dealer_obj = DealerReview(dealership=dealer["dealership"], name=dealer["name"],
                                      purchase=dealer["purchase"], review=dealer["review"],
                                      purchase_date=year, car_make=dealer["car_make"],
                                      car_model=dealer["car_model"], car_year=dealer["car_year"],
                                      sentiment=sentiment, id=dealer["id"])
            results.append(dealer_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/a540a9fb-cf24-4d67-8bdc-4ee56d69b29e/v1/analyze?version=2019-07-12'
    api_key = 'ZIqkGswVBIJLqvlV1SO3Ewl31QKZw_sIgDM_7YQvTZmJ'
    payload = {
        "text": text,
        "features": {
            "sentiment": {
            }
        }
    }
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'},
                             auth=HTTPBasicAuth('apikey', api_key))
    return json.loads(response.text)["sentiment"]["document"]["label"]
