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
except ImportError:
    # Python 2
    from StringIO import StringIO as BytesIO


# global variables
CHARSET = 'utf-8'
CREDENTIAL = []
CREDENTIAL_SEPARATOR = ':'
USERNAME = "dummy_username"
PASSWORD = "dummy_password"
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
        -t, --target    indicate the user who you want to reference
    ''')


# valid client input & init params
def init_args():
    shortargs = 'u:p:t:h'
    longargs = ['username=', 'password=', 'target=' "help"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)
    except getopt.GetoptError:
        usage()
        sys.exit()

    if len(opts) == 0:
        usage()
        sys.exit()

    arg_u_exist = False
    arg_p_exist = False
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
        elif arg in ('-t', '--target'):
            arg_t_exist = True
            target = val
        else:
            usage()
            sys.exit()
    return username, password, target, (arg_u_exist and arg_p_exist and arg_t_exist)


# common method: send a HTTP API invocation
def _send_https_request(method, url, credential, header=None):
    buffer = BytesIO()
    curl = pycurl.Curl()

    curl.setopt(pycurl.CUSTOMREQUEST, method.upper())
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.CAINFO, certifi.where())
    if header:
        curl.setopt(pycurl.HTTPHEADER, header)
    curl.setopt(pycurl.USERPWD, CREDENTIAL_SEPARATOR.join(credential))
    curl.setopt(pycurl.WRITEDATA, buffer)

    curl.perform()
    curl.close
    result = buffer.getvalue().decode(CHARSET)
    return result


# common method: send a HTTP GET API invocation
def _send_get_request(url, credential):
    return _send_https_request("GET", url, credential)


# common method: send a HTTP PUT API invocation
def _send_put_request(url, credential):
    return _send_https_request("PUT", url, credential, ["Content-Length: 0"])


# get starred url dict
def _get_starred_url_list(username):
    """
        you can execute the command like below in your terminal for test(not include prompt symbol '$'):
        $ curl -i https://api.github.com/users/networm/starred?page=1&per_page=2
        or
        $ curl -i -u "mynameisny:xxxx" https://api.github.com/user/starred?page=1&per_page=2
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
        $ curl -i -u "mynameisny" -X PUT -d "Content-Length: 0" https://api.github.com/user/starred/ketoo/NoahGameFrame
    """
    api_result = _send_put_request('https://api.github.com/user/starred/' + owner + '/' + repo, CREDENTIAL)
    return api_result


# star all old GitHub account's star-repo for the new one
def migrate_star_repo(target):
    for star_repo_entry in _get_starred_url_list(target):
        print("[Info]Begin to star " + star_repo_entry['owner'] + "'s repository: " + star_repo_entry['name'] + "...")
        _star_repo(star_repo_entry['owner'], star_repo_entry['name'])


if __name__ == '__main__':
    USERNAME, PASSWORD, TARGET, flag = init_args()
    CREDENTIAL.append(USERNAME)
    CREDENTIAL.append(PASSWORD)

    if flag:
        print("username=" + USERNAME + ", password=" + PASSWORD + ", target=" + TARGET)
        migrate_star_repo(TARGET)
    else:
        usage()
        sys.exit()
