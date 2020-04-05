from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework import status
from rest_framework.response import Response
from .models import Item, Auction,Bid
from .serializers import ItemSerializer,AuctionSerializer,BidSerializer,BidSerializerWithoutAuctionID


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
            Auction.objects.all().delete()
            Item.objects.all().delete()
            return Response("All auctions, items and bids deleted.", status=status.HTTP_200_OK)
        else:
            return Response("Not Authorized", status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
         
class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    
class BidViewSetReadyOnly(viewsets.ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializerWithoutAuctionID