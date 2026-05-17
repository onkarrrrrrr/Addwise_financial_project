import json
import os
import time
import urllib.parse
import urllib.request

from django.shortcuts import render

from .models import Appointment

_GOOGLE_REVIEWS_CACHE = {"expires": 0, "data": None}
_GOOGLE_REVIEWS_TTL_SECONDS = 60 * 60


def _build_reviews_payload(payload):
    result = payload.get("result", {})
    rating = float(result.get("rating") or 0)
    rating_int = max(0, min(5, int(round(rating))))
    reviews = []
    for review in result.get("reviews", []):
        text = review.get("text", "")
        preview = text if len(text) <= 160 else f"{text[:157]}..."
        author = review.get("author_name", "Anonymous")
        review_rating = int(review.get("rating") or 0)
        reviews.append(
            {
                "author_name": author,
                "initial": author[:1].upper() if author else "A",
                "profile_photo_url": review.get("profile_photo_url"),
                "time": review.get("relative_time_description", ""),
                "rating_int": max(0, min(5, review_rating)),
                "preview": preview,
            }
        )
    return {
        "name": result.get("name", "Addwise Financials"),
        "address": result.get("formatted_address", ""),
        "rating": rating,
        "rating_int": rating_int,
        "user_ratings_total": int(result.get("user_ratings_total") or 0),
        "reviews": reviews,
        "star_range": [1, 2, 3, 4, 5],
    }


def _get_google_reviews():
    now = time.time()
    cached = _GOOGLE_REVIEWS_CACHE.get("data")
    if cached and now < _GOOGLE_REVIEWS_CACHE.get("expires", 0):
        return cached

    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    place_id = os.getenv("GOOGLE_PLACE_ID")
    if not api_key or not place_id:
        return None

    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,reviews,formatted_address",
        "reviews_sort": "most_relevant",
        "key": api_key,
    }
    url = "https://maps.googleapis.com/maps/api/place/details/json?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=6) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

    if payload.get("status") != "OK":
        return None

    data = _build_reviews_payload(payload)
    _GOOGLE_REVIEWS_CACHE["data"] = data
    _GOOGLE_REVIEWS_CACHE["expires"] = now + _GOOGLE_REVIEWS_TTL_SECONDS
    return data


def _get_fallback_reviews():
    reviews = [
        {
            "author_name": "Harshad Deodhar",
            "initial": "H",
            "profile_photo_url": None,
            "time": "5 months ago",
            "rating_int": 5,
            "preview": "I had an excellent experience with this finance company. The team is knowledgeable, transparent, and very supportive throughout the process...",
        },
        {
            "author_name": "Digambar Deshpande",
            "initial": "D",
            "profile_photo_url": None,
            "time": "3 years ago",
            "rating_int": 5,
            "preview": "Got reference from friend, and still he helped me without any expectations. The 360 degree guidance was very helpful...",
        },
        {
            "author_name": "Deepak Pawar",
            "initial": "D",
            "profile_photo_url": None,
            "time": "5 years ago",
            "rating_int": 5,
            "preview": "Positive experience and clear guidance...",
        },
        {
            "author_name": "Nilesh Valand",
            "initial": "N",
            "profile_photo_url": None,
            "time": "6 months ago",
            "rating_int": 5,
            "preview": "We appreciate your support and trust...",
        },
        {
            "author_name": "Tanvi K",
            "initial": "T",
            "profile_photo_url": None,
            "time": "1 year ago",
            "rating_int": 5,
            "preview": "Thank you for your rating. If there is anything we can do to improve, please let us know...",
        },
    ]
    return {
        "name": "Addwise Financials",
        "address": "Ground Floor, Janaki Building, Bhandarkar Rd, near Kamala Nehru Park, opp. Bandhan Bank, Deccan Gymkhana, Pune, Maharashtra 411004, India",
        "rating": 5.0,
        "rating_int": 5,
        "user_ratings_total": 5,
        "reviews": reviews,
        "star_range": [1, 2, 3, 4, 5],
    }


def appointment(request):
    success = False
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        service = request.POST.get('service', '')
        message = request.POST.get('message', '')

        Appointment.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            service=service,
            message=message,
        )
        success = True

def home_view(request):
    reviews_data = _get_google_reviews() or _get_fallback_reviews()
    place_id = os.getenv("GOOGLE_PLACE_ID")
    review_url = (
        f"https://search.google.com/local/writereview?placeid={place_id}"
        if place_id
        else "https://www.google.com/maps"
    )
    reviews_data["review_url"] = review_url
    return render(request, 'leads/home.html', {"reviews_data": reviews_data})

def services_view(request):
    return render(request, 'leads/services.html')

def about_view(request):
    return render(request, 'leads/about.html')

    return render(request, 'leads/appointment.html', {'success': success})
