# encoding: utf-8

import re
import time
import json
import requests
import traceback
from config import memc
from waclib.core import app

def check_fb(openid, token):
    url = "https://graph.facebook.com/v2.1/me?access_token=%s&fields=id,name&format=json&method=get&pretty=0&suppress_http_code=1" %(token)
    try:
        resp = requests.get(url, timeout = 5)
        if resp.status_code != 200:
            return False

        od = json.loads(resp.text)
        if od and (od.get("id").lower() == openid):
            return True
    except Exception, e:
        traceback.print_exc()
    return False

def send_requests(url):
    try:
        resp = requests.get(url.encode('utf-8'))
        if resp.status_code == 200:
            return resp, True
    except Exception, e:
        traceback.print_exc()
    return None, False

def format_response(text):
    items = text.split("&")
    m = {}
    for item in items:
        key, value = item.split("=")
        if key and value:
            m[key] = value
    return m

def get_paypal_url(params):
    key = [(k, v) for k, v in params.iteritems()]
    sorted_data = sorted(key, key=lambda x : x[0], reverse=False)
    list_data = ['%s=%s' % (str(k),str(v)) for k, v in sorted_data]
    data = '&'.join(list_data)
    return memc.PAYPAL_CHECKOUT_URL +"?"+ data

def create_order():
    engine = app.get_engine("order_seq")
    lastrowid = engine.master_execute("UPDATE order_seq SET id=LAST_INSERT_ID(id+1)")
    return "%s%s" % (lastrowid, time.strftime("%Y%m", time.localtime()))
