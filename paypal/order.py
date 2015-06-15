# -*- coding: utf-8 -*-

from apps.models.paypal import PayPal
from django.http import HttpResponse, HttpResponseRedirect

def make_order(request):
    """
    @Description: make order
    @Request Parmeters:
        uid - User ID
        amount - amount
        productId - product ID
        productName - product Name
        productInfo - product Describe
    """
    data = dict(request.REQUEST.iteritems())
    uid = data.get("uid")
    amount = data.get("amount")
    productId = data.get("productId")
    productName = data.get("productName")
    productInfo = data.get("productInfo")
    if not (uid and amount):
        return HttpResponse("args error")
    
    paypalObj = PayPal.install(uid, amount, productId, productName, productInfo)

    # make a order and obtain token
    result, ret = paypalObj.set_express_checkout()
    if not ret:
        return HttpResponse("order error")

    token = result.get("TOKEN")
    url = memc.PAYPAL_LOGIN_URL + "?cmd=_express-checkout&token={0}".format(token)
    return HttpResponseRedirect(url)
