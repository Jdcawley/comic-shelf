# Base URL: https://comicvine.gamespot.com/api/

# Example search for a series:
# https://comicvine.gamespot.com/api/volume/?api_key=YOUR_KEY&filter=name:Batman&format=json

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://comicvine.gamespot.com/api/"
API_KEY = os.getenv("COMIC_VINE_API_KEY")

if not API_KEY:
        raise ValueError("API key not found. Please set COMIC_VINE_API_KEY in your environment variables.")

def _make_api_request(url, params):
    """Internal helper function to make Comic Vine API requests with error handling."""
    headers = {
        "User-Agent": "comic-shelf/1.0 (personal collection manager)"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def search_series(name):
    url = f"{BASE_URL}volumes/"
    params = {
        "api_key": API_KEY,
        "filter": f"name:{name}",
        "format": "json",
        "limit": 10  # Limit results to 10 for better performance
    }
    return _make_api_request(url, params)

def search_issue(comicvine_series_id, issue_number):
    url = f"{BASE_URL}issues/"
    params = {
        "api_key": API_KEY,
        "filter": f"volume:{comicvine_series_id},issue_number:{issue_number}",
        "format": "json"
    }
    return _make_api_request(url, params)