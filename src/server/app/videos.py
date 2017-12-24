import json
from flask import jsonify, abort, request
from flask import Blueprint

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

from googleapiclient.discovery import build
from .db import *


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyDrv7dBHAMN0lXxwQy-5784khjCb9X4wBs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

mod = Blueprint('videos', __name__)


@mod.route('/add', methods=['POST'])
def add():
    if not request.data:
        abort(400)

    jsoninput = json.loads(request.data)
    print(request.data)

    try:
        video_id = jsoninput["videoId"]
        videos_list_by_id(video_id)
    except Exception:
        return jsonify(success=False)
    return jsonify(success=True)


@mod.route('/category', methods=['GET'])
def searchByCategoryId():
    text = request.args.get('categoryId', default='*', type=str)
    rows = getDataTable("video", "*", "WHERE CategoryId=%s" % text,"","","ORDER BY Id")
    data = [{
            'id': r[0],
            'categoryId': r[1],
            'channelId': r[2],
            'title': r[3],
            'level': r[4],
            } for r in rows]
    return jsonify(listVideo=data)


@mod.route('/delete-all', methods=['GET'])
def delete_all():
    try:
        truncated("video")
    except Exception as e:
        return jsonify(success=False)
    return jsonify(success=True)


@mod.route('/level', methods=['GET'])
def searchByLevel():
    text = request.args.get('level', default='*', type=str)
    rows = getDataTable("video", "*", "WHERE level=%s" % text, "", "", "ORDER BY Id")
    data = [{
            'id': r[0],
            'categoryId': r[1],
            'channelId': r[2],
            'title': r[3],
            'level': r[4],
            } for r in rows]
    return jsonify(listVideo=data)


@mod.route('/delete', methods=['GET'])
def delete_video():
    text = request.args.get('videoId', default='*', type=str)
    try:
        delete("video", "Id = '%s'" % text)
        delete("subtitle", "VideoId = '%s'" % text)
    except Exception as e:
        print (e)
        return jsonify(success=False)
    return jsonify(success=True)


def videos_list_by_id(videoId):

    # See full sample for function
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    response = youtube.videos().list(
        part='snippet',
        id=videoId
        ).execute()
    # print "%s" % (response)
    return response


def addVideo(video_id, categoryId, channelId, title, level):
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
    # print sql
    try:
        # Thuc thi lenh SQL
        cursor.execute(sql)
        # Commit cac thay doi vao trong Database
        db.commit()
    except Exception as e:
        print (e)
        # Rollback trong tinh huong co bat ky error nao
        db.rollback()
        return False
    finally:
        # ngat ket noi voi server
        db.close()
    return True
