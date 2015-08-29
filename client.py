#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import pycurl
import certifi
import json

try:
    # Python 3
    from io import BytesIO
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from StringIO import StringIO as BytesIO
    from urllib import urlencode


# global variables
CHARSET = 'utf-8'
CREDENTIAL = []
CREDENTIAL_SEPARATOR = ':'
USERNAME = "dummy_username"
PASSWORD = "dummy_password"
ACTION = "dummy_action"
TARGET = "dummy_target"
LIST_PER_PAGE = "200"


# usage info
def usage():
    print("usage: test.py <options>")
    print('''
    options:
        -h, --help      show this help message and exit
        -u, --username  indicate your GitHub username
        -p, --password  indicate your GitHub password
        -a, --action    indicate the action you want to do [star|following|watching]
        -t, --target    indicate the user who you want to reference

    ''')
    print("Report bugs to <mynameisny@126.com>.")


# valid client input & init params
def init_args():
    shortargs = 'u:p:a:t:h'
    longargs = ['username=', 'password=', 'action=', 'target=' "help"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
    except getopt.GetoptError:
        usage()
        sys.exit()

    if len(opts) == 0:
        usage()
        sys.exit()

    username = ""
    password = ""
    action = ""
    target = ""

    arg_u_exist = False
    arg_p_exist = False
    arg_a_exist = False
    arg_t_exist = False

    for arg, val in opts:
        if arg in ('-h', '--help'):
            usage()
            sys.exit()
        elif arg in ('-u', '--username'):
            arg_u_exist = True
            username = val
        elif arg in ('-p', '--password'):
            arg_p_exist = True
            password = val
        elif arg in ('-a', '--action'):
            arg_a_exist = True
            action = val
        elif arg in ('-t', '--target'):
            arg_t_exist = True
            target = val
        else:
            usage()
            sys.exit()
    return username, password, action, target, (arg_u_exist and arg_p_exist and arg_a_exist and arg_t_exist)


# common method: send a HTTP API invocation
def _send_https_request(method, url, credential, header=None, data=None):
    buffer_data = BytesIO()
    curl = pycurl.Curl()

    curl.setopt(pycurl.CUSTOMREQUEST, method.upper())
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.CAINFO, certifi.where())
    if header:
        curl.setopt(pycurl.HTTPHEADER, header)
    if data:
        curl.setopt(curl.POSTFIELDS, data)
    curl.setopt(pycurl.USERPWD, CREDENTIAL_SEPARATOR.join(credential))
    curl.setopt(pycurl.WRITEDATA, buffer_data)

    curl.perform()
    curl.close
    result = buffer_data.getvalue().decode(CHARSET)
    return result


# common method: send a HTTP GET API invocation
def _send_get_request(url, credential):
    return _send_https_request("GET", url, credential)


# common method: send a HTTP PUT API invocation
def _send_put_request(url, credential, data=None):
    if data:
        content_length = str(len(data))
    else:
        content_length = '0'
    return _send_https_request("PUT", url, credential, ['Content-Length: ' + content_length], data)


# common method: send a HTTP DELETE API invocation
def _send_delete_request(url, credential):
    return _send_https_request("DELETE", url, credential, ["Content-Length: 0"])


# get repositories list(dict) being starred by the user
def _get_starred_url_list(username):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i "https://api.github.com/users/networm/starred?page=1&per_page=2"
            or
        $ curl -i -u "mynameisny:xxxx" "https://api.github.com/user/starred?page=1&per_page=2"
    """
    api_result = _send_get_request('https://api.github.com/users/' + username + '/starred?page=1&per_page='
                                   + LIST_PER_PAGE, CREDENTIAL)
    result_list = []
    for item in json.loads(api_result):
        result_list.append(dict(owner=item['owner']['login'], name=item['name']))
    return result_list


# star a repository
def _star_repo(owner, repo):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i -u "mynameisny" -X PUT -H "Content-Length: 0" "https://api.github.com/user/starred/ningyu/demo"
    """
    api_result = _send_put_request('https://api.github.com/user/starred/' + owner + '/' + repo, CREDENTIAL)
    return api_result


# unstar a repository
def _unstar_repo(owner, repo):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i -u "mynameisny" -X DELETE -H "Content-Length: 0" "https://api.github.com/user/starred/ningyu/demo"
    """
    api_result = _send_delete_request('https://api.github.com/user/starred/' + owner + '/' + repo, CREDENTIAL)
    return api_result


# get users list(dict) being followed by the user
def _get_following_user_list(username):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i "https://api.github.com/users/mynameisny/following?page=1&per_page=2"
            or
        $ curl -i -u "mynameisny:xxxx" "https://api.github.com/users/mynameisny/following?page=1&per_page=2"
    """
    api_result = _send_get_request('https://api.github.com/users/' + username + '/following?page=1&per_page='
                                   + LIST_PER_PAGE, CREDENTIAL)
    result_list = []
    for item in json.loads(api_result):
        result_list.append(dict(id=item['id'], name=item['login']))
    return result_list


# follow a user
def _follow_user(username):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i -u "mynameisny" -X PUT -H "Content-Length: 0" "https://api.github.com/user/following/neo1218"
    """
    api_result = _send_put_request('https://api.github.com/user/following/' + username, CREDENTIAL)
    return api_result


# unfollow a user
def _unfollow_user(username):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i -u "mynameisny" -X DELETE -H "Content-Length: 0" "https://api.github.com/user/following/neo1218"
    """
    api_result = _send_delete_request('https://api.github.com/user/following/' + username, CREDENTIAL)
    return api_result


# get repositories list(dict) being watched by the user
def _get_watching_repo_list(username):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i "https://api.github.com/users/mynameisny/subscriptions?page=1&per_page=2"
            or
        $ curl -i -u "mynameisny:xxxx" "https://api.github.com/users/mynameisny/subscriptions?page=1&per_page=2"
    """
    api_result = _send_get_request('https://api.github.com/users/' + username + '/subscriptions?page=1&per_page='
                                   + LIST_PER_PAGE, CREDENTIAL)
    result_list = []
    for item in json.loads(api_result):
        result_list.append(dict(owner=item['owner']['login'], name=item['name']))
    return result_list


# watch a repository (Set a Repository Subscription)
def _watch_repo(owner, repo):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i -X PUT -H 'Context-Length:0'  '{"subscribed": "true"}' -u "mynameisny" "https://api.github.com/re
        pos/networm/FollowGitHubUser/subscription"
            or
        $ curl -i -X PUT -H "Context-Length:0" -d "{\"subscribed\": \"true\"}" -u "mynameisny" "https://api.github.com/
        repos/networm/FollowGitHubUser/subscription"

        TODO update basic put method: allow pass in a param
    """
    put_data = '{"subscribed": "true"}'
    api_result = _send_put_request('https://api.github.com/repos/' + owner + '/' + repo + '/subscription', CREDENTIAL,
                                   put_data)
    return api_result


# unwatch a repository (Delete a Repository Subscription)
def _unwatch_repo(owner, repo):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i -X DELETE -H "Context-Length: 0" -u "mynameisny:xxx" "https://api.github.com/repos/networm/FollowGitH
        ubUser/subscription"
    """
    api_result = _send_delete_request('https://api.github.com/repos/' + owner + '/' + repo + '/subscription',
                                      CREDENTIAL)
    return api_result


# star all old GitHub account's star-repo for the new one
def migrate_star_repo(target):
    for star_repo_entry in _get_starred_url_list(target):
        print("[Info]Begin to star " + star_repo_entry['owner'] + "'s repository: " + star_repo_entry['name'] + "...")
        _star_repo(star_repo_entry['owner'], star_repo_entry['name'])


# follow all old GitHub account's following-user for the new one
def migrate_following(target):
    for following_user_entry in _get_following_user_list(target):
        print("[Info]Begin to follow user: " + following_user_entry['name'] + "...")
        _follow_user(following_user_entry['name'])


# watch all old GitHub account's watching-repo for the new one
def migrate_watching(target):
    for watch_repo_entry in _get_watching_repo_list(target):
        print("[Info]Begin to watch " + watch_repo_entry['owner'] + "'s repository: " + watch_repo_entry['name'] + "...")
        _watch_repo(watch_repo_entry['owner'], watch_repo_entry['name'])


if __name__ == '__main__':
    USERNAME, PASSWORD, ACTION, TARGET, flag = init_args()
    CREDENTIAL.append(USERNAME)
    CREDENTIAL.append(PASSWORD)

    if flag:
        print("username=" + USERNAME + ", password=" + PASSWORD + ", action=" + ACTION + ", target=" + TARGET)
        if ACTION == 'star':
            migrate_star_repo(TARGET)
        elif ACTION == "following":
            migrate_following(TARGET)
        elif ACTION == "watching":
            migrate_watching(TARGET)
        else:
            usage()
            sys.exit()
    else:
        usage()
        sys.exit()
