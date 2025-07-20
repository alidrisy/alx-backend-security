from django.shortcuts import render
from django.http import HttpResponse
from .models import RequestLog
from .geolocation import get_ip_geolocation, get_client_ip_from_request

# Create your views here.

def home(request):
    """Home view for the root route"""
    ip = get_client_ip_from_request(request)
    geo_data = get_ip_geolocation(ip)
    
    # Get recent request logs
    recent_logs = RequestLog.objects.order_by('-timestamp')[:10]
    
    # Create geolocation info HTML
    geo_info = ""
    if geo_data:
        geo_info = f"""
        <div class="geo-info">
            <h3>📍 Your Location</h3>
            <p><strong>IP Address:</strong> {ip}</p>
            <p><strong>Country:</strong> {geo_data.get('country', {}).get('name', 'Unknown')}</p>
            <p><strong>City:</strong> {geo_data.get('city', 'Unknown')}</p>
            <p><strong>Region:</strong> {geo_data.get('region', 'Unknown')}</p>
            <p><strong>Timezone:</strong> {geo_data.get('timezone', 'Unknown')}</p>
        </div>
        """
    else:
        geo_info = f"""
        <div class="geo-info">
            <h3>📍 Your Location</h3>
            <p><strong>IP Address:</strong> {ip}</p>
            <p><em>Geolocation data not available</em></p>
        </div>
        """
    
    # Create recent logs HTML
    logs_html = ""
    if recent_logs:
        logs_html = "<h3>📊 Recent Requests</h3><div class='logs'>"
        for log in recent_logs:
            logs_html += f"""
            <div class="log-entry">
                <span class="ip">{log.ip_address}</span>
                <span class="path">{log.path}</span>
                <span class="time">{log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</span>
                <span class="location">{log.country or 'Unknown'}, {log.city or 'Unknown'}</span>
            </div>
            """
        logs_html += "</div>"
    
    return HttpResponse(f"""
    <html>
    <head>
        <title>ALX Backend Security</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 20px;
            }}
            p {{
                color: #666;
                line-height: 1.6;
                text-align: center;
            }}
            .status {{
                background-color: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                text-align: center;
            }}
            .geo-info {{
                background-color: #e3f2fd;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #2196f3;
            }}
            .geo-info h3 {{
                margin-top: 0;
                color: #1976d2;
            }}
            .logs {{
                margin-top: 15px;
            }}
            .log-entry {{
                background-color: #f8f9fa;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border-left: 3px solid #28a745;
                display: grid;
                grid-template-columns: 1fr 2fr 1fr 1fr;
                gap: 10px;
                font-size: 14px;
            }}
            .log-entry .ip {{
                font-weight: bold;
                color: #495057;
            }}
            .log-entry .path {{
                color: #6c757d;
            }}
            .log-entry .time {{
                color: #6c757d;
                font-size: 12px;
            }}
            .log-entry .location {{
                color: #28a745;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 ALX Backend Security</h1>
            <div class="status">
                ✅ Application is running successfully with geolocation!
            </div>
            <p>Welcome to the ALX Backend Security project. This application now includes IP tracking and geolocation features.</p>
            
            {geo_info}
            
            {logs_html}
        </div>
    </body>
    </html>
    """)
