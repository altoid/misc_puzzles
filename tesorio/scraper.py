#!/usr/bin/env python

import sys
import requests
import config
import json
import MySQLdb
import MySQLdb.cursors
import argparse
from contextlib import closing

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--user',
                        help='login name of user to scrape')

    args = parser.parse_args()

    headers={'Authorization': 'token %s' % config.token,
             'Accept': 'application/vnd.github.v3+json',
             }

    if args.user:
        user_url = 'https://api.github.com/users/%s' % args.user
        repo_url = 'https://api.github.com/users/%s/repos' % args.user
    else:
        user_url = 'https://api.github.com/user'
        repo_url = 'https://api.github.com/user/repos'

    user_response = requests.get(user_url, headers=headers)

    if user_response.status_code == 404:
        print 'no such user:  %s' % args.user
        sys.exit(1)

#    print user_response.status_code
    user_text_as_json = json.loads(user_response.text)

    repo_response = requests.get(repo_url, headers=headers)

    if repo_response.status_code != 200:
        print 'aw dang:  %s' % repo_response.status_code
        sys.exit(1)

    dml_args = {
            'id': user_text_as_json['id'],
            'login': user_text_as_json['login'],
            'json': user_response.text
            }

    put_response = requests.put("%s/user/%s" % (config.serviceurl, user_text_as_json['login']),
                                data=dml_args)

    dml_args = {
            'json': repo_response.text
            }

    put_response = requests.put("%s/user/%s/repos" % (config.serviceurl, user_text_as_json['login']),
                                data=dml_args)


    
