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
    print_header("owner")
    print_info_basic(owner_data)
    print_footer("owner")


#Gets the user id for the passed username
def get_user_id_from_username(username):
    url = BASE_URL + "/users/search?q=" + username + "&access_token=" + APP_ACCESS_TOKEN  #For Eg:https://api.instagram.com/v1/users/search?q=jack&access_token=ACCESS-TOKEN
    user_data = requests.get(url).json()
    code = check_success(user_data["meta"]["code"])
    if code and len(user_data['data']):
        id = user_data['data'][0]['id']
        return id
    return False  #for nasty errors


def user_post_info(media_id):
    url = BASE_URL + "/media/" + media_id + "?access_token=" + APP_ACCESS_TOKEN
    data = requests.get(url).json()
    code = check_success(data["meta"]["code"])
    if code:
        return data
    return False


def no_of_user_posts(username):
    return len(get_recent_posts(username))


def user_post(username, criteria):
    no_of_posts = no_of_user_posts(username)
    if no_of_posts:
        media_id = evaluate_criterion(username, criteria)
        if media_id:
            data = user_post_info(media_id)
            if data:
                no_of_likes = get_likes_count(media_id)
                no_of_comments = get_comments_count(media_id)
                link = data['data']['link']
                print_header("post")
                print "Username                            : " + username
                print "Link                                : " + link
                print "Number of Likes                     : " + str(no_of_likes)
                print "Number of Comments                  : " + str(no_of_comments)
                print_footer("post")
    else:
        print "The user has no Posts"


def print_header(role):
    if role == "user":
        heading = "User Info"
        x = 70
    elif role == "owner":
        heading = "Owner Info"
        x = 70
    else:
        heading = "Post Info"
        x = 50

    header_right = ""
    for i in range(x):
        header_right += '-'
    header_left = header_right
    print header_left + heading + header_right


def print_footer(role):
    if role in ["owner", "user"]:
        y = 140
    else:
        y = 100
    y += len(role + " info")

    footer = ""
    for i in range(y):
        footer += '-'
    print footer


def get_user_details(username):
    user_id = get_user_id_from_username(username)
    if user_id:
        url = BASE_URL + "/users/" + str(user_id) + "/?access_token=" + APP_ACCESS_TOKEN
        data = requests.get(url).json()
        print_header("user")
        print_info_basic(data)
        print_footer("user")


def print_info_basic(data):
    print "Id                                   : " + data['data']['id']
    print "Full Name                            : " + data["data"]["full_name"]
    print "Username                             : " + data["data"]["username"]
    print "Profile Picture                      : " + data['data']['profile_picture']
    bio = data["data"]["bio"]
    if len(bio) == 0:
        bio = "User has not updated the Bio"
    print "Bio                                  : " + bio
    website = data["data"]['website']
    if len(website) == 0:
        website = "User has not updated the Website Link"
    print "Website                              : " + website
    posts = data['data']['counts']['media']
    if posts == 0:
        posts = "No Posts Yet"
    print "No of Posts                          : " + str(posts)
    print "People Followed By                   : " + str(data['data']['counts']["followed_by"])
    print "People Following                     : " + str(data['data']['counts']["follows"])


def get_likes_count(media_id):
    data = user_post_info(media_id)
    if data:
        return data['data']['likes']['count']
    return False


def get_comments_count(media_id):
    data = user_post_info(media_id)
    if data:
        return data['data']['comments']['count']
    return False


def get_recent_posts(username):
    user_id = get_user_id_from_username(username)
    if user_id:
        url = BASE_URL + "/users/" + user_id + "/media/recent/?access_token=" + APP_ACCESS_TOKEN
        data = requests.get(url).json()
        id = []
        for i in range(len(data['data'])):
            id.append(data['data'][i]['id'])
        return id
    return False


#To evaluate the criteria for interesting posts
def evaluate_criterion(username, criteria):
    id = get_recent_posts(username)
    if id:
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
    return False


def like_user_post(username, criterion ) :
    media_id = evaluate_criterion(username, criterion)
    if media_id:
        url = BASE_URL + "/media/" + media_id + "/likes"
        requests_data = {"access_token": APP_ACCESS_TOKEN}
        like_request = requests.post(url, requests_data).json()
        message = check_success(like_request['meta']['code'])
        if message:
            return "Successfully Liked the Post "
        else:
            return "Sorry could not Like the Post..Try again Later "
    return False


def comment_user_post(username, criteria):
    media_id = evaluate_criterion(username, criteria)
    if media_id:
        url = BASE_URL + "/media/" + media_id + "/comments"
        comment_text = ask_user_comment()
        requests_data = {"access_token": APP_ACCESS_TOKEN, 'text': comment_text}
        comment_request = requests.post(url, requests_data).json()
        message = check_success(comment_request['meta']['code'])
        if message:
            return "Successfully commented on the Post "
        else:
            return "Sorry could not Comment on the Post..Try again Later "
    return False


def fetch_post_comments(media_id):
    url = BASE_URL + "/media/" + media_id + "/comments?access_token=" + APP_ACCESS_TOKEN
    data = requests.get(url).json()
    code = check_success(data['meta']['code'])
    data = data['data']
    if code:
        return data
    return False


#  search word input by user
def comment_word_search(word):
    media_id = evaluate_criterion(username, criteria)
    if media_id:
        data = fetch_post_comments(media_id)

        for i in range(len(data)):
            a = data[i]['text']
            comment_by = data[i]['from']['full_name']

            b = a.strip()
            if word in b:
                my_list = [data[i]['id'], a, comment_by]
                return my_list
        return False
    return False


# delete comment on successful word search
def delete_comment_on_search(word):
    comment_data = comment_word_search(word)
    if comment_data:
        comment_id = comment_data[0]
        if comment_id:
            media_id = evaluate_criterion(username, criteria)
            url = BASE_URL + "/media/" + media_id + "/comments/" + comment_id + "?access_token=" +APP_ACCESS_TOKEN
            data = requests.delete(url).json()
            comment = comment_data[1]
            comment_by = comment_data[2]
            success = check_success(data['meta']['code'])
            if success:
                success_message = "\n\n\nComment Deleted Successfully."
                message_text = "\n\nDeleting Comment : " + comment + "\n     By: " + comment_by + success_message
                return message_text
            else:
                error = "\n\n\n Sorry,I am not authorised to Delete this as its done by some other user"
                message_text = "\n\nDeleting Comment : " + comment + "\n     By: " + comment_by +  error
                return message_text
        return "No Comment contains the word %s " % word
    return "No Comment contains the word %s " % word


# display average words per comment on most popular post
def comments_average_words():
    media_id = evaluate_criterion(username, criteria)
    if media_id:
        total_comments = get_comments_count(media_id)
        data = fetch_post_comments(media_id)
        no_of_words = 0
        for i in range(len(data)):
            comment = data[i]['text']
            no_of_words += len(comment.split())
        no_of_words = float(no_of_words)
        average_words_per_comment = no_of_words / total_comments
        average_words_per_comment = round(average_words_per_comment, 2)
        return average_words_per_comment
    return False


# Asks the word to search in comments from the user.
def ask_word():
    return raw_input("Enter the word you want to search for :- ")


#  Asks user what comment to make
def ask_user_comment():
    comment = raw_input("\nWhat comment do you want to make :- ")
    return comment


#  Ranking users post on basis of likes or comments.
def ask_criteria():
    tasks = {"1": "likes", "2": "comments"}
    choice = raw_input(("What criteria do you wish to set for ranking posts for %s (hight-->low) : \n 1.Likes \n 2.Comments \n") % (username))
    if choice in ['1', '2']:
        return tasks[choice]
    else:
        print "Sorry I guess that was a wrong Input :(  "
        ask_criteria()


# function to take username from user
def ask_username():
    user_name = raw_input("Enter the Username of the Person on whose Profile you want the bot to work on : ")
    valid_user = get_user_id_from_username(user_name)
    if valid_user:
        return user_name
    return False


# print the values returned by the functions called
def print_response_text(parameter):
    if parameter:
        print parameter
    else:
        print " A Error Occoured!! "


# driver function to take user choice
def ask_user_input():
    task_input = raw_input("What do you wish to do : \n "
                               "1.Get Owner Details \n "
                               "2.Get User's User Id  \n "
                               "3.Get User's Details  \n "
                               "4.Get User's Most interesting Post Details \n "
                               "5.Like a Post \n "
                               "6.Comment on a Post \n "
                               "7.Delete a comment having a particular word \n "
                               "8.Display the average words per comment in a Post \n ----> ")

    if task_input in [str(x) for x in range(1, 9)]:
        return task_input
    else:
        print "Sorry I guess that was a wrong Input :(  "
        ask_user_input()

ch = "y"
while ch == "y":

    task_required = ask_user_input()

    if task_required == "1":
        owner_info()
    else:
        username = ask_username()
        if username:

            if task_required == "2":
                user_id = get_user_id_from_username(username)

                if user_id:
                    print "Id = ", user_id
                else:
                    print " The User could not be Found "

            elif task_required == "3":
                get_user_details(username)

            else:
                if no_of_user_posts(username):
                    criteria = ask_criteria()

                    if task_required == "4":
                        user_post(username, criteria)

                    else:
                        if task_required == "5":
                            response_text = like_user_post(username, criteria)
                        elif task_required == "6":
                            response_text = comment_user_post(username, criteria)
                        elif task_required == "7":
                            word = ask_word()
                            response_text = delete_comment_on_search(word)
                        else:
                            response_text = comments_average_words()
                            if response_text:
                                response_text = "The average word count per comment = " + str(response_text)
                        print_response_text(response_text)
                else:
                    print "----No Posts Found!----"

        else:
            print "I don't recognise this username in my current Mode"
    ch = raw_input("Do You want to make another Request to the Bot? (y/n) :- ")
    ch = ch.lower()
