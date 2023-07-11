from django.db import models
from api.constants import STATES, ROLES
# Create your models here.
class Shipment(models.Model):
    
    user_id = models.IntegerField()
    state  = models.CharField(max_length=1, choices=STATES)
    created = models.DateTimeField(auto_now_add=True)

class Message(models.Model):    
    role    = models.CharField(max_length=1, choices=ROLES)
    message = models.TextField()
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)