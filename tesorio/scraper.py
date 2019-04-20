#!/usr/bin/env python

import sys
import requests
import config
import json
import MySQLdb
import MySQLdb.cursors
import argparse
from contextlib import closing

# def update_repos():
# 
#     # get all the repos we know about from the database.  delete any from the database that do not appear
#     # in the return result from the repo call.
# 
#     repos = json.loads(repo_response.text)
# 
#     select_repo = """
# select id
# from repo
# where owner_id = %(owner_id)s
# """
#     select_args = {
#         'owner_id': 
#     insert_repo = """
# insert into repo
# (owner_id, id, url, json)
# values
# (%(owner_id)s, %(id)s, %(url)s, %(json)s)
# on duplicate key update
# json=values(json)
# """
# 
#     for repo in repos:
#         dml_args = {
#             'owner_id': repo['owner']['id'],
#             'id': repo['id'],
#             'url': repo['html_url'],
#             'json': repo_response.text
#             }
#         cursor.execute(insert_repo, dml_args)
# 
#     print "%s repos" % len(repos)


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
    repos = json.loads(repo_response.text)
    # print repo_response.status_code

    dml_args = {
            'id': user_text_as_json['id'],
            'login': user_text_as_json['login'],
            'json': user_response.text
            }

    put_response = requests.put("%s/user/%s" (config.serviceurl, %user_text_as_json['login']),
                                data = dml_args)


