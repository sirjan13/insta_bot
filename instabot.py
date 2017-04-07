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

def like_user_post(username, criterion ) :
    media_id = evaluate_criterion(username, criterion)
    url = BASE_URL + "/media/" + media_id + "/likes"
    requests_data = {"access_token": APP_ACCESS_TOKEN}
    like_request = requests.post(url, requests_data).json()
    #print like_request
    message = check_success(like_request['meta']['code'])
    if message:
        print "Sucessfully Liked the Post "
    else:
        print "Sorry a Error occoured..Try again Later "


def comment_user_post(username, criteria):
    media_id = evaluate_criterion(username, criteria)
    url = BASE_URL + "/media/" + media_id + "/comments"
    requests_data = {"access_token": APP_ACCESS_TOKEN, 'text': "hi bot hun mein "}
    comment_request = requests.post(url, requests_data).json()
    message = check_success(comment_request['meta']['code'])
    if message:
        print "Sucessfully commented on the Post "
    else:
        print "Sorry a Error occoured..Try again Later "


#ranking users post on basis of likes or comments
def ask_criteria():
    criteria = raw_input(("What criteria do you wish to set for ranking posts for %s : \n 1.Likes \n 2.Comments \n") % (username))
    tasks = {"1": "likes", "2": "comments"}
    return tasks[criteria]



username = raw_input("Enter the Username of the Person on whose Profile you want the bot to work on : ")
task_required = raw_input(("What do you wish to do for %s : \n 1.Likes \n 2.Comments \n")%(username) )

criteria = ask_criteria()

if task_required == "1":
    like_user_post(username, criteria)
else:
    comment_user_post(username, criteria)

#owner_info()
#print get_user_id_from_username(username)
