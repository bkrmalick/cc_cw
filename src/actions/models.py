from django.db import models
from django.contrib.auth.models import User

CONDITION_CHOICES = (
    ("poor","POOR"),
    ("good","GOOD"),
    ("new","NEW"),

)
class Item(models.Model):
    ItemCode=models.CharField(max_length=10, primary_key=True)
    Title=models.CharField(max_length=50)
    Condition=models.CharField(max_length=5, choices=CONDITION_CHOICES,default='good')
    Description=models.CharField(max_length=200)
    
class Auction(models.Model):
    ItemCode=models.ForeignKey(Item, on_delete=models.PROTECT) #do not allow deletion of item before auction
    CreatedByUsername=models.ForeignKey(User, on_delete=models.PROTECT) 
    StartDate=models.DateTimeField()
    EndDate=models.DateTimeField()
    MinimumPrice=models.FloatField()