'''
Database related operations
'''

import sqlite3
import argparse
import ConfigParser

# load config file
conf_parser = ConfigParser.ConfigParser()
conf_parser.read('config.ini')

db_filename = conf_parser.get('db', 'filename')

# init the db object
conn = sqlite3.connect(db_filename)


def initDB():
    '''
    Initialize the database file
    '''
    sql = """
    CREATE TABLE photos(
        album int,
        fn text,
        user text,
        ctime int
    )
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    print '* created table photos!'

    return 0


def insertSamples():
    '''
    Insert some sample data in photos
    '''
    sql = """
    INSERT INTO photos (album, fn, user, ctime)
    VALUES ('0', '2017-10-08-10-10-10.hehuan.jpg', 'hehuan', 1507475282549)
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    print '* inserted record into table photos!'

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="WeSee database operation basis")
    parser.add_argument("-f", "--func", help="the name of function to execute, including: init, sample")

    args = parser.parse_args()

    if args.func:
        if args.func == 'init':
            initDB()
        elif args.func == 'sample':
            insertSamples()
        else:
            pass
    else:
        pass
