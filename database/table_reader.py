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
# if table already exists, abort the whole thing - don't bother to insert the data.
# name of file is name of table.

import unittest
import argparse
from pprint import pprint
import MySQLdb
import MySQLdb.cursors

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
    print table_name

    with open(args.filename) as fd:
        fd.readline() # toss first line
        columns = fd.readline()
        columns = parse_line(columns)

        table_dict = {}
        for c in columns:
            table_dict[c] = []

        column_types = {k:'varchar(64)' for k in columns}

        fd.readline() # toss line after column header

        data = fd.readline().strip()
        nrows = 0
        while data[0] != '+':
            data = parse_line(data)

            for z in zip(columns, data):
                table_dict[z[0]].append(z[1])

            data = fd.readline().strip()
            nrows += 1

        # try to cast column values with ints
        for c in columns:
            try:
                l = map(int, table_dict[c])
                column_types[c] = 'int'
                table_dict[c] = l
            except ValueError as e:
                pass

    colspecs = map(lambda x: "%s %s not null" % (x, column_types[x]), columns)

    create_table = """
    create table %s.%s
    (
    %s
    ) engine=innodb
    """ % (db_name, table_name, ',\n'.join(colspecs))

    print create_table

    rows = []
    for i in xrange(nrows):
        row = []
        for c in columns:
            row.append(table_dict[c][i])
        rows.append(row)

    pprint(rows)

    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='aoeu',
                           db=db_name)
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

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



