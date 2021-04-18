import requests
import os
import json
import sys

# has auth info
api_call_header = ""

def main():
    global api_call_header

    if (len(sys.argv) < 2):
        raise Exception("Missing bearer_token as command line arg")
    bearer_token = sys.argv[1]
    api_call_header = create_headers(bearer_token)

    userids_url = get_userids_url()
    userids_response = connect_to_endpoint(userids_url)
    userids = get_userids(userids_response)

    to_follow_dict = {}
    for userid in userids:
    	to_follow_dict = add_following(userid, to_follow_dict)

    print(json.dumps(to_follow_dict, indent=4, sort_keys=True))

def add_following(userid, to_follow_dict):
	"""
		following shape:
		{<username> : { 
				userid : <id>,
				followers_count : <integer value>,
				frequency : <integer value> -- how fequent is this user as a following for given users
			}
		}
	"""

	following_url = get_following_url(userid)

	# TODO implement support for multi-page
	following_response = connect_to_endpoint(following_url)
	
	for following in following_response["data"]:
		username = following['username']
		userid = following['id']
		followers_count = following['public_metrics']['followers_count']
		frequency = 1
		if username in to_follow_dict:
			frequency = frequency + to_follow_dict[username]['frequency']
		to_follow_dict[username] = {'userid' : userid, 'followers_count' : followers_count, 'frequency' : frequency}

	return to_follow_dict

def get_following_url(userid):
    url = "https://api.twitter.com/2/users/{}/following?max_results=3&user.fields=public_metrics".format(userid)
    return url

def connect_to_endpoint(url):
    global api_call_header
    response = requests.request("GET", url, headers=api_call_header)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def get_userids_url():
	# TODO take this from cmd line
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