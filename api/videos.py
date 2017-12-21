import json
import urllib2
from flask import Flask, jsonify, abort, request
from flask import Blueprint

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from app import *


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyDrv7dBHAMN0lXxwQy-5784khjCb9X4wBs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

mod = Blueprint('videos',__name__)

@mod.route('/add', methods = ['POST'])
def add():
    if not request.data:
        abort(400)
    jsoninput=json.loads(request.data)
    print request.data
    video_id = jsoninput["videoId"]

    try:
        videos_list_by_id(video_id)
        success = True
    except urllib2.HTTPError:
        success= False
    return jsonify(success=success)

def videos_list_by_id(videoId):

  # See full sample for function
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)
  response = youtube.videos().list(
    part='snippet',
    id=videoId
  ).execute()
  #print "%s" % (response)
  return response


def addVideo(video_id,categoryId,channelId,title,level):
    # open connect Database
    db = connectDb()

    # use method cursor()
    cursor = connectCursor(db)

    # sql insert database
    sql = """INSERT INTO video(Id,
                     CategoryId, ChannelId, Title, Level)
                     VALUES ('%(Id)s', '%(CategoryId)s', '%(ChannelId)s', '%(Title)s', %(Level)s)""" % \
          {'Id': video_id,
           'CategoryId': categoryId,
           'ChannelId': channelId,
           'Title': title,
           'Level': level,
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
