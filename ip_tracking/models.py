from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=50)
    timestamp = models.DateField(auto_now=True)
    path = models.CharField(max_length=250)