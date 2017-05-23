import json
from django.http import HttpResponse
from BLL.get_informition import BLL_get_dep_selfcheck_data,BLL_get_selfcheck_data,BLL_get_dep_selfcheck_count_data
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from BLL.set_informition import BLL_delete_selfcheck_data,BLL_delete_mulrecord_data
from BLL.set_informition import BLL_set_newpasswd,BLL_deleteTimeSpan_data

def querySelf(request):
    return render_to_response('querySelf.html')

def userQuery(request):
    return render_to_response('userQuery.html')

def userQueryCount(request):
    return render_to_response('userQueryCount.html')

def passwdChange(request):
    return render_to_response('passwdChange.html')

def source404(request):
    return render_to_response('source404.html')

@csrf_exempt
def get_selfcheck_data(request):
    ret={}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    scanTime = request.POST.get("scanTime", "").encode("utf-8")
    if not user_acc.decode("utf-8") or not page.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret["selfcheck_fun_data"] = BLL_get_selfcheck_data(user_acc)
    ret["selfcheck_data"] = BLL_get_dep_selfcheck_data(user_acc,page,scanTime)
    ret["count"] = len(BLL_get_dep_selfcheck_data(user_acc,0,scanTime))
    return HttpResponse(json.dumps(ret), content_type='application/json')

# 删除记录
@csrf_exempt
def set_selfcheck_data(request):
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
   # user_acc = request.POST.get("userAcc", "").encode("utf-8")
    usId = request.POST.get("usId", "").encode("utf-8")
    #print (user_acc)
    print (usId)
    if not usId.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_delete_selfcheck_data(usId)
    return HttpResponse(json.dumps(ret), content_type='application/json')
	
# 修改密码
@csrf_exempt
def set_newpasswd(request):
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    passwd = request.POST.get("passwd", "").encode("utf-8")
    if not user_acc.decode("utf-8") or not passwd.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_set_newpasswd(user_acc,passwd)
    return HttpResponse(json.dumps(ret), content_type='application/json')
	
@csrf_exempt
def delete_mulrecord_data(request):   #删除多条记录
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    record_list = request.POST.get("record_list", "").encode("utf-8")
    user_acc = request.POST.get("user_acc", "").encode("utf-8")
    if not record_list.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_delete_mulrecord_data(record_list, user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')
	
@csrf_exempt
def get_selfcheck_count_data(request):
    ret={}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    if not user_acc.decode("utf-8") or not page.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret["selfcheck_fun_data"] = BLL_get_selfcheck_data(user_acc)
    ret["selfcheck_count_data"] = BLL_get_dep_selfcheck_count_data(user_acc,page)
    ret["count"] = len(BLL_get_dep_selfcheck_count_data(user_acc,0))
    return HttpResponse(json.dumps(ret), content_type='application/json')
	
@csrf_exempt
def delete_timespan_data(request):   #删除多条记录
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    record_list = request.POST.get("record_list", "").encode("utf-8")
    user_acc = request.POST.get("user_acc", "").encode("utf-8")
    if not record_list.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_deleteTimeSpan_data(record_list, user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')