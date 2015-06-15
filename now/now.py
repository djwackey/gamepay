# encoding: utf-8

import time
import urllib
import requests
from config import memc
from hashlib import md5

def make_request(payObj):
    params = {"appId":           memc.NOW_WEB_APPID,
              "mhtOrderNo":      payObj.oid,
              "mhtOrderName":    payObj.productName,
              "mhtOrderType":    memc.TRADE_ORDER_TYPE,
              "mhtCurrencyType": memc.CURRENCY_TYPE,
              "notifyUrl":       memc.SERVER_NOTIFY_URL,
              "frontNotifyUrl":  memc.FRONT_NOTIFY_URL,
              "mhtCharset":      memc.TRADE_CHARSET,
              "payChannelType":  memc.TRADE_CHANNEL_TYPE,
              "mhtOrderAmt":     "%.f"%(float(payObj.amount)*100),
              "mhtOrderDetail":  payObj.productInfo,
              "mhtOrderStartTime": time.strftime("%04Y%02m%02d%02H%02M%02S", time.localtime())}
              #"mhtOrderTimeOut": "3600",
              #"mhtReserved":  "",
              #"consumerId":   "",
              #"consumerName": ""}

    params["mhtSignature"] = make_sign(params, memc.WEB_SECRET_KEY)
    params["funcode"]     = memc.TRADE_FUNCODE
    params["deviceType"]  = memc.DEVICE_TYPE_WEB
    params["mhtSignType"] = memc.TRADE_SIGN_TYPE

    payload = urllib.urlencode(params)
    return memc.NOW_PAY_URL + "?" + payload

def make_sign(data, secret_key):
    # step 1 得到表单字符串
    key = [(k, v) for k, v in data.iteritems()]
    sorted_data = sorted(key, key=lambda x : x[0], reverse=False)
    list_data = ['%s=%s' % (str(k), str(v)) for k, v in sorted_data if v]
    form_str = '&'.join(list_data)
    # step 2 得到密钥MD5值
    secret_value = md5(secret_key).hexdigest()
    return md5(form_str + "&" + secret_value).hexdigest()

def check_sign(data, secret_key):
    signType = data.get("signType")
    if signType != "MD5":
        print "check_now_sign", signType
        return False

    sign = data.get("signature")
    # 排除下面两个字段
    data.pop("signType")
    data.pop("signature")
    return (sign == make_sign(data, secret_key))

def parse_body(body):
    pairs = body.split("&")
    m = {}
    for pair in pairs:
        key, value = pair.split("=")
        m[key] = value
    return m
