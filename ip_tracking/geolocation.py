import requests
import json
from typing import Dict, Optional

def get_ip_geolocation(ip_address: str) -> Optional[Dict]:
    """
    Get geolocation data for an IP address using a free service.
    Returns None if geolocation fails.
    """
    try:
        # Use ipapi.co - a free, reliable geolocation service
        url = f"https://ipapi.co/{ip_address}/json/"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "country": {
                    "name": data.get("country_name"),
                    "code": data.get("country_code")
                },
                "city": data.get("city"),
                "region": data.get("region"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone": data.get("timezone"),
                "org": data.get("org")
            }
        else:
            print(f"Geolocation API returned status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Geolocation request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse geolocation response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in geolocation: {e}")
        return None

def get_client_ip_from_request(request) -> str:
    """
    Extract client IP address from Django request object.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip 