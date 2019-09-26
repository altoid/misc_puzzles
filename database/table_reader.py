#!/usr/bin/env python

# read a text file that looks like this
#
# +----+-------+--------+--------------+
# | Id | Name  | Salary | DepartmentId |
# +----+-------+--------+--------------+
# | 1  | Joe   | 85000  | 1            |
# | 2  | Henry | 80000  | 2            |
# | 3  | Sam   | 60000  | 2            |
# | 4  | Max   | 90000  | 1            |
# | 5  | Janet | 69000  | 1            |
# | 6  | Randy | 85000  | 1            |
# | 7  | Will  | 70000  | 1            |
# +----+-------+--------+--------------+
#
# and create a table in mysql with the data.  assumptions:
#
# columns named "id" will be PK
# columns with all numbers will be given int types
# all columns not null
# database named on command line
# if table already exists, drop and reinsert
# name of file is name of table.

import unittest
import argparse
from pprint import pprint
import MySQLdb
import MySQLdb.cursors
from datetime import datetime


def parse_line(line):
    line = line.strip()
    line = line.split('|')
    line = map(lambda x: x.strip(), line)
    return filter(lambda x: len(x) > 0, line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='name of the file containing table description')
    parser.add_argument('database',
                        help='mysql database where table is to be created')

    args = parser.parse_args()

    table_name = args.filename.split('.')[0]
    db_name = args.database

    with open(args.filename) as fd:
        fd.readline() # toss first line
        columns = fd.readline()
        columns = parse_line(columns)

        table_dict = {}
        for c in columns:
            table_dict[c] = []

        column_types = {}

        fd.readline() # toss line after column header

        data = fd.readline().strip()
        nrows = 0
        while data[0] != '+':
            data = parse_line(data)

            for z in zip(columns, data):
                table_dict[z[0]].append(z[1])

            data = fd.readline().strip()
            nrows += 1

        for c in columns:
            # try to cast column values with ints
            try:
                l = map(int, table_dict[c])
                column_types[c] = 'int'
                table_dict[c] = l
                continue
            except ValueError as e:
                pass

            # try to cast them as dates
            try:
                l = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), table_dict[c])

                column_types[c] = 'date'
                table_dict[c] = l
                continue
            except ValueError as e:
                pass

            # find the length of the longest string
            maxlength = len(max(table_dict[c], key=len))
            column_types[c] = 'varchar(%s)' % maxlength

    colspecs = map(lambda x: "%s %s not null" % (x, column_types[x]), columns)

    rows = []
    for i in xrange(nrows):
        row = []
        for c in columns:
            row.append(table_dict[c][i])
        rows.append(row)

    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='aoeu',
                           db=db_name)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    drop_table = """
    drop table if exists %s.%s
    """ % (db_name, table_name)
    cursor.execute(drop_table)

    create_table = """
    create table %s.%s
    (
    %s
    ) engine=innodb
    """ % (db_name, table_name, ',\n'.join(colspecs))

    cursor.execute(create_table)

    format_str = ['%s'] * len(columns)
    format_str = ', '.join(format_str)
    column_spec = ', '.join(columns)

    insert_stmt = """
    insert into %s (%s)
    values (%s)
    """ % (table_name, column_spec, format_str)

    cursor.executemany(insert_stmt, rows)
    conn.commit()

    print "done"


class MyTest(unittest.TestCase):

    def test_all_dates_good(self):
        candidates = ['2019-09-22', '2019-04-29']

        results = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), candidates)
        self.assertEqual(2, len(results))

    def test_no_dates_good(self):
        candidates = ['barf', 'whee']

        with self.assertRaises(ValueError) as context:
            results = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), candidates)

    def test_one_date_bad(self):
        candidates = ['barf', '2019-09-22', '2017-09-11']

        with self.assertRaises(ValueError) as context:
            results = map(lambda x: datetime.strptime(x, "%Y-%m-%d"), candidates)

    def test_longest(self):
        l = ['h', 'hh','hhh','hhhh']
        self.assertEqual(4, len(max(l, key=len)))
