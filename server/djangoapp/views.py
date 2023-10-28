from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_with_id, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return redirect('/djangoapp/')
    else:
        return render(request, 'djangoapp/index.html')


def logout_request(request):
    logout(request)
    return render(request, 'djangoapp/index.html')


def registration_request(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        user = User.objects.create_user(username, username+'@gmail.com', password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return render(request, 'djangoapp/index.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://prodlist.18x7z2eezce9.us-south.codeengine.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', {"data": dealerships})


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://prodlist.18x7z2eezce9.us-south.codeengine.appdomain.cloud/api/get_reviews"
        # Get dealers from the URL
        dealershipReviews = get_dealer_reviews_from_cf(url, dealer_id)
        dealer = get_dealer_with_id(
            "https://prodlist.18x7z2eezce9.us-south.codeengine.appdomain.cloud/api/dealership", dealer_id)
        return render(request, 'djangoapp/dealer_details.html', {"data": dealershipReviews, "dealer": dealer})


def add_review(request, dealer_id):
    if request.method == "GET":
        url = "https://prodlist.18x7z2eezce9.us-south.codeengine.appdomain.cloud/api/get_reviews"
        data = get_dealer_reviews_from_cf(url, dealer_id)
        return render(request, 'djangoapp/add_review.html', {"cars": data, "dealer_id": dealer_id})
    elif request.method == "POST":
        url = "https://prodlist.18x7z2eezce9.us-south.codeengine.appdomain.cloud/api/get_reviews"
        data = get_dealer_reviews_from_cf(url, dealer_id)
        dealership = dealer_id
        review = request.POST.get("review", "")
        purchase = request.POST.get("purchase", "")
        purchase_date = request.POST.get("purchase_date", "")
        car = request.POST.get("car", "").split("-")
        body = {
            'id': len(data)+1,
            'name': 'test',
            'dealership': dealership,
            'review': review,
            'purchase': purchase,
            'purchase_date': purchase_date.utcnow().isoformat(),
            'car_make': car[0],
            'car_model': car[1],
            'car_year': car[2]
        }
        url_post = "https://prodlist.18x7z2eezce9.us-south.codeengine.appdomain.cloud/api/post_review"
        post_request(url_post, body)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        #return render(request, 'djangoapp/add_review.html')

