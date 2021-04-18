import requests
import os
import json

headers = ""

def main():
    global headers
    headers = create_headers()

    userids_url = get_userids_url()
    userids_response = connect_to_endpoint(userids_url, headers)
    # print(json.dumps(userids_response, indent=4, sort_keys=True))
    userids = get_userids(userids_response)
    # print(userids)

    following_dict = {}
    for userid in userids:
    	following_dict = add_following(userid, following_dict)

def add_following(userid, following_dict):
	following_url = get_following_url(userid)
	following_response = connect_to_endpoint(following_url, headers)
	followings = get_followings(following_response)

	# print(json.dumps(following_response, indent=4))
	return following_response

def get_followings(following_response):
    followings = {}
    for following in following_response["data"]:
    	

def get_following_url(userid):
    url = "https://api.twitter.com/2/users/{}/following?max_results=3&user.fields=public_metrics".format(userid)
    return url

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def create_headers():
    bearer_token = "---" //TODO
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def get_userids_url():
	usernames = "usernames=divijvaidya,__spd__"
	url = "https://api.twitter.com/2/users/by?{}".format(usernames)
	return url

def get_userids(userids_response):
	userids = set()

	for user in userids_response["data"]:
		userids.add(user["id"])

	return userids



if __name__ == "__main__":
    main()