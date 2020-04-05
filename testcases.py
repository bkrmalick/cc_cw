import json, requests, datetime
###########################GLOBAL VARIABLES###########################

reg_url="http://193.61.36.131:8000/authentication/register/"
revoke_url="http://193.61.36.131:8000/authentication/token/revoke/"
token_url="http://193.61.36.131:8000/authentication/token/"

auctions_url="http://193.61.36.131:8000/actions/auction/"

olga={"username": "olga", "password": "olga123"}
nick={"username": "nick", "password": "nick123"}
mary={"username": "mary", "password": "mary123"}
admin={"username": "bkr", "password": "bkr"}
###########################HELPER FUNCTIONS############################

def prettyResponse(resp):
    return (json.dumps(resp.json(), indent=2))

def resetApplication(): #deletes all auctions, access tokens, users
    #get new token for admin user
    token=requests.post(token_url,data=admin).json()["access_token"]

    #delete all auctions, items, and bids (only works with admin token) 
    requests.delete(auctions_url,headers= {'Authorization':'Bearer '+token})   
 
    #delete all users and their tokens
    #todo

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
    "StartDate": str(datetime.datetime.now()),                          #todays date
    "EndDate": str(datetime.datetime.now()+datetime.timedelta(days=1)), #todays date +1 day
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
    "StartDate": str(datetime.datetime.now()),                          #todays date
    "EndDate": str(datetime.datetime.now()+datetime.timedelta(days=1)), #todays date +1 day
    "MinimumPrice": 40
}


mary_response=requests.post(auctions_url,json=mary_auction, headers={'Content-type': 'application/json','Authorization':'Bearer '+mary_token})

print("\nResponse of Mary adding new auction: ")
print(prettyResponse(mary_response))

print("\n############-TEST CASE 7-############")

olga_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+olga_token})

print("\nOLGA BROWSING AUCTIONS: ")
print(prettyResponse(olga_response))

nick_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+nick_token})

print("\nNICK BROWSING AUCTIONS: ")
print(prettyResponse(nick_response))
