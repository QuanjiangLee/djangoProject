#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 获取和处理index页面数据
@time: 2017-1-13
'''

EXCEL_PATH = '/home/dev/excl'

import os
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from BLL.get_informition import BLL_get_dep_user_count, BLL_get_dep_user_error, select_scan_file, BLL_get_deprtment_data
from BLL.get_informition import BLL_get_dep_data, BLL_get_user_data, BLL_get_user_conn_data, get_user_name
from BLL.get_informition import BLL_select_key, get_file_data, BLL_get_user_data_select, BLL_get_user_key_select,BLL_get_is_admin
from BLL.get_informition import getKeyCount,BLL_get_dep_user_error_detail
from BLL.set_informition import BLL_update_user_error, BLL_update_user_data, BLL_delete_user_data, BLL_reset_user
from BLL.set_informition import update_user_net_status, update_user_scan_status, BLL_update_key_data, BLL_delete_key_data
from BLL.set_informition import BLL_update_depatment_data, BLL_delete_department_data,BLL_del_user_error
from BLL.client import conn_run
from BLL.decrypt import Decrypt, delete_file
from BLL.get_informition import BLL_get_dep_user_error_bytime,BLL_get_dep_user_error_byperson
from BLL.get_informition import BLL_get_file_data,BLL_get_file_password,BLL_get_dep_count,select_scan_file_bytime
from BLL.set_informition import BLL_insert_remote_record,BLL_import_excel_inf
from BLL import readExcl
from BLL.set_informition import BLL_del_not_exist_file
from BLL.ukey_handle import BLL_get_ukey_info

def index(request):
    user_position_status = request.session.get("status", "")
    # if not user_position_status:
    #     return render_to_response('login.html')
    return render_to_response('index.html')

def indexScanSelf(request):
    user_position_status = request.session.get("status", "")
    # if not user_position_status:
    #     return render_to_response('login.html')
    return render_to_response('indexScanSelf.html')

@csrf_exempt
def quit(request):
    user_position_status = request.session.get("status", "")
    if user_position_status:
        del request.session["status"]
        return HttpResponse(json.dumps(True), content_type='application/json')
    else:
        return HttpResponse(json.dumps(False), content_type='application/json')

def download_client(request):
    filename = request.GET.get('file_name','').encode("utf-8")
    if filename.decode("utf-8") == "":
        request.session["status"] = ""
        return render_to_response("source404.html")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "programFile/clientdownload/")
    if not os.path.exists(file_path):
        request.session["status"] = ""
        return render_to_response("source404.html")
    response = HttpResponse()
    response['Content-Disposition'] = ('attachment;filename='+filename.decode("utf-8")).encode("utf-8")
    filename = filename.decode()
    file = os.path.join(file_path, filename)
    if not file: 
        request.session["status"] = ""
        return render_to_response("source404.html")
    content = open(file, 'rb').read()
    response.write(content)
    try:
        return response
    except:
        return render_to_response("source404.html")

def download_file(request):
    errId = request.GET.get('errId','').encode("utf-8")
    file_name = request.GET.get('file_name','').encode("utf-8")
    if errId.decode("utf-8") == "" or file_name.decode("utf-8") == "":
        request.session["status"] = ""
        return render_to_response("source404.html")
    file_data = BLL_get_file_data(errId)
    if file_data == False:
        request.session["status"] = ""
        return render_to_response("source404.html")
    if not os.path.exists(os.path.join(file_data["file_path"], file_data["file_name"])):
         request.session["status"] = ""
         return render_to_response("source404.html")
    full_path = os.path.join(file_data["file_path"], file_data["file_name"])
    temporary_dir = os.path.join(file_data["file_path"], 'temporary')
    if not os.path.exists(temporary_dir):
        os.mkdir(temporary_dir)
    new_fileName = file_name.decode().rsplit(".", 1)[0]
    response = HttpResponse()
    response['Content-Disposition'] = ('attachment;filename=' + new_fileName).encode("utf-8")
    password = BLL_get_file_password(file_data["file_hash"])
    if password == False:
        return render_to_response("source404.html")
    print(full_path, file_name.decode("utf-8"), password, temporary_dir)
    Decrypt(full_path, file_name.decode("utf-8"), password, temporary_dir)
    full_path = os.path.join(temporary_dir, new_fileName)
    if os.path.exists(full_path):
        response['Content-Length'] = os.path.getsize(full_path)    #  可不加
        content = open(full_path, 'rb').read()
        response.write(content)
        try:
            delete_file(full_path)
        except:
            return render_to_response("source404.html")
        finally:
            return response
    else:
        return render_to_response("source404.html")

'''
@csrf_exempt
def get_dep_user_count(request):    #获取用户异常统计
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_acc.decode("utf-8") or not user_position_status:
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret = BLL_get_dep_user_count(user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')
'''

@csrf_exempt
def get_dep_user_count(request):    #获取用户异常统计
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    errStatus = request.POST.get("errStatus", "").encode("utf-8")
    if not user_acc.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8") or not page.decode("utf-8") or not user_position_status:
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["error_data"] = BLL_get_dep_user_count(user_acc,province,city,department,page,errStatus)
    ret["count"] = len(BLL_get_dep_user_count(user_acc,province,city,department,0,errStatus))
    print(ret["count"])
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def get_user_error(request):    #获取用户异常数据
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    keyclass = request.POST.get("keyclass", "").encode("utf-8")
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    status = request.POST.get("status", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_acc.decode("utf-8") or not page.decode("utf-8") or not status.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    #删除数据库关于报警动态的冗余信息
    BLL_del_not_exist_file()
    ret["error_data"] = BLL_get_dep_user_error(keyclass,user_acc, page, status, province, city, department)
    ret["count"] = len(BLL_get_dep_user_error(keyclass,user_acc, "0".encode("utf-8"), status, province, city, department))
    return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def get_dpt_data(request):    #获取部门信息
    user_position_status = request.session.get("status", "")
    if user_position_status == "":
        return HttpResponse(json.dumps(False), content_type='application/json')

    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")

    if not user_acc.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret = BLL_get_dep_data(user_acc, province, city)

    return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def get_departManage_data(request):    #获取获取部门数据
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_acc.decode("utf-8") or not page.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["department_data"] = BLL_get_deprtment_data(province, city, department, page)
    ret["count"] = len(BLL_get_deprtment_data(province, city, department, "0".encode("utf-8")))
    return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def get_user_data(request):    #获取用户数据
    ret = {}
    user_position_status = request.session.get("status", "")
    if user_position_status == "":
        return HttpResponse(json.dumps(False), content_type='application/json')

    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    if not user_acc.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8") or not page.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["user_data"] = BLL_get_user_data(user_acc, province, city, department, page)
    ret["user_count"] = len(BLL_get_user_data(user_acc, province, city, department, 0))

    return HttpResponse(json.dumps(ret), content_type='application/json')


#根据输入信息查找用户信息
@csrf_exempt
def get_user_data_select(request):    #获取用户数据
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    province = request.POST.get("province","").encode("utf-8")
    city = request.POST.get("city","").encode("utf-8")
    department = request.POST.get("department","").encode("utf-8")
    select_data = request.POST.get("select_data", "").encode("utf-8")
    user_acc = request.POST.get("user_acc", "").encode("utf-8")
    page = request.POST.get("page","").encode("utf-8")

    if not user_acc.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["user_data"] = BLL_get_user_data_select(user_acc, province, city, department, select_data,page)
    ret["user_count"] = len(BLL_get_user_data_select(user_acc, province, city, department, select_data,0))
    return HttpResponse(json.dumps(ret), content_type='application/json')

#根据输入信息查找关键字信息
@csrf_exempt
def get_user_key_select(request):
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False),content_type='application/json')
    province = request.POST.get("province","").encode("utf-8")
    city = request.POST.get("city","").encode("utf-8")
    department = request.POST.get("department","").encode("utf-8")
    select_data = request.POST.get("select_data", "").encode("utf-8")
    user_acc = request.POST.get("user_acc", "").encode("utf-8")
    page = request.POST.get("page","").encode("utf-8")
    if not user_acc.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret["key_data"] = BLL_get_user_key_select(user_acc, province, city, department, select_data,page)
    ret["key_count"] = len(BLL_get_user_key_select(user_acc, province, city, department, select_data,0))
    return HttpResponse(json.dumps(ret),content_type='application/json')

#获取用户连接数据
@csrf_exempt
def get_user_conn_data(request):
    ret = {}
    user_position_status = request.session.get("status", "")
    if user_position_status == "":
        return HttpResponse(json.dumps(False), content_type='application/json')

    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    select_status = request.POST.get("status","")#表示离线（0）或在线（1）

    if not user_acc.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8") or not page.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["user_data"] = BLL_get_user_conn_data(user_acc, province, city, department, page,select_status)
    ret["count"] = len(BLL_get_user_conn_data(user_acc, province, city, department, 0,select_status))

    return HttpResponse(json.dumps(ret), content_type='application/json')

#扫描用户文件
@csrf_exempt
def scan_file(request):
    receive_no = request.POST.get("receive_no", "")
    status = request.POST.get("status", "")
    send_time = request.POST.get("send_time", "")
    send_no = request.POST.get("send_no", "")
    ret = False
    if int(status) == 0:
        comm = "scan_file";
        ret = conn_run(comm, user_list=receive_no)
        if ret == True:
            update_user_scan_status(receive_no, "1")
            BLL_insert_remote_record(send_no, receive_no, comm, send_time, 1)
        else:
            BLL_insert_remote_record(send_no, receive_no, comm, send_time, 0)
    return HttpResponse(json.dumps(ret), content_type='application/json')

#用户自查
@csrf_exempt
def scan_self(request):
    user_no = request.POST.get("user_no", "")
    status = request.POST.get("status", "")
    scan_time = request.POST.get("scan_time", "")
    ret = False
    if int(status) == 0:
        comm = "scan_self"
        ret = conn_run(comm, user_list=user_no)
        if ret == True:
            update_user_scan_status(user_no, "1")
            BLL_insert_remote_record(user_no, user_no, comm, scan_time, 1)
        else:
            BLL_insert_remote_record(user_no, user_no, comm, scan_time, 0)
    return HttpResponse(json.dumps(ret), content_type='application/json')


#获取扫描文件
@csrf_exempt
def get_scan_file(request):
    scanTime = request.POST.get("scanTime","").encode("utf-8")
    province = request.POST.get("province","").encode("utf-8")
    city = request.POST.get("city","").encode("utf-8")
    department = request.POST.get("department","").encode("utf-8")
    userAcc = request.POST.get("userAcc","").encode("utf-8")
    page = request.POST.get("page","").encode("utf-8")
    if not province.decode("utf-8") or not userAcc.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8") or not page.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = {}
    ret["file"] = select_scan_file(scanTime,province, city, department, userAcc, page)
    ret["count"] = len(select_scan_file(scanTime,province, city, department, userAcc,"0".encode("utf-8")))
    if ret["file"] == False:
        return HttpResponse(json.dumps(False), content_type='application/json')
    return HttpResponse(json.dumps(ret), content_type='application/json')

 #关闭网络
@csrf_exempt
def close_net(request):
    ret = False
    receive_no = request.POST.get("receive_no", "")
    status = request.POST.get("status", "")
    send_no = request.POST.get("send_no", "")
    send_time = request.POST.get("send_time", "")
    if int(status) == 0:
        comm = "close_net"
        ret = conn_run(comm, user_list=receive_no)
        if ret == True:
            data= receive_no.split("|")[0:-1]
            for i in data:
                update_user_net_status(i, "1")
            BLL_insert_remote_record(send_no, receive_no, comm, send_time, 1)
        else:
            BLL_insert_remote_record(send_no, receive_no, comm, send_time, 0)
    elif int(status) == 1:
        comm = "open_net"
        ret = conn_run(comm, user_list=receive_no)
        if ret == True:
            data= receive_no.split("|")[0:-1]
            for i in data:
                update_user_net_status(i, "0")
            BLL_insert_remote_record(send_no, receive_no, comm, send_time, 1)
        else:
            BLL_insert_remote_record(send_no, receive_no, comm, send_time, 0)
    return HttpResponse(json.dumps(ret), content_type='application/json')

#客户端自卸载
@csrf_exempt
def remove_self(request):
    receive_no = request.POST.get("receive_no", "")
    send_no = request.POST.get("send_no", "")
    send_time = request.POST.get("send_time", "")
    ret = False
    comm="remove_self"
    ret = conn_run(comm, user_list=receive_no)
    print(type(ret))
    if ret == True:
        BLL_insert_remote_record(send_no, receive_no, comm, send_time, 1)
    else:
        BLL_insert_remote_record(send_no, receive_no, comm, send_time, 0)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def user_error(request):    #设置报警状态
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    secretId = request.POST.get("secretId", "").encode("utf-8")
    status = request.POST.get("status", "").encode("utf-8")
    if not secretId.decode("utf-8") or not status.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_update_user_error(secretId, status)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def get_is_admin(request):  #获取用户是否为超级管理员
    userNo = request.POST.get("userNo", "").encode("utf-8")
    if not userNo.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    user_position_status = BLL_get_is_admin(userNo)
    return HttpResponse(json.dumps(user_position_status), content_type='application/json')


@csrf_exempt
def reset_user(request):    #重置用户数据
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    userNo = request.POST.get("userNo", "").encode("utf-8")
    if not userNo.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_reset_user(userNo)
    return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def get_key_data(request):  #获取关键字数据
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    user_acc = request.POST.get("user_acc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    ret = {}
    user_position_status = request.session.get("status", "")
    if  not province.decode("utf-8") or not user_acc.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret["key_data"] = BLL_select_key(user_acc, province, city, department, page)
    ret["key_count"] = getKeyCount(province, city, department)
    #ret["key_count"] = len(BLL_select_key(user_acc, province, city, department, page))
    return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def input_user_data(request):   #提交用户信息
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    user_data = request.POST.get("user_data", "").encode("utf-8")
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_data.decode("utf-8") or not province.decode("utf-8") or not user_acc.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_update_user_data(user_data, province, city, department, user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def input_key_data(request):    #提交关键字信息
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    key_data = request.POST.get("key_data", "").encode("utf-8")
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not key_data.decode("utf-8") or not province.decode("utf-8") or not user_acc.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_update_key_data(key_data, province, city, department, user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def input_department_data(request):
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    department_data = request.POST.get("department_data", "").encode("utf-8")
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not department_data.decode("utf-8") or not province.decode("utf-8") or not user_acc.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_update_depatment_data(department_data, province, city, department, user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')


@csrf_exempt
def delete_user_data(request):  #删除用户
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    user_list = request.POST.get("user_list", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_list.decode("utf-8") or not user_position_status:
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_delete_user_data(user_list)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def delete_key_data(request):   #删除关键字
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    key_list = request.POST.get("key_list", "").encode("utf-8")
    user_acc = request.POST.get("user_acc", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not key_list.decode("utf-8") or not user_position_status:
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_delete_key_data(key_list, user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def delete_department_data(request):   #删除部门
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    department_list = request.POST.get("department_list", "").encode("utf-8")
    user_acc = request.POST.get("user_acc", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not department_list.decode("utf-8") or not user_position_status:
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_delete_department_data(department_list, user_acc)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def get_user_error_bytime(request):    #按时间获取用户异常数据
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    keyclass = request.POST.get("keyclass", "").encode("utf-8")
    startTime = request.POST.get("startTime", "").encode("utf-8")
    endTime = request.POST.get("endTime", "").encode("utf-8")
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    status = request.POST.get("status", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_acc.decode("utf-8") or not page.decode("utf-8") or not status.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["error_data"] = BLL_get_dep_user_error_bytime(keyclass,startTime,endTime,user_acc, page, status, province, city, department)
    ret["count"] = len(BLL_get_dep_user_error_bytime(keyclass,startTime,endTime,user_acc, "0".encode("utf-8"), status, province, city, department))
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def get_user_error_byperson(request):    #按责任人获取用户异常数据
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    keyclass = request.POST.get("keyclass", "").encode("utf-8")
    personName = request.POST.get("personName", "").encode("utf-8")
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    status = request.POST.get("status", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_acc.decode("utf-8") or not page.decode("utf-8") or not status.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["error_data"] = BLL_get_dep_user_error_byperson(keyclass,personName,user_acc, page, status, province, city, department)
    ret["count"] = len(BLL_get_dep_user_error_byperson(keyclass,personName,user_acc, "0".encode("utf-8"), status, province, city, department))
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def del_user_error(request):    #删除报警记录
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    secretId = request.POST.get("secretId", "").encode("utf-8")
    if not secretId.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = BLL_del_user_error(secretId)
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def get_dep_count(request):    #获取用户异常统计
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    province = request.POST.get("province", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    errStatus = request.POST.get("errStatus", "").encode("utf-8")
    if not province.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["error_data"] = BLL_get_dep_count(province,page,errStatus)
    ret["count"] = len(BLL_get_dep_count(province,0,errStatus))
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def import_excel(request):
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')
    print(request.FILES)
    file_data = request.FILES['choosefile']
    province = request.POST.get("province", "")
    file_path = EXCEL_PATH
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    full_path = os.path.join(file_path, file_data.name)
    print(full_path)
    try:
        fw = open(full_path, 'wb+')
    except:
        ret = False
        return HttpResponse(json.dumps(ret), content_type='application/json')
    for fd in file_data:
        fw.write(fd)
    fw.close()
    if not os.path.exists(full_path):
        ret = False
        return HttpResponse(json.dumps(ret), content_type='application/json')
    excl_data = readExcl.excel_table_byindex(full_path)
    if excl_data == False:
        return HttpResponse(json.dumps(excl_data), content_type='application/json')
    ret = BLL_import_excel_inf(excl_data, province)
    if ret == False:
        return HttpResponse(json.dumps(ret), content_type='application/json')
    else:
        return HttpResponse(json.dumps(ret), content_type='application/json')

#获取扫描文件
@csrf_exempt
def get_scan_file_bytime(request):
    province = request.POST.get("province","").encode("utf-8")
    city = request.POST.get("city","").encode("utf-8")
    department = request.POST.get("department","").encode("utf-8")
    userAcc = request.POST.get("userAcc","").encode("utf-8")
    page = request.POST.get("page","").encode("utf-8")
    if not province.decode("utf-8") or not userAcc.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8") or not page.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')
    ret = {}
    ret["file"] = select_scan_file_bytime(province, city, department, userAcc, page)
    ret["count"] = len(select_scan_file_bytime(province, city, department, userAcc,"0".encode("utf-8")))
    if ret["file"] == False:
        return HttpResponse(json.dumps(False), content_type='application/json')
    return HttpResponse(json.dumps(ret), content_type='application/json')

def download_excel_file(request):
    filename = request.GET.get('file_name', '').encode("utf-8")
    if filename.decode("utf-8") == "":
        request.session["status"] = ""
        return render_to_response("source404.html")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "programFile/userexcelfile/")
    if not os.path.exists(file_path):
        request.session["status"] = ""
        return render_to_response("source404.html")
    response = HttpResponse()
    response['Content-Disposition'] = ('attachment;filename=' + filename.decode("utf-8")).encode("utf-8")
    filename = filename.decode()
    file = os.path.join(file_path, filename)
    if not file:
        request.session["status"] = ""
        return render_to_response("source404.html")
    content = open(file, 'rb').read()
    response.write(content)
    try:
        return response
    except:
        return render_to_response("source404.html")

@csrf_exempt
def get_user_error_detail(request):    #按责任人获取用户异常数据
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    personName = request.POST.get("personName", "").encode("utf-8")
    user_acc = request.POST.get("userAcc", "").encode("utf-8")
    page = request.POST.get("page", "").encode("utf-8")
    status = request.POST.get("status", "").encode("utf-8")
    province = request.POST.get("province", "").encode("utf-8")
    city = request.POST.get("city", "").encode("utf-8")
    department = request.POST.get("department", "").encode("utf-8")
    user_position_status = request.session.get("status", "")
    if not user_acc.decode("utf-8") or not page.decode("utf-8") or not status.decode("utf-8") or not province.decode("utf-8") or not city.decode("utf-8") or not department.decode("utf-8"):
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["error_data"] = BLL_get_dep_user_error_detail(personName,user_acc, page, status, province, city, department)
    ret["count"] = len(BLL_get_dep_user_error_detail(personName,user_acc, "0".encode("utf-8"), status, province, city, department))
    return HttpResponse(json.dumps(ret), content_type='application/json')

@csrf_exempt
def get_grant_data(request):    #按责任人获取用户异常数据
    ret = {}
    if not request.is_ajax() and request.method != "POST":
        return HttpResponse(json.dumps(False), content_type='application/json')

    ret["ret_ukey"] = BLL_get_ukey_info()
    return HttpResponse(json.dumps(ret), content_type='application/json')