# encoding: utf-8

import now
import urllib
from config import memc

def now_sign(request):
    """
    现在支付SDK支付方式, 返回签名字符串
    """
    body = request.body
    key, value = body.split("=")
    if key != "paydata":
        return HttpResponse("success=Y")

    data = now.parse_body(urllib.unquote(value))

    rtn = "mhtSignature=%s&mhtSignType=MD5" % now.make_sign(data, memc.SDK_SECRET_KEY)
    return HttpResponse(rtn)

def now_notify(request):
    """
    现在支付通知回调
    """
    data = now.parse_body(urllib.unquote(request.body))
    appId = data.get("appId")
    funcode = data.get("funcode")
    deviceType = data.get("deviceType")
    mhtCharset = data.get("mhtCharset")
    mhtOrderNo = data.get("mhtOrderNo")
    mhtOrderAmt = data.get("mhtOrderAmt")
    mhtOrderType = data.get("mhtOrderType")
    mhtCurrencyType = data.get("mhtCurrencyType")
    mhtOrderTimeOut = data.get("mhtOrderTimeOut")
    mhtOrderStartTime = data.get("mhtOrderStartTime")
    payChannelType = data.get("payChannelType")
    nowPayAccNo = data.get("nowPayAccNo")
    tradeStatus = data.get("tradeStatus")
    mhtReserved = data.get("mhtReserved")
    signature = data.get("signature")
    signType = data.get("signType")

    # 若交易未成功，则直接返回
    if tradeStatus != "A001":
        return HttpResponse("success=Y")

    # 验签
    secret_key = memc.DEVICE_TYPE_MAPPING.get(deviceType)
    if not now.check_sign(data, secret_key):
        return HttpResponse("success=Y")

    nowObj = NOW.get(mhtOrderNo)
    if not nowObj:
        return HttpResponse("success=Y")

    # 更新订单信息
    nowObj.update_order(data)

    # 通知游戏服务器
    """ pass """

    return HttpResponse("success=Y")
