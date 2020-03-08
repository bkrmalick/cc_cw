from django.shortcuts import render
from rest_framework import viewsets 
from .models import Item, Auction
from .serializers import ItemSerializer,AuctionSerializer 


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer