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
    print "------------------------------------------------"


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
    return data['data']['comments']['count']


#To evaluate the criteria for interesting posts
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
    comment_text = ask_user_comment()
    requests_data = {"access_token": APP_ACCESS_TOKEN, 'text': comment_text}
    comment_request = requests.post(url, requests_data).json()
    message = check_success(comment_request['meta']['code'])
    if message:
        print "Sucessfully commented on the Post "
    else:
        print "Sorry a Error occoured..Try again Later "


def fetch_post_comments(media_id):
    url = BASE_URL + "/media/" + media_id + "/comments?access_token=" + APP_ACCESS_TOKEN
    data = requests.get(url).json()
    data = data['data']
    return data


def ask_user_comment():
    comment = raw_input("\nWhat comment do you want to make :- ")
    return comment


def comment_word_search(word):
    media_id = evaluate_criterion(username, criteria)
    data = fetch_post_comments(media_id)
    for i in range(len(data)):
        a = data[i]['text']
        b = a.strip()
        if word in b:
            return data[i]['id']
    return False


def delete_comment_on_search(word):
    comment_id = comment_word_search(word)
    if comment_id:
        media_id = evaluate_criterion(username, criteria)
        url = BASE_URL + "/media/" + media_id + "/comments/" + comment_id + "?access_token=" +APP_ACCESS_TOKEN
        data = requests.delete(url).json()
        success = check_success(data['meta']['code'])
        if success:
            print "Comment Delted Sucessfully. "
        else:
            print "I can't Delete this "
    else:
        print "No Comment contains the word %s " %word


def comments_average_words():
    media_id = evaluate_criterion(username, criteria)
    total_comments = get_comments_count(media_id)
    data = fetch_post_comments(media_id)
    no_of_words = 0
    for i in range(len(data)):
        comment = data[i]['text']
        no_of_words += len(comment.split())
    no_of_words = float(no_of_words)
    average_words_per_comment = no_of_words / total_comments
    return average_words_per_comment


#Asks the word to search in comments from the user.
def ask_word():
    return raw_input("Enter the word you want to search for :- ")


#Ranking users post on basis of likes or comments.
def ask_criteria():
    choice = raw_input(("What criteria do you wish to set for ranking posts for %s : \n 1.Likes \n 2.Comments \n") % (username))
    tasks = {"1": "likes", "2": "comments"}
    return tasks[choice]


def ask_username():
    user_name = raw_input("Enter the Username of the Person on whose Profile you want the bot to work on : ")
    return user_name


task_required = raw_input("What do you wish to do : \n "
                           "1.Get Owner Details \n "
                           "2.Get User's User Id  \n "
                           "3.Like a Post \n "
                           "4.Comment on a Post \n "
                           "5.Delete a comment having a particular word \n "
                           "6.Display the average words per comment in a Post \n ----> ")


if task_required == "1":
    owner_info()
else:
    username = ask_username()
    if task_required == "2":
        print get_user_id_from_username(username)
    else:
        criteria = ask_criteria()
        if task_required == "3":
            like_user_post(username, criteria)
        elif task_required == "4":
            comment_user_post(username, criteria)
        elif task_required == "5":
            word = ask_word()
            delete_comment_on_search(word)
        else:
            print comments_average_words()

