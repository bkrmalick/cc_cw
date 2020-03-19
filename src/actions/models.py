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
    Description=models.CharField(max_length=200)
    FirstRegDate=models.DateTimeField()
    
    def __str__(self):
        return self.ItemCode+" ("+self.Title+")"
    
class Auction(models.Model):
    #AuctionID - automatic
    Item=models.ForeignKey(Item, on_delete=models.PROTECT) #do not allow deletion of item before auction
    ItemCondition=models.CharField(max_length=5, choices=CONDITION_CHOICES,default='good')
    CreatedByUsername=models.ForeignKey(User, on_delete=models.PROTECT) 
    Brief=models.TextField()
    StartDate=models.DateTimeField()
    EndDate=models.DateTimeField()
    MinimumPrice=models.FloatField()
