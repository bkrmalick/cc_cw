from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django.utils import timezone


CONDITION_CHOICES = (
    ("poor","POOR"),
    ("good","GOOD"),
    ("new","NEW"),
)

AUCTION_STATUSES = (
    ("pending","PENDING"),        #awaiting start date
    ("live","LIVE"),              #open to offers
    ("completed","COMPLETED"),    
    ("cancelled","CANCELLED"),    
)

class Item(models.Model):
    ItemCode=models.CharField(max_length=10)
    Title=models.CharField(max_length=50)
    Description=models.CharField(max_length=200)
    ItemCondition=models.CharField(max_length=5, choices=CONDITION_CHOICES,default='good') 
    FirstRegDate=models.DateTimeField()
    
    def __str__(self):
        return self.Title+" ("+self.ItemCode+")"
        
class Bid(models.Model):
    Auction=models.ForeignKey('Auction',on_delete=models.PROTECT)
    PlacedByUserID=models.ForeignKey(User, on_delete=models.PROTECT)
    PlacedDate=models.DateTimeField()
    BidPrice=MoneyField(decimal_places=2,default=0,default_currency='GBP',max_digits=10,)
          
    def __str__(self):
        return "bid on "+str(self.Auction)+" by "+str(self.PlacedByUserID.username)
    
class Auction(models.Model):
    Item=models.ForeignKey(Item, on_delete=models.PROTECT) #do not allow deletion of item before auction
    CreatedByUserID=models.ForeignKey(User, on_delete=models.PROTECT) 
    Brief=models.TextField(blank=True)
    StartDate=models.DateTimeField()
    EndDate=models.DateTimeField()
    MinimumPrice=MoneyField(decimal_places=2,default=0,default_currency='GBP',max_digits=10, blank=False)
    Status=models.CharField(max_length=10, choices=AUCTION_STATUSES,default='default') 
    WinnerBid=models.ForeignKey(Bid, null=True,default=None, on_delete=models.SET_NULL, blank=True) #on_delete set null, otherwise unable to delete auction as Auction and Bid table have cyclic dependency/foreign keys
    
    def __str__(self):
        return "AuctionID " +str(self.id)
    
    #update statuses of all auctions acc. to StartDate and EndDate
    def updateStatusOfAllAuctions():
        auctions=Auction.objects.all()
        
        for i in range(len(auctions)):
            Auction.updateStatusOfAuction(auctions[i])
            auctions[i].save()
    
    #update status of a single auction acc. to StartDate and EndDate
    def updateStatusOfAuction(auction):
        now=timezone.localtime(timezone.now())
        
        if(auction.StartDate<=now and now<auction.EndDate):
            auction.Status="LIVE"
        elif(auction.EndDate<=now):
            auction.Status="COMPLETED"
            auction.WinnerBid=Auction.getWinningBid(auction)
        else:
            auction.Status="PENDING"
    
    #get the winning bid for a particular auction
    def getWinningBid(auction):
        if( len(Bid.objects.filter(Auction=auction))>0):
            return Bid.objects.filter(Auction=auction).order_by('-BidPrice')[0] #max price bid
        else:
            return None
            
            
        
            
    
