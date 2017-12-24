# coding: utf-8

import os
import codecs
import requests
from unittest import TestCase

SERVER = 'http://127.0.0.1'
video_id = "5Ai2wBynBtA"

class APITest(TestCase):
    def setUp(self):
        self.headers = {'Content-Type': 'application/json'}


    def test_get_subvideo_json(self):
        # given
        # when
        res = self.get_api_caption_video()
        self.save_srt(res.text, "sub.json")
        # then
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.text, basestring)

    def test_get_category_json(self):
        # given
        # when
        res = self.get_api_category()
        self.save_srt(res.text, "category.json")
        # then
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.text, basestring)


    def get_api_caption_video(self):
        """GET /api/test"""
        res = requests.get(
            '%s/caption/video?videoId=%s' % (SERVER, video_id)
        )
        return res


    def get_api_category(self):
        """GET /api/test"""
        res = requests.get(
            '%s/videocategories/' % SERVER
        )
        return res

    def save_srt(self, text, filename):
        """Save a list of srt formatted lines in a srt file with UTF-8 BOM"""
        with codecs.open(filename, 'w', 'utf-8-sig') as file:
            file.writelines(text)
