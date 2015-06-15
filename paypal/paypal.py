# encoding: utf-8

import time
from config import memc
from urllib import unquote
from waclib import util
from waclib.model import BaseModel

class PayPal(BaseModel):
    """
        payerId - 订单号
        status - 支付状态
        payTime - 订单支付时间
    """
    def __init__(self, oid=None):
        BaseModel.__init__(self)
        self.oid = oid
        self.uid = None
        self.amount = 0
        self.taxAmount = 0
        self.feeAmount = 0
        self.status = None
        self.payerId = None
        self.payTime = None
        self.orderTime = None
        self.productId = None
        self.productName = None
        self.productInfo = None
        self.tradeAmount = None
        self.transactionId = None
        self.cuid = memc.PAYPAL_CUID
        self.payStatus = memc.PAY_ORDER_START
        self.createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    @classmethod
    def install(cls, uid, amount, productId, productName, productInfo):
        """
	    @Description: 创建PayPal支付订单对象
	    @Parameters:
		    uid - 用户ID
            cuid - 币种
		    amount - 商品金额
		    productId - 商品ID
		    productName - 商品名称
		    productInfo - 商品描述
		    createTime - 订单创建时间
	    @Return:
		    obj - PayPal支付订单对象
        """
        oid = util.create_order()
        obj = cls(oid)
        obj.uid = uid
        obj.amount = amount
        obj.productId = productId
        obj.productName = productName
        obj.productInfo = productInfo
        obj.put()
        return obj 

    def update_express_details(self, result):
        """
	    @Description: 更新细节获取后的订单
        """
        self.status = memc.PAY_ORDER_DETAIL
        self.payerId = result.get('PAYERID')
        self.payStatus = result.get('PAYERSTATUS')
        self.put()

    def update_express_payment(self, result):
        """
	    @Description: 更新快速支付后的订单
        """
        self.status        = memc.PAY_TRADE_SUCCESS
        self.tradeAmount   = unquote(result.get('PAYMENTINFO_0_AMT'))
        self.taxAmount     = unquote(result.get('PAYMENTINFO_0_TAXAMT'))
        self.feeAmount     = unquote(result.get('PAYMENTINFO_0_FEEAMT'))
        self.payStatus     = result.get('PAYMENTINFO_0_PAYMENTSTATUS')
        self.transactionId = result.get('PAYMENTINFO_0_TRANSACTIONID')
        self.orderTime     = unquote(result.get('PAYMENTINFO_0_ORDERTIME'))
        self.payTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.put()

    """
    Result Example:
    {u'ACK': u'Success', 
     u'TIMESTAMP': u'2015%2d03%2d13T07%3a01%3a39Z', 
     u'TOKEN': u'EC%2d3G988532370131530', 
     u'VERSION': u'78', 
     u'BUILD': u'15735246', 
     u'CORRELATIONID': u'2c5a12679bbc1'}
    """
    def set_express_checkout(self):
        """
	    @Description: 请求PayPal使用快速支付快速结账
        """
        params = {"METHOD": "SetExpressCheckout",
                  "RETURNURL": memc.PAYPAL_RESULT_URL + "?oid={0}".format(self.oid),
                  "CANCELURL": memc.PAYPAL_LOGIN_URL,
                  "USER":      memc.PAYPAL_API_USER,
                  "PWD":       memc.PAYPAL_API_PSWD,
                  "SIGNATURE": memc.PAYPAL_API_SIGN,
                  "VERSION":   memc.PAYPAL_API_VERSION,
                  "PAYMENTREQUEST_0_AMT":     self.amount,
                  "PAYMENTREQUEST_0_DESC":    self.productName,
                  "PAYMENTREQUEST_0_INVNUM":  self.oid,
                  "PAYMENTREQUEST_0_ITEMAMT": self.amount,
                  "PAYMENTREQUEST_0_PAYMENTACTION": "Sale",
                  "PAYMENTREQUEST_0_CURRENCYCODE": memc.PAYPAL_CUID,
                  # 以下用于手机显示（必须加上）
                  "L_PAYMENTREQUEST_0_AMT0":  self.amount,
                  "L_PAYMENTREQUEST_0_NAME0": self.productName,
                  "L_PAYMENTREQUEST_0_DESC0": self.productName,
                 }
        url = util.get_paypal_url(params)
        resp, ret = util.send_requests(url)
        if ret:
            result = util.format_response(resp.text)
            ack = result.get("ACK")
            if ack == "Success":
                return result, True
        return {}, False

    """
    Result Example:
    {u'PAYMENTREQUEST_0_SHIPTOSTREET': u'NO%201%20Nan%20Jin%20Road', 
     u'ACK': u'Success', 
     u'LASTNAME': u'Buyer', 
     u'SHIPTOCITY': u'Shanghai', 
     u'SHIPTONAME': u'Buyer%20Test', 
     u'SHIPDISCAMT': u'0%2e00', 
     u'PAYMENTREQUEST_0_ADDRESSSTATUS': u'Unconfirmed', 
     u'PAYMENTREQUEST_0_INSURANCEAMT': u'0%2e00',
     u'SHIPPINGAMT': u'0%2e00', 
     u'ADDRESSSTATUS': u'Unconfirmed', 
     u'EMAIL': u'chunyan%2efeng%2dbuyer%40rekoo%2ecom', 
     u'CORRELATIONID': u'544d614779496', 
     u'SHIPTOCOUNTRYCODE': u'CN', 
     u'PAYMENTREQUEST_0_INSURANCEOPTIONOFFERED': u'false', 
     u'TAXAMT': u'0%2e00', 
     u'SHIPTOSTREET': u'NO%201%20Nan%20Jin%20Road', 
     u'PAYMENTREQUEST_0_AMT': u'10%2e00', 
     u'PAYMENTREQUEST_0_HANDLINGAMT': u'0%2e00', 
     u'PAYMENTREQUEST_0_TAXAMT': u'0%2e00', 
     u'SHIPTOCOUNTRYNAME': u'China', 
     u'PAYMENTREQUESTINFO_0_ERRORCODE': u'0', 
     u'AMT': u'10%2e00', 
     u'PAYMENTREQUEST_0_SHIPTOZIP': u'200000', 
     u'PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE': u'CN', 
     u'PAYMENTREQUEST_0_SHIPTOCOUNTRYNAME': u'China', 
     u'PAYERID': u'F44DB3V5TY5SY', 
     u'COUNTRYCODE': u'CN', 
     u'PAYMENTREQUEST_0_CURRENCYCODE': u'USD', 
     u'CURRENCYCODE': u'USD', 
     u'PAYMENTREQUEST_0_SHIPTOCITY': u'Shanghai', 
     u'TOKEN': u'EC%2d27E62959R0795740H', 
     u'VERSION': u'78', 
     u'PAYMENTREQUEST_0_SHIPDISCAMT': u'0%2e00', 
     u'BUILD': u'15735246', 
     u'INSURANCEAMT': u'0%2e00', 
     u'SHIPTOZIP': u'200000', 
     u'CHECKOUTSTATUS': u'PaymentActionNotInitiated', 
     u'PAYMENTREQUEST_0_SHIPTOSTATE': u'Shanghai', 
     u'BILLINGAGREEMENTACCEPTEDSTATUS': u'0', 
     u'PAYERSTATUS': u'verified', 
     u'FIRSTNAME': u'Test', 
     u'TIMESTAMP': u'2015%2d03%2d13T06%3a29%3a24Z', 
     u'SHIPTOSTATE': u'Shanghai', 
     u'PAYMENTREQUEST_0_SHIPPINGAMT': u'0%2e00', 
     u'HANDLINGAMT': u'0%2e00', 
     u'PAYMENTREQUEST_0_SHIPTONAME': u'Buyer%20Test'}
    """
    def get_express_details(self, token):
        """
	    @Description: 请求PayPal获取用户详细信息
        """
        params = {"METHOD":    "GetExpressCheckoutDetails",
                  "USER":      memc.PAYPAL_API_USER,
                  "PWD":       memc.PAYPAL_API_PSWD,
                  "SIGNATURE": memc.PAYPAL_API_SIGN,
                  "VERSION":   memc.PAYPAL_API_VERSION,
                  "TOKEN":     token,
                 }
        url = util.get_paypal_url(params)
        resp, ret = util.send_requests(url)
        if ret:
            result = util.format_response(resp.text)
            ack = result.get("ACK")
            if ack == "Success":
                return result, True
        return {}, False

    """
    Result Example:
    {u'PAYMENTINFO_0_TRANSACTIONTYPE': u'expresscheckout', 
     u'ACK': u'Success', 
     u'PAYMENTINFO_0_PAYMENTTYPE': u'instant', 
     u'PAYMENTINFO_0_REASONCODE': u'None', 
     u'SHIPPINGOPTIONISDEFAULT': u'false', 
     u'INSURANCEOPTIONSELECTED': u'false', 
     u'CORRELATIONID': u'ebdea4d6bd92f', 
     u'PAYMENTINFO_0_TAXAMT': u'0%2e00', 
     u'PAYMENTINFO_0_TRANSACTIONID': u'5N360562MS773311F', 
     u'PAYMENTINFO_0_ACK': u'Success', 
     u'PAYMENTINFO_0_PENDINGREASON': u'None', 
     u'PAYMENTINFO_0_AMT': u'10%2e00', 
     u'PAYMENTINFO_0_PROTECTIONELIGIBILITY': u'Eligible', 
     u'PAYMENTINFO_0_ERRORCODE': u'0', 
     u'TOKEN': u'EC%2d69492988M6877351F', 
     u'VERSION': u'78', 
     u'SUCCESSPAGEREDIRECTREQUESTED': u'false', 
     u'BUILD': u'15735246', 
     u'PAYMENTINFO_0_CURRENCYCODE': u'USD', 
     u'PAYMENTINFO_0_FEEAMT': u'0%2e64', 
     u'TIMESTAMP': u'2015%2d03%2d13T07%3a09%3a05Z', 
     u'PAYMENTINFO_0_SECUREMERCHANTACCOUNTID': u'JTR9GJVCUXL4G', 
     u'PAYMENTINFO_0_PROTECTIONELIGIBILITYTYPE': u'ItemNotReceivedEligible%2cUnauthorizedPaymentEligible', 
     u'PAYMENTINFO_0_ORDERTIME': u'2015%2d03%2d13T07%3a09%3a04Z', 
     u'PAYMENTINFO_0_PAYMENTSTATUS': u'Completed'}
    """
    def do_express_payment(self, token, payerId, amount):
        """
	    @Description: 获取付款
            @Parameters:
                token - 由SetExpressCheckout方法请求获取的token
                payerId - 支付订单编号
                amount - 支付金额
            @Return:
                @1 - 返回的字典数据
                @2 - True/False 成功/失败
        """
        params = {"METHOD":    "DoExpressCheckoutPayment",
                  "USER":      memc.PAYPAL_API_USER,
                  "PWD":       memc.PAYPAL_API_PSWD,
                  "SIGNATURE": memc.PAYPAL_API_SIGN,
                  "VERSION":   memc.PAYPAL_API_VERSION,
                  "TOKEN":     token,
                  "PAYERID":   payerId,
                  "PAYMENTINFO_0_PAYMENTACTION": "Sale",
                  "PAYMENTREQUEST_0_AMT": amount}
        url = util.get_paypal_url(params)
        resp, ret = util.send_requests(url)
        if ret:
            result = util.format_response(resp.text)
            ack = result.get("ACK")
            if ack == "Success":
                return result, True
        return {}, False
