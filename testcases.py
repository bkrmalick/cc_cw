import json, requests, datetime
###########################GLOBAL VARIABLES###########################

reg_url="http://193.61.36.131:8000/authentication/register/"
revoke_url="http://193.61.36.131:8000/authentication/token/revoke/"
token_url="http://193.61.36.131:8000/authentication/token/"

auctions_url="http://193.61.36.131:8000/actions/auction/"


create_user_flag=0 #to-do : api call here such that it resets and removes all tokens

olga={"username": "olga", "password": "olga123"}
nick={"username": "nick", "password": "nick123"}
mary={"username": "mary", "password": "mary123"}

print("############-TEST CASE 1-############")

if(create_user_flag==1):
    olga_response=requests.post(reg_url,data=olga).json()
    nick_response=requests.post(reg_url,data=nick).json()
    mary_response=requests.post(reg_url,data=mary).json()
    #olga_response=requests.post(revoke_url, data={"token":"iGeEjKoNUHhOIu1J4DF39yejIljE9G"}).json()

    print("\nOlga Response: ",olga_response)
    print("\nNick Response: ",nick_response)
    print("\nMary Response: ",mary_response)

print("############-TEST CASE 2-############")

olga_response=requests.post(token_url,data=olga).json()
nick_response=requests.post(token_url,data=nick).json()
mary_response=requests.post(token_url,data=mary).json()


print("\nOlga Response:",olga_response)
print("\nNick Response:",nick_response)
print("\nMary Response:",mary_response)

olga_token=str(olga_response['access_token'])
nick_token=str(nick_response['access_token'])
mary_token=str(mary_response['access_token'])


print("\n############-TEST CASE 3-############")

olga_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+""}).json()
print("Olga request without token:\n "+str(olga_response))

olga_response=requests.get(auctions_url, headers= {'Authorization':'Bearer '+olga_token})

print("Olga request with token:\n "+json.dumps(olga_response.json(), indent=2))

print("\n############-TEST CASE 4-############")

olga_auction={
    "Item": {
        "Title": "Olga's Shirt",
        "ItemCondition": "good",
        "Description": "D&C shirt, hasn't been worn in years"
    },
    #"CreatedByUsername": 1,
    "Brief": "Serious buyers only",
    "StartDate": str(datetime.datetime.now()),
    "EndDate": str(datetime.datetime(2020, 3, 27, 23, 35, 14, 496045)),
    "MinimumPrice": 20
}


olga_response=requests.post(auctions_url,json=olga_auction, headers={'Content-type': 'application/json','Authorization':'Bearer '+olga_token})

print(olga_response.text)
print(olga_response.request.body)
