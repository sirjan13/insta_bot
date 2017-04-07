import requests

import operator


APP_ACCESS_TOKEN = "482738385.a4c3737.f3781c605e8d4cebbc31ccd9095f5ed8"
'''My Access Token'''


BASE_URL = "https://api.instagram.com/v1"

#checks if the status code returned denoted success or not.It Returns a boolean depeding on success or failure
def check_success(status_code):
    if status_code == 200:
        return True
    return False

#collects the owner information
def owner_info():
    url = BASE_URL + "/users/self/?access_token=" + APP_ACCESS_TOKEN
    owner_data = requests.get(url).json()
    print "------------------Owner Info-------------------"
    print "Id : "+owner_data["data"]['id']
    print "Full Name : "+owner_data["data"]["full_name"]
    print "Username : "+owner_data["data"]["username"]
    bio = owner_data["data"]["bio"]
    if len(bio) == 0:
        bio = "User has not updated the Bio"
    print "Bio: " + bio
    print "------------------------------------------------" \

#Gets the user id for the passed username
def get_user_id_from_username(username):
    url = BASE_URL + "/users/search?q=" + username + "&access_token=" + APP_ACCESS_TOKEN  #For Eg:https://api.instagram.com/v1/users/search?q=jack&access_token=ACCESS-TOKEN
    user_data = requests.get(url).json()
    code = check_success(user_data["meta"]["code"])
    if code == True and len(user_data['data']):
        id = user_data['data'][0]['id']
        return id
    return " Sorry The requested User could not be Found "

def user_post_info(media_id):
    url = BASE_URL + "/media/" + media_id + "?access_token=" + APP_ACCESS_TOKEN
    data = requests.get(url).json()
    return data


def get_likes_count(media_id):
    data = user_post_info(media_id)
    return data['data']['likes']['count']


def get_comments_count(media_id):
    data = user_post_info(media_id)
    return data['data']['likes']['count']


'''to evaluate the criteria for interesting posts'''
def evaluate_criterion(username,criteria):
    id = get_recent_posts(username)
    b = {}
    d = {}
    for i in id:
        if criteria == "comments":
            a = get_comments_count(i)
        else:
            a = get_likes_count(i)
        b[i] = a
    b = sorted(b.items(), key=operator.itemgetter(1))
    d = sorted(d.items(), key=operator.itemgetter(1))
    return b[-1][0]



def get_recent_posts(username):
    user_id = get_user_id_from_username(username)
    url = BASE_URL + "/users/" + user_id + "/media/recent/?access_token=" + APP_ACCESS_TOKEN
    data = requests.get(url).json()
    id = []
    for i in range(len(data['data'])):
        id.append(data['data'][i]['id'])
    return id


#ranking users post on basis of likes or comments
username = raw_input("Enter the Username of the Person on whose Profile you want the bot to work on : ")
task_required = raw_input(("What do you wish to set ranking criteria for %s : \n 1.Likes \n 2.Comments \n")%(username) )
tasks = {"1": "likes", "2": "comments"}
#owner_info()
#print get_user_id_from_username(username)
print "id =", evaluate_criterion(username, tasks[task_required])
