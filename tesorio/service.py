#!/usr/bin/env python

from flask import Flask
from flask_restful import Api, Resource, reqparse
import config
import MySQLdb
import MySQLdb.cursors
from contextlib import closing
from pprint import pprint
import json

app = Flask(__name__)
api = Api(app)

class User(Resource):
    def get(self, name):
        try:
            with closing(MySQLdb.connect(user=config.mysql_user,
                                         passwd=config.mysql_passwd,
                                         host=config.mysql_host,
                                         db=config.mysql_db,
                                         cursorclass=MySQLdb.cursors.DictCursor)) as conn:
     
                cursor = conn.cursor()
    
                # check whether this login exists
                select_user = """
    select *
    from user
    where login = %s
    """
                cursor.execute(select_user, (name,))
                rows = cursor.fetchone()
                if rows:
                    return rows['json'], 200

                return "user %s not found" % name, 400
        except Exception as e:
            return name, 500

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("login")
        parser.add_argument("json")
        args = parser.parse_args()

        try:
            with closing(MySQLdb.connect(user=config.mysql_user,
                                         passwd=config.mysql_passwd,
                                         host=config.mysql_host,
                                         db=config.mysql_db,
                                         cursorclass=MySQLdb.cursors.DictCursor)) as conn:
     
                cursor = conn.cursor()
    
                # check whether this login exists
                select_user = """
    select login
    from user
    where login = %s
    """
                cursor.execute(select_user, (args.login,))
                rows = cursor.fetchone()
                if rows:
                    return_code = 200
                else:
                    return_code = 201
    
                insert_user = """
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
    
                cursor.execute(insert_user, dml_args)
                conn.commit()
    
                return args.login, return_code
        except Exception as e:
            return args.login, 500

api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
