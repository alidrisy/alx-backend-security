from .models import RequestLog, BlockedIP
from .geolocation import get_ip_geolocation, get_client_ip_from_request
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = get_client_ip_from_request(request)

        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        country = None
        city = None

        # Get geolocation data using our custom service
        try:
            geo_data = get_ip_geolocation(ip)
            if geo_data:
                country = geo_data.get("country", {}).get("name")
                city = geo_data.get("city")
                print(f"Geolocation data for {ip}: Country={country}, City={city}")
            else:
                print(f"No geolocation data available for {ip}")
        except Exception as e:
            print(f"Error getting geolocation for {ip}: {e}")

        # Create the request log entry
        try:
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=country,
                city=city,
            )
        except Exception as e:
            # Log the error but don't break the request
            print(f"Error logging request: {e}")

        return self.get_response(request)

    def get_client_ip(self, request):
        return get_client_ip_from_request(request)
