#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 登陆页面显示与处理
@time: 2017-1-13
'''

import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from BLL.get_informition import get_user_login
from BLL.get_verification_code import get_indentiry_code_img
from django.views.decorators.csrf import csrf_exempt
from BLL.close_django import check_auth


def login(request):
    return render_to_response('login.html')

def loginScanSelf(request):
    return render_to_response('loginScanSelf.html')


@csrf_exempt
def user_login(request):    #验证用户登陆
    if request.is_ajax() and request.method == "POST":
        userName = request.POST.get("userName", "").encode("utf-8")
        passwd = request.POST.get("passwd", "").encode("utf-8")
    else:
        return HttpResponse(json.dumps(False), content_type='application/json')

    if userName.decode("utf-8") == "" or passwd.decode("utf-8") == "":
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret = get_user_login(userName, passwd)

    if ret[0][0] == 0:
        return HttpResponse(json.dumps(False), content_type='application/json')
    if int(ret[0][1]) == 0:
        return HttpResponse(json.dumps(-1), content_type='application/json')

    # user_ip = request.META["REMOTE_ADDR"]
    request.session["status"] = ret[0][1]
        # request.session["user_ip"] = user_ip
    return HttpResponse(json.dumps(ret[0][1]), content_type='application/json')


@csrf_exempt
def indentifying_code(request): #获取验证码
    check_auth()
    img = get_indentiry_code_img()
    return HttpResponse(json.dumps(img), content_type='application/json')




