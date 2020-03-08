from rest_framework import serializers
from .models import Item, Auction


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('ItemCode','Title','Condition','Description')
        
        

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('ItemCode','CreatedByUsername','StartDate','EndDate','MinimumPrice')