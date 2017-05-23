#-*-coding:utf-8-*-


import json
from django.http import HttpResponse
from django.shortcuts import render_to_response


def first(request):
    return render_to_response('first.html')

def user_error(request):
    return render_to_response('userError.html')

def userManage(request):
    return render_to_response('userManage.html')

def about(request):
    return render_to_response('about.html')

def userConn(request):
    return render_to_response('userConn.html')

def keyword(request):
    return render_to_response('keyword.html')

def departmentManage(request):
    return render_to_response('departmentManage.html')

def userScan(request):
    return render_to_response('userScan.html')

def userErrorCount(request):
    return render_to_response('userErrorCount.html')

def errorDataMore(request):
    return render_to_response('errorDataMore.html')