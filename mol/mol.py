# encoding: utf-8

import time
import json
import hashlib
import traceback
from config import memc
from waclib import utils
from waclib.model import BaseModel

class MOL(BaseModel):    
    def __init__(self, oid = None):
        BaseModel.__init__(self)
        self.oid = oid
        self.uid = None
        self.amount = 0
        self.tradeAmt = 0
        self.channelId = 0
        self.statusCode = 0
        self.productId = None
        self.productName = None
        self.productInfo = None
        self.currencyCode = None
        self.reserved = None
        self.version = None
        self.payTime = None
        self.createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    @classmethod
    def install(cls, uid, amount, productId, productName, productInfo):
        oid = utils.create_order()
        mol = cls(oid)
        mol.uid = uid
        mol.amount = amount
        mol.productId = productId
        mol.productName = productName
        mol.productInfo = productInfo
        mol.put()
        return mol

    def create_order_data(self):
        m = {"referenceId":     self.oid,
             "customerId":      self.uid,
             "amount":          self.amount,
             "channelId":       self.channelId,
             "description":     self.productInfo,
             "version":         memc.MOL_API_VERSION,
             "returnUrl":       memc.MOL_RETURN_URL,
             "currencyCode":    memc.MOL_CUID,
             "applicationCode": memc.MOL_APP_CODE,
             }
        m["signature"] = self.make_sign(m)
        return "&".join(k + "=" + str(m[k]) for k in m.keys())

    def update_order(self, data):
        try:
            self.version = data.get("version")
            self.tradeAmt = data.get("amount")
            self.customerId = data.get("customerId")
            self.channelId = data.get("channelId")
            self.signature = data.get("signature")
            self.paymentId = data.get("paymentId")
            self.statusCode = data.get("paymentStatusCode")
            self.currencyCode = data.get("currencyCode")
            paytime = data.get("paymentStatusDate").replace("T", " ")
            self.payTime = paytime[:len(paytime)-1]
            self.put()
            return True
        except Exception, e:
            traceback.print_exc()
        return False

    def query_order(data):
        pass

    def check_sign(self, data):
        applicationCode = data.get("applicationCode")
        if applicationCode != memc.MOL_APP_CODE:
            print "error app code", applicationCode
            return False

        signature = data.get("signature")
        data.pop("signature")
        return (signature == self.make_sign(data))

    def make_sign(self, data):
        payload = "".join(str(data[k]) for k in sorted(data.keys()))
        payload += memc.MOL_SECRET_KEY
        return hashlib.md5(payload).hexdigest()

    def get_payment_url(self):
        data = self.create_order_data()
        try:
            resp = requests.post(memc.MOL_PAY_URL, data, timeout=5)
            if resp.status_code == 200:
                content = json.loads(resp.text)
                return content.get("paymentUrl")
        except Exception, e:
            traceback.print_exc()
        return None
