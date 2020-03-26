from django.db import models
from django.contrib.auth.models import User

CONDITION_CHOICES = (
    ("poor","POOR"),
    ("good","GOOD"),
    ("new","NEW"),
)

class Item(models.Model):
    ItemCode=models.CharField(max_length=10)#, primary_key=True)
    Title=models.CharField(max_length=50)
    Description=models.CharField(max_length=200)
    ItemCondition=models.CharField(max_length=5, choices=CONDITION_CHOICES,default='good') 
    FirstRegDate=models.DateTimeField()
    
    def __str__(self):
        return self.Title+" ("+self.ItemCode+")"
        
class Bid(models.Model):
    Auction=models.ForeignKey('Auction',on_delete=models.PROTECT)
    PlacedByUsername=models.ForeignKey(User, on_delete=models.PROTECT)
    PlacedDate=models.DateTimeField()
    BidPrice=models.FloatField()
          
    def __str__(self):
        return "bid on AuctionID"+str(self.Auction.id)+" by "+str(self.PlacedByUsername)
    
class Auction(models.Model):
    #AuctionID - automatic
    Item=models.ForeignKey(Item, on_delete=models.PROTECT) #do not allow deletion of item before auction
    CreatedByUserID=models.ForeignKey(User, on_delete=models.PROTECT) 
    CreatedByUsername=models.CharField(max_length=200)
    Brief=models.TextField()
    StartDate=models.DateTimeField()
    EndDate=models.DateTimeField()
    MinimumPrice=models.FloatField()
    WinnerBid=models.ForeignKey(Bid, null=True,blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return "AuctionID " +str(self.id)
    
    

    

    
