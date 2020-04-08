import json, requests, datetime, time
###########################GLOBAL VARIABLES###########################

reg_url="http://193.61.36.131:8000/authentication/register/"
revoke_url="http://193.61.36.131:8000/authentication/token/revoke/"
token_url="http://193.61.36.131:8000/authentication/token/"

auctions_url="http://193.61.36.131:8000/actions/auction/"
bid_url="http://193.61.36.131:8000/actions/bid/"

olga={"username": "olga", "password": "olga123"}
nick={"username": "nick", "password": "nick123"}
mary={"username": "mary", "password": "mary123"}
admin={"username": "bkr", "password": "bkr"}

MARY_AUCTION_DURATION_IN_SECONDS=5
###########################HELPER FUNCTIONS############################

def prettyResponse(resp):
    return str(resp)+"\n"+ str(json.dumps(resp.json(), indent=2))

def resetApplication(): #deletes all auctions, access tokens, users
    print("\nTrying to reset API data for demo...")
    #get new token for admin user
    token=requests.post(token_url,data=admin).json()["access_token"]

    #delete all auctions, items, and bids (only works with admin token) 
    resp=requests.delete(auctions_url,headers= {'Authorization':'Bearer '+token})
    
    print(resp)
    print(resp.reason+"\n")

    if(resp.ok):
        print("Successfully deleted previous data!\n")
    else:
        print("Error, check details above \n")

###########################PRE-TEST ACTIONS############################

resetApplication()

###########################TEST CASES###################################

print("############-TEST CASE 1-############")

olga_response=requests.post(reg_url,data=olga)
nick_response=requests.post(reg_url,data=nick)
mary_response=requests.post(reg_url,data=mary)

print("\nOlga Response: ",prettyResponse(olga_response))
print("\nNick Response: ",prettyResponse(nick_response))
print("\nMary Response: ",prettyResponse(mary_response))

print("\n############-TEST CASE 2-############")

olga_response=requests.post(token_url,data=olga)
nick_response=requests.post(token_url,data=nick)
mary_response=requests.post(token_url,data=mary)

print("\nOlga Response: ",prettyResponse(olga_response))
print("\nNick Response: ",prettyResponse(nick_response))
print("\nMary Response: ",prettyResponse(mary_response))

olga_token=str(olga_response.json()['access_token'])
nick_token=str(nick_response.json()['access_token'])
mary_token=str(mary_response.json()['access_token'])


print("\n############-TEST CASE 3-############")

olga_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+""})
print("\nResponse of Olga request without token:\n "+prettyResponse(olga_response))

olga_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+olga_token})

print("\nResponse of Olga request with token:\n "+prettyResponse(olga_response))

print("\n############-TEST CASE 4-############")

##OLGA AUCTIONING HER ITEM
olga_auction={
    "Item": {
        "Title": "Olga's Shirt",
        "ItemCondition": "good",
        "Description": "D&C shirt, hasn't been worn in years"
    },
    "Brief": "Serious buyers only",
    "StartDate": str(datetime.datetime.now()),                          #todays date
    "EndDate": str(datetime.datetime.now()+datetime.timedelta(days=1)), #todays date +1 day
    "MinimumPrice": 20
}


olga_response=requests.post(auctions_url,json=olga_auction, headers={'Content-type': 'application/json','Authorization':'Bearer '+olga_token})

print("\nResponse of Olga adding new auction: ")
print(prettyResponse(olga_response))

print("\n############-TEST CASE 5-############")

##NICK AUCTIONING HIS ITEM
nick_auction={
    "Item": {
        "Title": "Xbox 360 Controller",
        "ItemCondition": "poor",
        "Description": "left joystick doesn't work, salvageable for other parts"
    },
    "Brief": "Buyer must be willing to pick up item from Croydon",
    "StartDate": str(datetime.datetime.now()+datetime.timedelta(days=1)),#todays date +1 days
    "EndDate": str(datetime.datetime.now()+datetime.timedelta(days=2)),  #todays date +2 day
    "MinimumPrice": 30
}


nick_response=requests.post(auctions_url,json=nick_auction, headers={'Content-type': 'application/json','Authorization':'Bearer '+nick_token})

print("\nResponse of Nick adding new auction: ")
print(prettyResponse(nick_response))

print("\n############-TEST CASE 6-############")

##MARY AUCTIONING HER ITEM
mary_auction={
    "Item": {
        "Title": "Bedside Lamp",
        "ItemCondition": "good",
        "Description": "Cara Glass Touch Lamps, Set of 2 - connects to WiFi and controllable with phone"
    },
    "Brief": "",
    "StartDate": str(datetime.datetime.now()),                             #todays date
    "EndDate": str(datetime.datetime.now()+datetime.timedelta(seconds=MARY_AUCTION_DURATION_IN_SECONDS)), #will end seconds after starting
    "MinimumPrice": 40
}


mary_response=requests.post(auctions_url,json=mary_auction, headers={'Content-type': 'application/json','Authorization':'Bearer '+mary_token})

print("\nResponse of Mary adding new auction: ")
print(prettyResponse(mary_response))

print("\n############-TEST CASE 7 & 8-############")

olga_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+olga_token})

print("\nOLGA BROWSING AUCTIONS: ")
print(prettyResponse(olga_response))

nick_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+nick_token})

print("\nNICK BROWSING AUCTIONS: ")
print(prettyResponse(nick_response))

print("\n############-TEST CASE 9-############")

for i in nick_response.json(): #can be either one of three peoples response as they all will contain marys auction
	if(i["CreatedByUsername"]=="mary"):
		marys_auction=i

mary_bid={
    "Auction": marys_auction["id"],
    "BidPrice": 29.87
}

mary_response=requests.post(bid_url,json=mary_bid, headers={'Content-type': 'application/json','Authorization':'Bearer '+mary_token})

print("\nResponse of Mary bidding on her own auction: "+prettyResponse(mary_response))


print("\n############-TEST CASE 10-############")

#Olga's bid on marys item
olga_bid={
    "Auction": marys_auction["id"],
    "BidPrice": 45
}

olga_response=requests.post(bid_url,json=olga_bid, headers={'Content-type': 'application/json','Authorization':'Bearer '+olga_token})

print("\nResponse of Olga bidding on Mary's auction: "+prettyResponse(olga_response))


#Nick's bid on marys item
nick_bid={
    "Auction": marys_auction["id"],
    "BidPrice": 60
}

nick_response=requests.post(bid_url,json=nick_bid, headers={'Content-type': 'application/json','Authorization':'Bearer '+nick_token})

print("\nResponse of Nick bidding on Mary's auction: "+prettyResponse(nick_response))

print("\n############-TEST CASE 11-############")

print("Waiting for Mary's auction to finish...")

for i in range(MARY_AUCTION_DURATION_IN_SECONDS):
    time.sleep(i+1)
    print("Time Passed: "+str(i+1)+" seconds")

nick_response=requests.get(auctions_url+str(marys_auction["id"])+"/", headers= {'Authorization':'Bearer '+nick_token})
print("\nResponse of Nick GET-ting Mary's auction to see if he's won: ")
print(prettyResponse(nick_response))

print("\n############-TEST CASE 12-############")

olga_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+olga_token})

print("\nOLGA BROWSING all the items sold: ")
print(olga_response)
for i in olga_response.json(): 
	if(i["Status"]=="COMPLETED"):
		print(json.dumps(i["Item"], indent=2))

print("\n############-TEST CASE 13-############")

mary_response=requests.get(bid_url, headers= {'Authorization':'Bearer '+mary_token})

print("\nMary querying for all bids on her auction: ")
print(mary_response)
for i in mary_response.json(): 
	if(i["Auction"]==marys_auction["id"]):
		print(json.dumps(i, indent=2))

