from flask import Flask
import MySQLdb


def connectDb():
    db = MySQLdb.connect(host='127.0.0.1'
                         , user='root'
                         , passwd=''
                         , db='howtospeak'
                         , charset='utf8'
                         , use_unicode=True)
    return db
def connectCursor(db):

    cursor = db.cursor()
    return cursor

app = Flask(__name__)
