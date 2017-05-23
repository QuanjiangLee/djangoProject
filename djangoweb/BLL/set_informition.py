#-*-coding:utf-8-*-
'''
@authon: jefferson
@function: 设置用户数据
@time: 2017-1-14
'''
import os
from  BLL.oprate import get_data_list, get_user_data
from DAL.update import DAL_update_user_error, DAL_update_user_inf, DAL_reset_userInf, DAL_update_user_net_status, DAL_update_user_scan_status
from DAL.update import DAL_update_department_inf
from DAL.update import DAL_update_key_inf
from DAL.insert import DAL_insert_user_inf, DAL_insert_key_inf, DAL_insert_dep_key, DAL_insert_department_inf
from DAL.select import DAL_get_userNo_count, get_dep_id_user_acc, get_dep_id, DAL_get_key_count, DAL_get_department_count
from DAL.delete import delete_computerInf_user_no, delete_fileUploadInf_user_no, delete_login_user_no,delete_userErrInf_user_no, delete_userInf_user_no
from DAL.delete import delete_dep_key, delete_key, delete_department,DAL_delete_selfcheck_data
from BLL.get_informition import BLL_get_dep_inf
from DAL.update import DAL_update_passwd
from DAL.delete import delete_selfcheck_userId,delete_userscan_userId,delete_computerInf_userId,delete_loginLog_userId
from DAL.delete import delete_userErrInf_userId,delete_loginInf_userId,delete_fileUploadInf_userId,delete_userInf_userId
from DAL.delete import DAL_deleteTimeSpan_selfcheck_data,DAL_del_user_error
from DAL.insert import DAL_insert_remote_record,DAL_insert_by_excel
from DAL.select import DAL_get_deprtment_data,DAL_get_file,DAL_find_filehash,DAL_from_fileupload, DAL_from_usererr
from DAL.delete import DAL_del_from_fileinf,DAL_del_from_usererr,DAL_del_from_upload

def BLL_update_user_error(secretId, status):
    secretId_list = get_data_list(secretId)
    ret = 0
    for secretId in secretId_list:
        ret += DAL_update_user_error(secretId, status)
    if ret > 0:
        return True
    else:
        return False


def BLL_delete_user_data(user_list):
    user_list = get_data_list(user_list)
    ret = 0
    for user_no in user_list:
        ret += delete_computerInf_user_no(user_no.encode("utf-8"))
        ret += delete_userErrInf_user_no(user_no.encode("utf-8"))
        ret += delete_login_user_no(user_no.encode("utf-8"))
        ret += delete_fileUploadInf_user_no(user_no.encode("utf-8"))
        ret += delete_userInf_user_no(user_no.encode("utf-8"))
    if ret > 0:
        return True
    else:
        return False


def BLL_delete_key_data(key_list, user_acc):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    key_list = get_data_list(key_list)
    ret = 0
    for keyId in key_list:
        ret += delete_dep_key(keyId.encode("utf-8"))
        ret += delete_key(keyId.encode("utf-8"))
    if ret > 0:
        return True
    else:
        return False

def BLL_delete_department_data(department_list, user_acc):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    department_list = get_data_list(department_list)
    ret = 0
    for department in department_list:
        ret += delete_loginLog_userId(department.encode("utf-8"))
        ret += delete_selfcheck_userId(department.encode("utf-8"))
        ret += delete_userscan_userId(department.encode("utf-8"))
        ret += delete_computerInf_userId(department.encode("utf-8"))
        ret += delete_userErrInf_userId(department.encode("utf-8"))
        ret += delete_loginInf_userId(department.encode("utf-8"))
        ret += delete_fileUploadInf_userId(department.encode("utf-8"))
        ret += delete_userInf_userId(department.encode("utf-8"))
        ret += delete_department(department.encode("utf-8"))
    if ret > 0:
        return True
    else:
        return False


def BLL_reset_user(user_no):
    ret = 0
    ret += delete_computerInf_user_no(user_no)
    ret += DAL_reset_userInf(user_no)
    if ret > 0:
        return True
    else:
        return False


def update_user_net_status(user_no, status):
    ret = DAL_update_user_net_status(user_no, status)
    if ret >= 0:
        ret = True
    else:
        ret = False
    return ret


def update_user_scan_status(user_no, status):
    ret = DAL_update_user_scan_status(user_no, status)
    if ret >= 0:
        ret = True
    else:
        ret = False
    return ret


def BLL_update_user_data(user_data, province, city, department, user_acc):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    secretId_list = get_user_data(user_data)
    ret = 0
    dep = None
    '''
    if province.decode("utf-8") == "一级部门":
        province = "一级部门".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "二级部门".encode("utf-8")
    '''
    if user_position_status == 1 and department.decode("utf-8") == u'三级部门':
        dep = get_dep_id_user_acc(user_acc)#departmentId
    elif user_position_status == 1 and department.decode("utf-8") != u'三级部门':
        dep = get_dep_id(province, city, department)
    elif user_position_status == 2 and department.decode("utf-8") == u'三级部门':
        dep = get_dep_id(province, city, department)
    elif user_position_status == 2 and department.decode("utf-8") != u'三级部门':
        dep = get_dep_id(province, city, department)
    for index in secretId_list:
        if index[1] =='increase':#增加
            ret_user = DAL_get_userNo_count(index[0][0])
            print(ret_user)
            if ret_user[0][0] > 0 :
                return False
            else:
                print(dep)
                if dep == None or len(dep) < 1:
                    return False
                ret += DAL_insert_user_inf(index[0][0], index[0][1], index[0][2], dep[0][0])
        elif index[1] =='update':#修改
            ret += DAL_update_user_inf(index[0][0], index[0][1], index[0][2])
    if ret > 0:
        return True
    else:
        return False


def BLL_update_depatment_data(department_data, province, city, department, user_acc):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    secretId_list = get_user_data(department_data)
    if secretId_list == False:
        return False
    ret = 0
    dep = None
    if city == None:
        city = "二级部门".encode("utf-8")
    if department == None:
        department = "三级部门".encode("utf-8")
    for index in secretId_list:
        if index[1] =='increase':
            if index[0][0] == "":
                index[0][0] = "三级部门"
            if index[0][3] == "":
                index[0][3] = "二级部门"
            ret_department = DAL_get_department_count(index[0][2], index[0][3],index[0][0])
            if ret_department[0][0] > 0 :
                return False
            else:
                create_user = dep_data["province"].decode("utf-8") + ":" + dep_data["city"].decode("utf-8") + ":" + dep_data["departmentName"].decode("utf-8") + ":" + dep_data["userName"].decode("utf-8")
                ret += DAL_insert_department_inf(index[0][0], index[0][1], index[0][2], index[0][3], 0, create_user)
        elif index[1] =='update':
            ret += DAL_update_department_inf(index[0][0], index[0][1])
    if ret > 0:
        return True
    else:
        return False


def BLL_update_key_data(key_data, province, city, department, user_acc,updata_status=0):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    secretId_list = get_user_data(key_data)#关键字信息
    print(secretId_list)
    ret = 0
    dep = None
    if province.decode("utf-8") == "一级部门":
        province = "一级部门".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "二级部门".encode("utf-8")
    if user_position_status == 1 and department.decode("utf-8") == u'三级部门':
        dep = get_dep_id_user_acc(user_acc)#departmentId
    elif user_position_status == 1 and department.decode("utf-8") != u'三级部门':
        dep = get_dep_id(province, city, department)
    if user_position_status == 1:  #普管
        for index in secretId_list:
            if index[1] =='increase':#增加关键字
                ret_key = DAL_get_key_count(updata_status,index[0][0],None, None)#根据关键字和创建它的人的职位
                if ret_key[0][0] > 0 :#是否存在这个关键字
                    ret_dep_key = DAL_get_key_count(updata_status,index[0][0],None, dep[0][0])
                    if ret_dep_key[0][0] > 0 :#根据关键字和部门查询
                        return False
                    else:
                        ret += DAL_insert_dep_key(ret_key[0][1], dep[0][0])
                else:
                    ret_key = DAL_get_key_count(updata_status,index[0][0],None, None, 0)
                    if ret_key[0][0] > 0:
                        return False
                    ret += DAL_insert_key_inf(index[0][0], index[0][1], user_acc)
                    ret_key = DAL_get_key_count(updata_status,index[0][0],None, None)
                    ret += DAL_insert_dep_key(ret_key[0][1], dep[0][0])
            elif index[1] =='update':#修改关键字
                ret_key = DAL_get_key_count(updata_status,index[0][1],None, None, 0)
                if ret_key[0][0] > 0:#关键字存在
                    ret_keyLever = DAL_get_key_count(1, index[0][1],index[0][2], None, 0)
                    if ret_keyLever[0][0] > 0:
                        return False
                ret_key = DAL_get_key_count(updata_status,index[0][1],None, None)
                if ret_key[0][0] > 0:
                    ret_keyLever = DAL_get_key_count(1, index[0][1],index[0][2], None, 0)
                    if ret_keyLever[0][0] > 0:
                        return False
                ret += DAL_update_key_inf(index[0][0], index[0][1], index[0][2])
    elif user_position_status == 2:  #超管
        for index in secretId_list:
            if index[1] =='increase':
                ret_key = DAL_get_key_count(updata_status,index[0][0],None, None, 0)
                if ret_key[0][0] > 0:
                    return False
                ret_key = DAL_get_key_count(updata_status,index[0][0],None, None, 1)
                if ret_key[0][0] > 0:
                    return False
                ret += DAL_insert_key_inf(index[0][0], index[0][1], user_acc, 0)
            elif index[1] =='update':
                ret_key = DAL_get_key_count(updata_status,index[0][1],None, None, 0)
                if ret_key[0][0] <= 0:
                    ret_key = DAL_get_key_count(updata_status,index[0][1],None,None)
                    if ret_key[0][0] > 0:
                        ret_keyLever = DAL_get_key_count(1, index[0][1], index[0][2], None, 0)
                        if ret_keyLever[0][0] > 0:
                            return False
                else:
                    ret_keyLever = DAL_get_key_count(1, index[0][1], index[0][2], None, 0)
                    if ret_keyLever[0][0] > 0:
                        return False
                ret += DAL_update_key_inf(index[0][0], index[0][1], index[0][2])
    if ret > 0:
        return True
    else:
        return False

#   删除用户自查信息
def BLL_delete_selfcheck_data(usId):
    ret = 0
    ret = DAL_delete_selfcheck_data(usId)
    if ret > 0:
        return True
    else:
        return False
		
def BLL_set_newpasswd(user_acc,passwd):
    ret = 0
    ret = DAL_update_passwd(user_acc,passwd)
    if ret > 0:
        return True
    else:
        return False
		
def BLL_delete_mulrecord_data(record_list, user_acc):
    dep_data = BLL_get_dep_inf(user_acc)
    record_list = get_data_list(record_list)
    ret = 0
    for usId in record_list:
        print("haifuhwfuhfkvuidsfhldshfkdfjhgfjdh@@@@@@@@")
        print(int(usId))
        ret += DAL_delete_selfcheck_data(usId.encode("utf-8"))
    if ret > 0:
        return True
    else:
        return False
		
def BLL_deleteTimeSpan_data(record_list, user_acc):
    dep_data = BLL_get_dep_inf(user_acc)
    record_list = get_data_list(record_list)
    ret = 0
    for scanTime in record_list:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(scanTime)
        ret += DAL_deleteTimeSpan_selfcheck_data(scanTime.encode("utf-8"))
    if ret > 0:
        return True
    else:
        return False
		
def BLL_del_user_error(secretId):
    secretId_list = get_data_list(secretId)
    ret = 0
    for secretId in secretId_list:
        ret += DAL_del_user_error(secretId)
    if ret > 0:
        return True
    else:
        return False

def BLL_insert_remote_record(send_no, receive_no, comm, send_time, send_status):
    DAL_insert_remote_record(send_no, receive_no, comm, send_time, send_status)


def BLL_import_excel_inf(data, province):
    if not isinstance(data, list) or len(data) == 0:
        return False
    for index in data:
        keys = index.keys()
        if not "用户编号" in keys or not "用户名" in keys or not "二级部门" in keys or not "三级部门" in keys:
            return False
        else:
            ret = DAL_get_deprtment_data(province.encode("utf-8"), index["二级部门"].encode("utf-8"), index["三级部门"].encode("utf-8"))
            if len(ret) == 0:
                return False
            else:
                department_id = ret[0][0]
                ret_user = DAL_get_userNo_count(index["用户编号"])
                if ret_user[0][0] > 0:
                    return False
                DAL_insert_by_excel(index["用户编号"], index["用户名"], department_id)
    return True

def BLL_del_not_exist_file():
    ret_path = []
    ret_name = []
    ret_count = DAL_get_file()
    if len(ret_count) > 0:
        for index in ret_count:
            file_path = os.path.join(index[0], index[1])
            if not os.path.exists(file_path):
                ret_path.append(file_path)
                ret_name.append(index[1])
    print("[不存在的文件名]:",len(ret_path))
    ret_hash = []
    for index in ret_name: #拿到不存在的文件的哈希
        ret_hash.append(DAL_find_filehash(index)[0][0])
    for index in ret_hash:
        ret_from_fileupload = DAL_from_fileupload(index)
        ret_from_usererr = DAL_from_usererr(index)
        if len(ret_from_fileupload) > 0: #fileUploadInf表中有数据
            DAL_del_from_upload(index)
            DAL_del_from_fileinf(index)
        else:
            DAL_del_from_fileinf(index)
        if len(ret_from_usererr) > 0: #usererr表中有数据
            DAL_del_from_usererr(index)
            DAL_del_from_fileinf(index)
        else:
            DAL_del_from_fileinf(index)
