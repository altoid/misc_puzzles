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
    repos = json.loads(repo_response.text)
#    print repo_response.status_code

    print "%s repos" % len(repos)

    with closing(MySQLdb.connect(user=config.mysql_user,
                                 passwd=config.mysql_passwd,
                                 host=config.mysql_host,
                                 db=config.mysql_db,
                                 cursorclass=MySQLdb.cursors.DictCursor)) as conn:

        cursor = conn.cursor()

        insert_user = """
insert into user
(id, login, json)
values (%(id)s, %(login)s, %(json)s)
on duplicate key update
json=values(json)
"""
        dml_args = {
            'id': user_text_as_json['id'],
            'login': user_text_as_json['login'],
            'json': user_response.text
            }

        cursor.execute(insert_user, dml_args)

        insert_repo = """
insert into repo
(owner_id, id, url, json)
values
(%(owner_id)s, %(id)s, %(url)s, %(json)s)
on duplicate key update
json=values(json)
"""

        for repo in repos:
            dml_args = {
                'owner_id': repo['owner']['id'],
                'id': repo['id'],
                'url': repo['html_url'],
                'json': repo_response.text
                }
            cursor.execute(insert_repo, dml_args)

        conn.commit()
