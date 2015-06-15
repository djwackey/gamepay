# -*- coding: utf-8 -*-

# pay status
PAY_ORDER_START  = "0"		# paying
PAY_ORDER_DETAIL = "1"		# requesting
PAY_TRADE_FAILED = "9"      # trade failed
PAY_TRADE_SUCCESS = "10"	# trade success
PAY_NOTIFY_SUCCESS = "11"	# notify success

# pay type
PAY_TYPE_PAYPAL = 1       # PayPal
PAY_TYPE_MYCARD = 2	      # MYCARD
PAY_TYPE_GASH   = 3	      # GASH
PAY_TYPE_MOL    = 4	      # MOL
PAY_TYPE_NOW    = 5	      # NOW
PAY_TYPE_MO9    = 6       # MO9

DEBUG = False
if DEBUG:
    GASH_ORDER_URL = "https://stage-api.eg.gashplus.com/CP_Module/order.aspx"
    GASH_SETTLE_URL = "https://stage-api.eg.gashplus.com/CP_Module/settle.asmx?WSDL"
    GASH_CHECK_ORDER_URL = "https://stage-api.eg.gashplus.com/CP_Module/checkorder.asmx?WSDL"
    GASH_CID  = "XXX"
    GASH_KEY1 = "XXX"
    GASH_KEY2 = "XXX"
    GASH_PASSWORD = "XXX"

    PAYPAL_CHECKOUT_URL = "https://api-3t.sandbox.paypal.com/nvp"
    PAYPAL_LOGIN_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"

    PAYPAL_API_USER = "XXX"
    PAYPAL_API_PSWD = "XXX"
    PAYPAL_API_SIGN = "XXX"

    MOL_PAY_URL = "https://sandbox.api.mol.com/payout/payments"
    MOL_APP_CODE = "XXX"
    MOL_SECRET_KEY = "XXX"
else:
    GASH_ORDER_URL = "https://api.eg.gashplus.com/CP_Module/order.aspx"
    GASH_SETTLE_URL = "https://api.eg.gashplus.com/CP_Module/settle.asmx?WSDL"
    GASH_CHECK_ORDER_URL = "https://api.eg.gashplus.com/CP_Module/checkorder.asmx?WSDL"
    GASH_CID  = "XXX"
    GASH_KEY1 = "XXX"
    GASH_KEY2 = "XXX"
    GASH_PASSWORD = "XXX"

    PAYPAL_CHECKOUT_URL = "https://api-3t.paypal.com/nvp"
    PAYPAL_LOGIN_URL = "https://www.paypal.com/cgi-bin/webscr"

    PAYPAL_API_USER = "XXX"
    PAYPAL_API_PSWD = "XXX"
    PAYPAL_API_SIGN = "XXX"

    MOL_PAY_URL = "https://api.mol.com/payout/payments"
    MOL_APP_CODE = "XXX"
    MOL_SECRET_KEY = "XXX"

GASH_CUID = "TWD"
GASH_MID  = "XXX"
GASH_BID  = "XXX"
GASH_MSG_TYPE = "0100"
GASH_ORDER_TYPE = "M"
GASH_ORDER_PCODE = "300000"
GASH_QUERY_PCODE = "200000"

PAYPAL_CUID = "USD"
PAYPAL_API_VERSION = "121"
    
PAY_CALLBACK_URL = "http://sdk.test.com"
PAY_SUCCESS_URL   = PAY_CALLBACK_URL + '/pay/success'
PAYPAL_RESULT_URL = PAY_CALLBACK_URL + '/paypal/result'
MOL_RETURN_URL    = PAY_CALLBACK_URL + '/mol/result' 

MOL_API_VERSION = "v1"
MOL_CUID = "TWD"


#############
# ipaynow
#############
NOW_PAY_URL = "https://api.ipaynow.cn"
FRONT_NOTIFY_URL  = PAY_CALLBACK_URL + "/pay/success"
SERVER_NOTIFY_URL = PAY_CALLBACK_URL + "/pay/now/result"
NOW_WEB_APPID = "XXX"
NOW_SDK_APPID = "XXX"
# MD5 secret key
WEB_SECRET_KEY = "XXX"
SDK_SECRET_KEY = "XXX"
TRADE_FUNCODE = "WP001"
QUERY_FUNCODE = "MQ001"
NOTIFY_FUNCODE = "N001"
TRADE_CHARSET = "UTF-8"
TRADE_SIGN_TYPE = "MD5"
TRADE_ORDER_TYPE = "01"
TRADE_CHANNEL_TYPE = "13" # WeChat
DEVICE_TYPE_SDK = "01"  # SDK
DEVICE_TYPE_WEB = "06"  # WEB
CURRENCY_TYPE = "156"   # RMB
DEVICE_TYPE_MAPPING = {DEVICE_TYPE_WEB: WEB_SECRET_KEY,
                       DEVICE_TYPE_SDK: SDK_SECRET_KEY}
