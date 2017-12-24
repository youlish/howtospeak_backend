
from flask import jsonify
from flask import Blueprint

from googleapiclient.discovery import build
from .db import *

DEVELOPER_KEY = 'AIzaSyDrv7dBHAMN0lXxwQy-5784khjCb9X4wBs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

mod = Blueprint('videocategories', __name__)


@mod.route('/update', methods=['GET'])
def update():
    try:
        response = video_categories_list()
        if response:
            truncated("c")
            items = response['items']
            for r in items:
                addCategory(r['id'], r['snippet']['title'])
    except Exception as e:
        return jsonify(success=False)
    return jsonify(success=True)

@mod.route('/', methods=['GET'])
def get_list_category():
    try:
        rows = getDataTable("category", "*", "", "", "", "ORDER BY Id")
        data = [{
                    'id': r[0],
                    'categoryName': r[1]
                } for r in rows]
    except Exception as e:
        return jsonify(listVideo=[])
    return jsonify(listVideo=data)


def video_categories_list():
    # See full sample for function
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    response = youtube.videoCategories().list(
        part='snippet',
        regionCode='US'
    ).execute()
    return response


def addCategory(cid, title):
    # open connect Database
    db = connectDb()

    # use method cursor()
    cursor = connectCursor(db)

    # sql insert database
    sql = """INSERT INTO category(Id, CategoryName)
                VALUES ('%(Id)s', '%(CategoryName)s')""" % {
                    'Id': cid,
                    'CategoryName': title}
    # print sql
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print (e)
        db.rollback()
        return False
    finally:
        db.close()
    return True
