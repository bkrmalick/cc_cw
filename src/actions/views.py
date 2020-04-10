from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework import status
from rest_framework.response import Response
from .models import Item, Auction,Bid
from .serializers import ItemSerializer,AuctionSerializer,BidSerializer,BidSerializerWithoutAuctionID
from django.contrib.auth.models import User


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
   
class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    
    #override below method so that we can update statuses of all auctions before they are displayed
    def get_queryset(self):
       Auction.updateStatusOfAllAuctions()
       return Auction.objects.all()
        
    def delete(self,request):  
        if(self.request.user.id==1): #if admin user
            Bid.objects.all().delete()
            Auction.objects.exclude(id=267).delete() #delete all auctions but the test one
            Item.objects.exclude(id=294).delete()    #delete all items but the test one
            User.objects.exclude(id=1).delete()      #delete all users but the admin
            return Response("All auctions, items and bids deleted.", status=status.HTTP_200_OK)
        else:
            return Response("Not Authorized", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
         
class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    
