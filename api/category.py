import json
import urllib2
from flask import Flask, jsonify, abort, request
from flask import Blueprint

from googleapiclient.discovery import build
from app import *

DEVELOPER_KEY = 'AIzaSyDrv7dBHAMN0lXxwQy-5784khjCb9X4wBs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

mod = Blueprint('videocategories',__name__)

@mod.route('/update', methods = ['GET'])
def update():
    try:
        response = video_categories_list()
        if response:
            truncated("c")
            items = response['items']
            for r in items:
                id = r['id']
                title = r['snippet']['title']
                addCategory(id, title)
        success = True
    except urllib2.HTTPError:
        success= False
    return jsonify(success=success)

def video_categories_list():
    # See full sample for function
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.videoCategories().list(
        part='snippet',
        regionCode='US'
    ).execute()
    return response

def addCategory(id,title):
    # open connect Database
    db = connectDb()

    # use method cursor()
    cursor = connectCursor(db)

    # sql insert database
    sql = """INSERT INTO category(Id,
                     CategoryName)
                     VALUES ('%(Id)s', '%(CategoryName)s')""" % \
          {'Id': id,
           'CategoryName': title,
           }
    #print sql
    try:
        # Thuc thi lenh SQL
        cursor.execute(sql)
        # Commit cac thay doi vao trong Database
        db.commit()
        success=True
    except:
        # Rollback trong tinh huong co bat ky error nao
        db.rollback()
        success = False

    # ngat ket noi voi server
    db.close()
    return success
