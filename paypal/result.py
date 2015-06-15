# -*- coding: utf-8 -*-

import logging
from apps.models.paypal import PayPal
from django.http import HttpResponse

def paypal_result(request):
    """
	PayPal Result
    """
    data = dict(request.REQUEST.iteritems())
    oid = data.get("oid")
    token = data.get("token")
    payerId = data.get("PayerID")
    if not (oid and token):
        logging.error("error parameters.{0}, {1}".format(oid, token))
        return HttpResponse("failed")

    # get the PayPal object
    paypalObj = PayPal.get(oid)
    if not paypalObj:
        logging.error("dont find paypal object.{0}, {1}, {2}".format(oid, token, payerId))
        return HttpResponse("failed")

    # get the express details
    result, ret = paypalObj.get_express_details(token)
    if not ret:
        logging.error("failed to get express details.reason:{0}".format(result))
        return HttpResponse("failed")

    paypalObj.update_express_details(result)

    amount = result.get("AMT")

    # do the express payment
    result, ret = paypalObj.do_express_payment(token, payerId, amount)
    if not ret:
        logging.error("failed to do express payment.reason:{0}".format(result))
        return HttpResponse("failed")

    # update the express payment
    paypalObj.update_express_payment(result)

    # notify the game server
    """ pass """

    logging.info("success for payment.{0}".format(result))
    return HttpResponse("success")
