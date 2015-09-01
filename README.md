

# Overview
this is a simple tool the follow GitHub user's starred, following, watching and clean all them by determined a account.
When you switch to a new account, you can use it to sync your old data of the past.

----------


# Prerequisite
I write and debug these code on Windows7 x64 with Python v3.4.3. There is only one python file in my project. All imported libs are: 
<pre>
import sys
import getopt
import json
import pycurl
import certifi
</pre>

Maybe the lib pycurl & cerifi not install on you computer, so you need install them first by 
<pre>pip install pycurl-7.19.5.1-cp34-none-win_amd64.whl </pre> and <pre>pip install certifi-2015.4.28-py2.py3-none-any.whl</pre> 

In the lib directory you can find these two files. If you encounter errors, search a appropriate edtion for your platform. If still does not work, email me or google it and retry.

----------

# Usage
`python client.py <options>`
usage: test.py <options>

    options:
        -h, --help      show this help message and exit
        -u, --username  indicate your GitHub username
        -p, --password  indicate your GitHub password
        -a, --action    indicate the action you want to do [star|following|watching|clean]
        -t, --target    indicate the user who you want to reference


In the case of default, param value "watching" will watch a repo and notificatio
ns should be received from this repo. If you want block notifications from this
repo, you can set the action to "watching-withoutnotify". The param value "watch
ing" is equivalent to "watching-withnofity".


----------

# TODO
1. ~~Batch follow GitHub user's watching and following.~~
2. Support OAuth2 autenticate.
3. ~~Clean old user's star repo(unstar).~~

----------

# Links
My friend write a robust & fully supported edition, it is really easy to use, you can get his repository via the link below. And I would like to thank him for his always support    **:)**

**FollowGitHubUser:**   
[https://github.com/networm/FollowGitHubUser](https://github.com/networm/FollowGitHubUser "networm/FollowGitHubUser")