#!/usr/bin/python
# -*- coding: utf-8 -*-
#paython 2.7
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import time
from xml.dom import minidom


import hashlib
from heapq import heappush, heappop
from collections import OrderedDict


import requests


SandBox_Url = 'https://api.mch.weixin.qq.com/sandboxnew/pay/getsignkey'
MicroPay_Url = "https://api.mch.weixin.qq.com/sandboxnew/pay/micropay"
UnifiedOrder_Url = "https://api.mch.weixin.qq.com/sandboxnew/pay/unifiedorder"
OrderQuery_Url = "https://api.mch.weixin.qq.com/sandboxnew/pay/orderquery"
ReFund_Url = "https://api.mch.weixin.qq.com/sandboxnew/pay/refund"
RefundQuery_Url = "https://api.mch.weixin.qq.com/sandboxnew/pay/refundquery"
DownloadBill_Url = "https://api.mch.weixin.qq.com/sandboxnew/pay/downloadbill"
nonce_str = "5K8264ILTKCH16CQ2502SI8ZNMTM67VS"


if __name__ == '__main__':
    mch_id = ""  #商户号
    wxpay_key = ""  #支付密钥



def get_sign_key(mch_id, key):
    template = "<xml><mch_id><![CDATA[{0}]]></mch_id>" \
               "<nonce_str><![CDATA[{1}]]></nonce_str>" \
               "<sign><![CDATA[{2}]]></sign></xml>"
    nonce_str = "5K8264ILTKCH16CQ2502SI8ZNMTM67VS"
    encrypted_str = "mch_id=" + mch_id + "&nonce_str=" + nonce_str + "&key=" + key
    m = hashlib.md5()
    m.update(encrypted_str.encode('utf-8'))
    sign_key_request_data = template.format(
        mch_id, nonce_str, m.hexdigest().upper())
    result = requests.post(SandBox_Url, sign_key_request_data)
    dom = minidom.parseString(result.content)
    root = dom.documentElement
    sandbox_signkey = ''
    if root.getElementsByTagName("return_code")[0].childNodes[0].nodeValue == "FAIL":
        retmsg = root.getElementsByTagName(
            "return_msg")[0].childNodes[0].nodeValue
        raise RuntimeError("请求出了点小错误:" + retmsg)
    else:
        sandbox_signkey = root.getElementsByTagName(
            "sandbox_signkey")[0].childNodes[0].nodeValue
    print("亲，这就是你的沙箱密钥了哦: " + sandbox_signkey)
    return sandbox_signkey



def to_tree_map(param_map):
    keys = param_map.keys()
    heap = []
    for item in keys:
        heappush(heap, item)


    sort = []
    while heap:
        sort.append(heappop(heap))


    res_map = OrderedDict()
    for key in sort:
        res_map[key] = param_map.get(key)


    return res_map



def build_xml(param, wxpay_key):
    tree_map = to_tree_map(param)
    encrypted_str = ""
    for k in tree_map:
        encrypted_str += "{}={}&".format(k, tree_map[k])
    encrypted_str = encrypted_str + "key=" + wxpay_key
    m = hashlib.md5()
    m.update(encrypted_str.encode('utf-8'))
    sign = m.hexdigest().upper()
    param.update(sign=sign)


    complete_tree_map = to_tree_map(param)
    xml = "<xml>"
    for k in complete_tree_map:
        xml += "<{}><![CDATA[{}]]></{}>".format(k, complete_tree_map[k], k)
    xml += "</xml>"
    return xml



def request_handler(url, xml, desc):
    result = requests.post(url, xml)
    print(desc + "我才不是请求结果呢：" + result.content.decode("utf-8"))



def upgrade(mch_id, wxpay_key):
    if mch_id == "":
        raise RuntimeError("出差错了哦，亲，你的商户号在哪呢？不填写商户号亲亲是要给空气去验收吗？")


    if wxpay_key == "":
        raise RuntimeError("出差错了哦，亲，你不填写商户密钥怎么继续呢，是用爱吗？")
    key = get_sign_key(mch_id, wxpay_key)
    nonce_str = "5K8264ILTKCH16CQ2502SI8ZNMTM67VS"
    out_trade_no = round(time.time())
    MicroPay_param = {
        'appid': "wxd678efh567hg6787",
                 'mch_id': mch_id,
                 'nonce_str': nonce_str,
                 'body': "check",
                 'out_trade_no': out_trade_no,
                 'total_fee': "501",
                 'spbill_create_ip': "8.8.8.8",
                 'auth_code': "120061098828009406",
    }
    MicroPay_xml = build_xml(MicroPay_param, key)
    request_handler(MicroPay_Url, MicroPay_xml, "亲，用例编号1001刷卡正常支付有结果了，快来看呀 ")
    time.sleep(1)


    OrderQuery_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no,
    }
    OrderQuery_xml = build_xml(OrderQuery_param, key)
    request_handler(OrderQuery_Url, OrderQuery_xml,
                    "亲，用例编号1001刷卡正常支付查询出结果了，快来看呀 ")
    time.sleep(1)


    out_trade_no_2nd = round(time.time())
    print("我是1002下单的订单号：", + out_trade_no_2nd)
    MicroPay_param = {
        'appid': "wxd678efh567hg6787",
                 'mch_id': mch_id,
                 'nonce_str': nonce_str,
                 'body': "check",
                 'out_trade_no': out_trade_no_2nd,
                 'total_fee': "502",
                 'spbill_create_ip': "8.8.8.8",
                 'auth_code': "120061098828009406",
    }
    MicroPay_xml = build_xml(MicroPay_param, key)
    request_handler(MicroPay_Url, MicroPay_xml,
                    "亲，用例编号1002刷卡正常支付结果来了，你还抓紧不来看 ")
    time.sleep(1)


    OrderQuery_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no_2nd,
    }
    OrderQuery_xml = build_xml(OrderQuery_param, key)
    request_handler(OrderQuery_Url, OrderQuery_xml,
                    "亲，用例编号1002刷卡正常支付查询结果，结果好像有点不太对呢 ")
    time.sleep(1)


    ReFund_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_refund_no': out_trade_no,
        'total_fee': "502",
        'refund_fee': "501",
        'out_trade_no': out_trade_no_2nd,
    }


    ReFund_xml = build_xml(ReFund_param, key)
    request_handler(ReFund_Url, ReFund_xml,
                    "亲，下面展示的是用例编号1002刷卡支付退款的结果，你猜对不对 ")
    time.sleep(1)


    RefundQuery_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no_2nd,
    }


    RefundQuery_xml = build_xml(RefundQuery_param, key)
    request_handler(RefundQuery_Url, RefundQuery_xml,
                    "亲，用例编号1002刷卡支付退款查询结果返回中，加载不出来长按电源键或Ait+F4重试哦 ")
    time.sleep(1)


    nonce_str = "5K8264ILTKCH16CQ2502SI8ZNMTM67VS"
    out_trade_no = round(time.time())
    UnifiedOrder_param = {
        'appid': "wxd678efh567hg6787",
                 'mch_id': mch_id,
                 'nonce_str': nonce_str,
                 'body': "check",
                 'out_trade_no': out_trade_no,
                 'total_fee': "551",
                 'notify_url': "https://www.weixin.qq.com/wxpay/pay.php",
                 'spbill_create_ip': "8.8.8.8",
                 'trade_type': "JSAPI",
    }
    UnifiedOrder_xml = build_xml(UnifiedOrder_param, key)
    request_handler(UnifiedOrder_Url, UnifiedOrder_xml,
                    "亲，用例编号1003-公众号/APP/扫码正常支付有结果了，快来看呀 ")
    time.sleep(1)
    OrderQuery_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no,
    }
    OrderQuery_xml = build_xml(OrderQuery_param, key)
    request_handler(OrderQuery_Url, OrderQuery_xml,
                    "亲，用例编号1003-公众号/APP/扫码正常支付查询出结果了，快来看呀 ")
    time.sleep(1)


    out_trade_no_2nd = round(time.time() * 1000)
    print("我是1002下单的订单号：", + out_trade_no_2nd)
    UnifiedOrder_param = {
        'appid': "wxd678efh567hg6787",
                 'mch_id': mch_id,
                 'nonce_str': nonce_str,
                 'body': "check",
                 'out_trade_no': out_trade_no_2nd,
                 'total_fee': "552",
                 'notify_url': "https://www.weixin.qq.com/wxpay/pay.php",
                 'spbill_create_ip': "8.8.8.8",
                 'trade_type': "JSAPI",
    }
    UnifiedOrder_xml = build_xml(UnifiedOrder_param, key)
    request_handler(UnifiedOrder_Url, UnifiedOrder_xml,
                    "亲，用例编号1004-公众号/APP/扫码支付退款结果来了，你还抓紧不来看 ")
    time.sleep(1)


    OrderQuery_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no_2nd,
    }
    OrderQuery_xml = build_xml(OrderQuery_param, key)
    request_handler(OrderQuery_Url, OrderQuery_xml,
                    "亲，用例编号1004-公众号/APP/扫码支付退款查询结果，结果好像有点不太对呢 ")
    time.sleep(1)


    ReFund_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_refund_no': out_trade_no,
        'total_fee': "552",
        'refund_fee': "551",
        'out_trade_no': out_trade_no_2nd,
    }


    ReFund_xml = build_xml(ReFund_param, key)
    request_handler(ReFund_Url, ReFund_xml,
                    "亲，下面展示的是用例编号1004-公众号/APP/扫码支付退款的结果，你猜对不对 ")
    time.sleep(1)


    RefundQuery_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'out_trade_no': out_trade_no_2nd,
    }


    RefundQuery_xml = build_xml(RefundQuery_param, key)
    request_handler(RefundQuery_Url, RefundQuery_xml,
                    "亲，用例编号1004-公众号/APP/扫码支付退款查询结果返回中，加载不出来长按电源键或Ait+F4重试哦 ")
    time.sleep(1)


    DownloadBill_param = {
        'appid': "wxd678efh567hg6787",
        'mch_id': mch_id,
        'nonce_str': nonce_str,
        'bill_date': "2021-04-01",
        'bill_type': "ALL"
    }


    DownloadBill_xml = build_xml(DownloadBill_param, key)
    request_handler(DownloadBill_Url, DownloadBill_xml,
                    "亲，你要下载交易的对账单来了，加载中······，加载不出来长按电源键或Ait+F4重试哦 ")



upgrade(mch_id, wxpay_key)