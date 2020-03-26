from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Item, Auction, Bid
import datetime

class ItemSerializer(serializers.ModelSerializer):
    #validation to ensure code input is unique
    ItemCode =serializers.CharField(max_length=10,read_only=True,validators=[UniqueValidator(queryset=Item.objects.all(), message="ItemCode already exists")])
    
    class Meta:
        model = Item
        fields = ('ItemCode','Title','ItemCondition','Description', 'FirstRegDate')
        read_only_fields = ['ItemCode','FirstRegDate'] #both set to have automatically generated values
    
    def create(self, validated_data):
        newItem=Item.objects.create(**validated_data, FirstRegDate=datetime.datetime.now(),ItemCode="" )
        
        newItem.ItemCode='STK'+str(newItem.id) #update the itemcode to be STK+id
        newItem.save()
        
        return newItem


class AuctionSerializer(serializers.ModelSerializer):
    Item=ItemSerializer()

    class Meta:
        model = Auction
        fields = ('Item','CreatedByUsername','CreatedByUserID','Brief','StartDate','EndDate','MinimumPrice')
        read_only_fields = ['CreatedByUsername','CreatedByUserID'] 
        
    ##TO-DO (automatically detect createbyusername) 
    def create(self, validated_data):
        #extract the item data from the request
        newItemData=validated_data.pop('Item') 

        #create a new item using the data
        newItem=Item.objects.create(
        ItemCode="", #set itemcode to empty for now
        Title=newItemData['Title'],
        ItemCondition=newItemData['ItemCondition'],
        Description=newItemData['Description'],
        FirstRegDate=datetime.datetime.now()
        )
        
        newItem.ItemCode='STK'+str(newItem.id) #update the itemcode to be STK+id
        newItem.save()
        
        #create a new auction using the item, and requesting user
        auction=Auction.objects.create(Item=newItem,CreatedByUsername=self.context["request"].user.username,CreatedByUserID=self.context["request"].user,**validated_data)
        
        return auction
        #return Auction.objects.create(**validated_data, CreatedByUsername=)
        
       
class BidSerializer(serializers.ModelSerializer):
    #ItemCode =serializers.CharField(max_length=10,read_only=True,validators=[UniqueValidator(queryset=Item.objects.all(), message="ItemCode already exists")])
    
    class Meta:
        model = Bid
        fields = ('Auction','PlacedByUsername','PlacedDate','BidPrice')
        #read_only_fields = ['PlaceByUsername'] #both set to have automatically generated values
    
    def create(self, validated_data):
        ##validation here or in validators?
        return Bid.objects.create(**validated_data, PlacedDate=datetime.datetime.now())
 
 
  