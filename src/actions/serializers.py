from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Item, Auction
import datetime

class ItemSerializer(serializers.ModelSerializer):
    #validation to ensure code input is unique
    ItemCode =serializers.CharField(max_length=10,validators=[UniqueValidator(queryset=Item.objects.all(), message="ItemCode already exists")])
    
    class Meta:
        model = Item
        fields = ('ItemCode','Title','Description')
    
    def create(self, validated_data):
        return Item.objects.create(**validated_data, FirstRegDate=datetime.datetime.now())


class AuctionSerializer(serializers.ModelSerializer):
    Item=ItemSerializer()

    class Meta:
        model = Auction
        fields = ('Item','ItemCondition','CreatedByUsername','Brief','StartDate','EndDate','MinimumPrice')
        
    ##TO-DO    
    ##def create(self, validated_data):
    ##    return Auction.objects.create(**validated_data, CreatedByUsername=)
  
  