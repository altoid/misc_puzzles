#!/usr/bin/env python

from flask import Flask
from flask_restful import Api, Resource, reqparse
import config
import MySQLdb
import MySQLdb.cursors
from contextlib import closing
from pprint import pprint, pformat
import json

app = Flask(__name__)
api = Api(app)

def get_login_info(cursor, login):
    select_user = """
    select *
    from user
    where login = %s
    """
    cursor.execute(select_user, (login,))
    return cursor.fetchone()


class User(Resource):
    def get(self, login):
        try:
            with closing(MySQLdb.connect(user=config.mysql_user,
                                         passwd=config.mysql_passwd,
                                         host=config.mysql_host,
                                         db=config.mysql_db,
                                         cursorclass=MySQLdb.cursors.DictCursor)) as conn:
     
                cursor = conn.cursor()
    
                # check whether this login exists
                login_info = get_login_info(cursor, login)
                if login_info:
                    return login_info['json'], 200

                return "user %s not found" % login, 404
        except Exception as e:
            return login, 500

    def template(self):
        with closing(MySQLdb.connect(user=config.mysql_user,
                                     passwd=config.mysql_passwd,
                                     host=config.mysql_host,
                                     db=config.mysql_db,
                                     cursorclass=MySQLdb.cursors.DictCursor)) as conn:
     
            cursor = conn.cursor()
            try:
                return 'OK'
            except Exception as e:
                conn.rollback()
                return 'BAD', 500

    def put(self, login):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("login")
        parser.add_argument("json")
        args = parser.parse_args()

        with closing(MySQLdb.connect(user=config.mysql_user,
                                     passwd=config.mysql_passwd,
                                     host=config.mysql_host,
                                     db=config.mysql_db,
                                     cursorclass=MySQLdb.cursors.DictCursor)) as conn:
     
            cursor = conn.cursor()
            try:
    
                # check whether this login exists
                login_info = get_login_info(cursor, args.login)
                if login_info:
                    return_code = 200
                else:
                    return_code = 201
    
                insert_login = """
    insert into user
    (id, login, json)
    values (%(id)s, %(login)s, %(json)s)
    on duplicate key update
    json=values(json)
    """
                dml_args = {
                    'id': args.id,
                    'login': args.login,
                    'json': args.json,
                    }
    
                cursor.execute(insert_login, dml_args)
                conn.commit()
    
                return args.login, return_code
            except Exception as e:
                conn.rollback()
                return args.login, 500


class RepoBatch(Resource):
    """
    batch get/update operations on repos
    """

    def put(self, login):
        parser = reqparse.RequestParser()
        parser.add_argument("json")
        args = parser.parse_args()

        with closing(MySQLdb.connect(user=config.mysql_user,
                                     passwd=config.mysql_passwd,
                                     host=config.mysql_host,
                                     db=config.mysql_db,
                                     cursorclass=MySQLdb.cursors.DictCursor)) as conn:
     
            cursor = conn.cursor()
            try:
                # get the id for this login, 404 if not found
                # check whether this login exists

                login_info = get_login_info(cursor, login)
                if not login_info:
                    return "no such login:  %s" % login, 404
                
                login_id = login_info['id']

                # get all repo ids for this login
                select_repo_ids = """
select id
from repo
where owner_id = %s
"""
                cursor.execute(select_repo_ids, (login_id,))
                rows = cursor.fetchall()
                stored_repo_ids = { x['id'] for x in rows }

                # get the repo ids from the request
                repos_json = json.loads(args.json)
                request_repo_ids = { x['id'] for x in repos_json }

                # determine which repos were deleted upstream; delete them here.
                extras = stored_repo_ids - request_repo_ids
                if extras:

                    in_clause = ["%s"] * len(extras)
                    in_clause = ', '.join(in_clause)

                    delete_stmt = """
delete from repo
where id in (%(in_clause)s)
""" % {
                        'in_clause': in_clause
                        }
                    sql_args = list(extras)
                    cursor.execute(delete_stmt, sql_args)

                # INSERT ON DUPLICATE KEY UPDATE the rest.
                insert_repo = """
insert into repo
(owner_id, id, url, json)
values
(%(owner_id)s, %(id)s, %(url)s, %(json)s)
on duplicate key update
json=values(json)
"""

                # not sure if this could be done in one request given the size of the repo JSON
                for repo in repos_json:
                    dml_args = {
                        'owner_id': repo['owner']['id'],
                        'id': repo['id'],
                        'url': repo['html_url'],
                        'json': json.dumps(repo)
                        }
                    cursor.execute(insert_repo, dml_args)

                conn.commit()
            except Exception as e:
#                print e
                conn.rollback()
                return login, 500


api.add_resource(User, "/user/<string:login>")
api.add_resource(RepoBatch, "/user/<string:login>/repos")

app.run(debug=True)
