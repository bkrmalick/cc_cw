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
    
    #override below method so that we can exclude users from viewing auctions created by themselves
    def get_queryset(self):
       Auction.updateStatusOfAllAuctions()
       return Auction.objects.all()
        
    def delete(self,request):  
        if(self.request.user.id==1): #if admin user
            Bid.objects.all().delete()
            Auction.objects.exclude(id=251).delete() #delete all auctions but the test
            Item.objects.exclude(id=278).delete()    #delete all items but the test
            User.objects.exclude(id=1).delete()      #delete all users but the admin
            return Response("All auctions, items and bids deleted.", status=status.HTTP_200_OK)
        else:
            return Response("Not Authorized", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
         
class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    
#class BidViewSetReadyOnly(viewsets.ReadOnlyModelViewSet):
 #   queryset = Bid.objects.all()
 #   serializer_class = BidSerializerWithoutAuctionID