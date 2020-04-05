from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Item, Auction, Bid
from django.utils import timezone


class ItemSerializer(serializers.ModelSerializer):
    #validation to ensure code input is unique
    ItemCode =serializers.CharField(max_length=10,read_only=True,validators=[UniqueValidator(queryset=Item.objects.all(), message="ItemCode already exists")])
    
    class Meta:
        model = Item
        fields = ('ItemCode','Title','ItemCondition','Description', 'FirstRegDate')
        read_only_fields = ['ItemCode','FirstRegDate'] #both set to have automatically generated values
    
    def create(self, validated_data):
        newItem=Item.objects.create(**validated_data, FirstRegDate=timezone.localtime(timezone.now()),ItemCode="" )
        
        newItem.ItemCode='STK'+str(newItem.id) #update the itemcode to be STK+id
        newItem.save()
        
        return newItem

       
class BidSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bid
        fields = ('Auction','PlacedByUserID','PlacedDate','BidPrice')
        read_only_fields = ['PlacedByUserID','PlacedDate'] #both set to have automatically generated values
    
    def create(self, validated_data):
        return Bid.objects.create(**validated_data, PlacedDate=timezone.localtime(timezone.now()),PlacedByUserID=self.context["request"].user )
 
    
    def validate_Auction(self, value):
    #https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
        if(value.CreatedByUserID.username==str(self.context["request"].user)):
            raise serializers.ValidationError("Cannot place bid on own auction")
        return value

    def validate(self, attrs):
        try:        
            if(attrs['BidPrice']==""):
                raise serializers.ValidationError("Bid Price cannot be null")
            elif(attrs['BidPrice']<attrs['Auction'].MinimumPrice):
                raise serializers.ValidationError("Bid Price needs to be greater than "+str(attrs['Auction'].MinimumPrice))
        except KeyError:
            raise serializers.ValidationError("Minimum Price cannot be null")
        
        
  

class AuctionSerializer(serializers.ModelSerializer):
    Item=ItemSerializer()
    CreatedByUsername=serializers.SerializerMethodField('get_CreatedByUsername') #computed field 

    class Meta:
        model = Auction
        fields = ('id','Item','Status','Brief','StartDate','EndDate','MinimumPrice','CreatedByUsername','WinnerBid')
        read_only_fields = ['CreatedByUsername','Status','WinnerBid'] 
         
    def create(self, validated_data):
        #extract the item data from the request
        newItemData=validated_data.pop('Item') 

        #create a new item using the data
        newItem=Item.objects.create(
            ItemCode="", #set itemcode to empty for now
            Title=newItemData['Title'],
            ItemCondition=newItemData['ItemCondition'],
            Description=newItemData['Description'],
            FirstRegDate=timezone.localtime(timezone.now())
        )
      
        #update the itemcode to be STK+id
        newItem.ItemCode='STK'+str(newItem.id) 
        newItem.save()
        
        #create a new auction using the item, and requesting user
        auction=Auction.objects.create(Item=newItem,Status="pending",CreatedByUserID=self.context["request"].user,**validated_data)
       
        #update status acc to dates
        Auction.updateStatusOfAuction(auction)
        
        return auction
        
    def get_CreatedByUsername(self, obj):
        return obj.CreatedByUserID.username 

    def validate(self, attrs):
        now =timezone.localtime(timezone.now())
        
        if(attrs['EndDate']<attrs['StartDate']):
            raise serializers.ValidationError("EndDate cannot be lesser than StartDate")
        if(attrs['StartDate']<now):
            raise serializers.ValidationError("StartDate cannot be in the past")
        try:        
            if(attrs['MinimumPrice']==""):
                raise serializers.ValidationError("Minimum Price cannot be null")
        except KeyError:
            raise serializers.ValidationError("Minimum Price cannot be null")
            
        return attrs
        
