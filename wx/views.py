# from django.shortcuts import render
#
# # Create your views here.
# # coding=utf-8
#
# from django.http import HttpResponse
# import hashlib, time, re
# from xml.etree import ElementTree as ET
#
#
# def weixin(request):
#     token = "your token here"
#     params = request.GET
#     args = [token, params['timestamp'], params['nonce']]
#     args.sort()
#     if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
#         if params.has_key('echostr'):
#             return HttpResponse(params['echostr'])
#         else:
#             reply = """<xml>
#                 <ToUserName><![CDATA[%s]]></ToUserName>
#                 <FromUserName><![CDATA[%s]]></FromUserName>
#                 <CreateTime>%s</CreateTime>
#                 <MsgType><![CDATA[text]]></MsgType>
#                 <Content><![CDATA[%s]]></Content>
#                 <FuncFlag>0</FuncFlag>
#                 </xml>"""
#
#         if request.raw_post_data:
#             xml = ET.fromstring(request.raw_post_data)
#             content = xml.find("Content").text
#             fromUserName = xml.find("ToUserName").text
#             toUserName = xml.find("FromUserName").text
#             postTime = str(int(time.time()))
#             if not content:
#                 return HttpResponse(reply % (toUserName, fromUserName, postTime, "输入点命令吧..."))
#             if content == "Hello2BizUser":
#                 return HttpResponse(reply % (toUserName, fromUserName, postTime, "更多功能开发中..."))
#         else:
#             return HttpResponse(reply % (toUserName, fromUserName, postTime, "暂不支持任何命令交互哦,功能开发中..."))
#
#     else:
#         return HttpResponse("Invalid Request")


# coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, Template
from django.utils.encoding import smart_str
import hashlib
from xml.etree import ElementTree as etree


@csrf_exempt
def wx(request):
    if request.method == 'GET':
        if request.GET.get('signature', None) is not None:
            response = HttpResponse(checkSignature(request))
            return response
        else:
            response=HttpResponse("err")
            return response
    else:
        xmlstr = smart_str(request.body)
        xml = etree.fromstring(xmlstr)
        ToUserName = xml.find('ToUserName').text
        FromUserName = xml.find('FromUserName').text
        CreateTime = xml.find('CreateTime').text
        Msgtype = xml.find('Msgtype').text
        Content = xml.find('Content').text
        Msgid = xml.find('Msgid').text
        reply_xml = """<xml>
       <ToUserName><![CDATA[%s]]></ToUserName>
       <FromUserName><![CDATA[%s]]></FromUserName>
       <CreateTime>%s</CreateTime>
       <Msgtype><![CDATA[text]]></Msgtype>
       <Content><![CDATA[%s]]></Content>
       </xml>""" % (FromUserName, ToUserName, CreateTime, Content + "This is test message,developing***")
        return HttpResponse(reply_xml)


def checkSignature(request):
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    #这里的token我放在setting，可以根据自己需求修改
    token = "wsytsgsl"

    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = "%s%s%s" % tuple(tmplist)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echostr
    else:
        return None