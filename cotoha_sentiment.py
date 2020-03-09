# -*- coding:utf-8 -*-

import os
import urllib.request
import json
import configparser
import codecs
import csv


class CotohaApi:
    def __init__(self, client_id, client_secret, developer_api_base_url, access_token_publish_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.developer_api_base_url = developer_api_base_url
        self.access_token_publish_url = access_token_publish_url
        self.getAccessToken()

    def getAccessToken(self):
        url = self.access_token_publish_url
        headers={
            "Content-Type": "application/json;charset=UTF-8"
        }

        data = {
            "grantType": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        data = json.dumps(data).encode()
        req = urllib.request.Request(url, data, headers)
        res = urllib.request.urlopen(req)
        res_body = res.read()
        res_body = json.loads(res_body)
        self.access_token = res_body["access_token"]

    # 感情分析API
    def sentiment(self, sentence):
        url = self.developer_api_base_url + "nlp/v1/sentiment"
        headers={
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json;charset=UTF-8",
        }
        data = {
            "sentence": sentence
        }
        data = json.dumps(data).encode()
        req = urllib.request.Request(url, data, headers)
        try:
            res = urllib.request.urlopen(req)
        except urllib.request.HTTPError as e:
            print ("<Error> " + e.reason)

        res_body = res.read()
        res_body = json.loads(res_body)
        return res_body

if __name__ == '__main__':
    APP_ROOT = os.path.dirname(os.path.abspath( __file__)) + "/"

    # config.iniの値を取得

    CLIENT_ID = ''
    CLIENT_SECRET = ''
    DEVELOPER_API_BASE_URL = ''
    ACCESS_TOKEN_PUBLISH_URL = ''

    cotoha_api = CotohaApi(CLIENT_ID, CLIENT_SECRET, DEVELOPER_API_BASE_URL, ACCESS_TOKEN_PUBLISH_URL)

    # file/infile.txtから解析対象文取得
    checkpath = 'file/infile.txt'
    song_data = open(checkpath, "r", encoding='utf-8')

    output_file = open('file/output.csv', 'w')
    writer = csv.writer(output_file, lineterminator='\n') # 改行コード（\n）を指定しておく

    sentence = song_data.readline()
    while sentence:
        print(sentence.strip())
        # API実行
        result = cotoha_api.sentiment(sentence)

        score = result["result"]["score"]
        # from_word = result["result"]["emotional_phrase"][0]
        print(score)
        # print(from_word)
        sentiment = result["result"]["sentiment"]
        print(sentiment)

        one_row = [score,sentiment]
        writer.writerow(one_row)  # listを渡す

        sentence = song_data.readline()

    song_data.close()
    output_file.close()
    
