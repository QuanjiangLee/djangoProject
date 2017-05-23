#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 获取用户数据
@time: 2017-1-14
'''

from DAL.select import DAL_get_user_login, DAL_get_dep_inf, DAL_get_dep_user_count, DAL_get_dep_user_error, get_province_DAL
from DAL.select import get_department_DAL, get_city_DAL, DAL_get_user_data, DAL_get_user_conn_data, select_scan_file_DAL
from DAL.select import DAL_get_user_name, DAL_select_key, DAL_get_file_data, DAL_get_deprtment_data,DAL_get_file_password
from DAL.select import DALGetKeyCount,DAL_get_dep_selfcheck_data,DAL_get_selfcheck_data,DAL_get_dep_user_error_byperson
from DAL.select import DAL_get_user_data_select,DAL_get_user_key_select,DAL_get_dep_user_error_bytime,DAL_get_selfcheck_count_data
from DAL.select import DAL_get_dep_count,select_scan_file_bytime_DAL,DAL_get_dep_user_error_detail

#获取用户登陆数据
def get_user_login(userName, passwd):
    ret = DAL_get_user_login(userName, passwd)
    return ret

#获取用户部门信息
def BLL_get_dep_inf(user_acc):
    ret_dpt = DAL_get_dep_inf(user_acc)
    ret = {}
    if len(ret_dpt) > 0:
        if int(ret_dpt[0][3]) != 0:
            ret["province"] = ret_dpt[0][0].encode("utf-8")
            ret["city"] = ret_dpt[0][1].encode("utf-8")
            ret["departmentName"] = ret_dpt[0][2].encode("utf-8")
            ret["userPositionStatus"] = ret_dpt[0][3]
            ret["userName"] = ret_dpt[0][4].encode("utf-8")
        else:
            ret["province"] = None
            ret["city"] = None
            ret["departmentName"] = None
            ret["userPositionStatus"] = ret_dpt[0][3]
            ret["userName"] = ret_dpt[0][4].encode("utf-8")
    return ret

def oprate_department_data(data):
    department_data={}
    for i in data:
        if i[1] == 0:
            department_data[i[0]] = [i[0]]
            for j in data:
                if j[0].find(i[0]) >= 0 and j != i:
                    department_data[i[0]].append(j[0])
    return department_data

def BLL_get_deprtment_data(province, city, department, page):
    page = int(page.decode("utf-8")) - 1

    if province.decode("utf-8") == u"一级部门":
        province = None
    if city.decode("utf-8") == u"二级部门":
        city = None
    if department.decode("utf-8") == u"三级部门":
        department = None
    ret_data = DAL_get_deprtment_data(province, city, department, page)
    if len(ret_data) == 0:
        return []
    ret_list = []
    for index in ret_data:
        ret_dir = {}
        ret_dir["departmentId"] = index[0]
        ret_dir["departmentName"] = index[1]
        ret_dir["createTime"] = str(index[2])
        ret_dir["createUser"] = index[3]
        ret_dir["province"] = index[4]
        ret_dir["city"] = index[5]
        ret_list.append(ret_dir)
    return ret_list

#获取部门信息
def BLL_get_dep_data(user_acc, province, city):
    dep_data = BLL_get_dep_inf(user_acc)
    if len(dep_data) == 0:
        return False
    if province.decode("utf-8") == "none":
        province = None
    if city.decode("utf-8") == "none":
        city = None
    if dep_data["province"] == "一级部门".encode("utf-8"):  #超高级超管
        ret_province = get_province_DAL()
        if len(ret_province) == 0:
            return {}
        ret_city = get_city_DAL(province)

        if len(ret_city) == 0:
            return {}
        if city == None:
            ret_department = get_department_DAL(ret_city[0][0].encode("utf-8"), province)
        else:
            ret_department = get_department_DAL(city, province)
        if len(ret_department) == 0:
            return {}

        province_data=[]
        city_data=[]

        for i in ret_province:
            province_data.append(i[0])

        for i in ret_city:
            city_data.append(i[0])

        ret_department_data = oprate_department_data(ret_department)
        ret_data = {"province": province_data, "city": city_data, "department": ret_department_data}
        return ret_data

    else:  #非超高级超管
        ret_department = None
        ret_city = get_city_DAL(province)
        if len(ret_city) == 0:
            return {}
        if city == None:
            ret_department = get_department_DAL(ret_city[0][0].encode("utf-8"), province, None)
        else:
            ret_department = get_department_DAL(city, province, None)
        if len(ret_department) == 0:
            return {}

        city_data=[]
        for i in ret_city:
            city_data.append(i[0])

        ret_department_data = oprate_department_data(ret_department)
        ret_data = {"province": [province.decode("utf-8"),], "city": city_data, "department": ret_department_data}
        return ret_data



'''
def BLL_get_dep_user_count(user_acc):    #获取部门违规统计
    dep_data = BLL_get_dep_inf(user_acc)
    ret = []
    if len(dep_data) == 0:
        return False
    ret_count = DAL_get_dep_user_count(dep_data["province"], dep_data["city"], dep_data["departmentName"])
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["department"] = index[0]
            dict["userNo"] = index[1]
            dict["userName"] = index[2]
            dict["hostMAC"] = index[3]
            dict["ip"] = index[4]
            dict["count"] = index[5]
            dict["time"] = index[6]
            ret.append(dict)
    return ret
'''
def BLL_get_dep_user_count(user_acc,province,city,department,page,errStatus):    #获取部门违规统计
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page)-1
    ret = []
    if len(dep_data) == 0:
        return False
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")
    print(province.decode('utf-8'),city.decode('utf-8'),department.decode('utf-8'))'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if int(user_position_status) == 2:
        if len(dep_data) == 0:
            return ret
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_count(province, city, None,page,errStatus)
        else:
            ret_count = DAL_get_dep_user_count(province, city, department,page,errStatus)
    elif int(user_position_status) == 1:
        ret_count = DAL_get_dep_user_count(province, city, department,page)
    #print(dep_data["province"].decode('utf-8'), dep_data["city"].decode('utf-8'), dep_data["departmentName"].decode('utf-8'),page)
    #ret_count = DAL_get_dep_user_count(dep_data["province"], dep_data["city"], dep_data["departmentName"])
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["department"] = index[0]
            dict["userNo"] = index[1]
            dict["userName"] = index[2]
            dict["hostMAC"] = index[3]
            dict["ip"] = index[4]
            dict["count"] = index[5]
            dict["errTime"] = index[6]
            dict["city"] = index[7]
            dict["province"] = index[8]
            ret.append(dict)
    return ret

 #获取部门违规数据
def BLL_get_dep_user_error(keyclass,user_acc, page, status, province, city, department):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page.decode("utf-8"))-1
    ret_count = ()
    dep_data = BLL_get_dep_inf(user_acc)
    ret = []
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if keyclass.decode("utf-8") == "所有":
        keyclass = " and keyWords like '%%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "严重":
        keyclass = " and keyWords like '%级别:0%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "重要":
        keyclass = " and keyWords like '%级别:1%' and keyWords not like '%级别:0%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "一般":
        keyclass = " and keyWords like '%级别:2%' and keyWords not like '%级别:0%' and keyWords not like '%级别:1%' ".encode("utf-8")
    '''if keyclass.decode("utf-8") == "所有":
        keyclass = "(级别:\"+\"?".encode("utf-8")
    elif keyclass.decode("utf-8") == "严重":
        keyclass = "(级别:0".encode("utf-8")
    elif keyclass.decode("utf-8") == "重要":
        keyclass = "(级别:1".encode("utf-8")
    elif keyclass.decode("utf-8") == "一般":
        keyclass = "(级别:2".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if int(user_position_status) == 1:
        if len(dep_data) == 0:
            return ret
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error(keyclass,province, city, None, page, status, True)
        else:
            ret_count = DAL_get_dep_user_error(keyclass,province, city, department, page, status, False)
    elif int(user_position_status) == 2:
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error(keyclass,province, city, None, page, status, True)
        else:
            ret_count = DAL_get_dep_user_error(keyclass,province, city, department, page, status, False)
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["userName"] = index[0]
            dict["errId"] = index[1]
            dict["errTime"] = index[2]
            dict["errOprate"] = index[3]
            dict["fileName"] = index[4]
            dict["fileHash"] = index[5]
            dict["keyWords"] = index[6]
            dict["ipAddr"] = index[7]
            dict["hostMac"] = index[8]
            dict["userNo"] = index[9]
            dict["keyExtend"] = index[10]
            dict["fileSize"] = index[11]
            dict["department"] = index[12]
            dict["city"] = index[13]
            ret.append(dict)
    return ret



def BLL_get_user_data(user_acc, province, city, department, page):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page)-1
    ret = []
    ret_user = 0
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")
    if int(user_position_status) == 1 and department.decode("utf-8") == u'三级部门':
        ret_user = DAL_get_user_data(dep_data["province"], dep_data["city"], dep_data["departmentName"], 0, page)
    elif int(user_position_status) == 1 and department.decode("utf-8") != u'三级部门':
        ret_user = DAL_get_user_data(province, city, department, 1, page)
    elif int(user_position_status) == 2 and department.decode("utf-8") == u'三级部门':
        ret_user = DAL_get_user_data(province, city, None, 0, page)
    elif int(user_position_status) == 2 and department.decode("utf-8") != u'三级部门':
        ret_user = DAL_get_user_data(province, city, department, 1, page)'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if department.decode("utf-8") == "三级部门":
        department = None
    ret_user = DAL_get_user_data(province, city, department, page)
    if len(ret_user) > 0:
        for index in ret_user:
            dict = {}
            dict["userNo"] = index[0]
            dict["userName"] = index[1]
            dict["userPosition"] = index[2]
            dict["macAddr"] = index[3]
            dict["ipAddr"] = index[4]
            ret.append(dict)
    return ret


def BLL_get_is_admin(user_no):
    dep_data = BLL_get_dep_inf(user_no)
    return dep_data["userPositionStatus"]

def BLL_get_user_key_select(user_acc, province, city, department, select_data,page):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page)-1
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    ret_key = []
    ret_data = []
    if user_position_status == 1:
        if department.decode("utf-8") != u'三级部门':
            ret_key = DAL_get_user_key_select(province, city, department,0,select_data,page)
        else:
            ret_key = DAL_get_user_key_select(dep_data["province"], dep_data["city"], dep_data["departmentName"], 1,select_data, page)
    elif user_position_status == 2:
        ret_key = DAL_get_user_key_select(province, city, department, 0,select_data, page)
    for index in ret_key:
        ret_dic = {}
        ret_dic["keyword"] = index[0]
        ret_dic["keyLever"] = index[1]
        ret_dic["keyId"] = index[2]
        ret_dic["isUpdate"] = 0
        if user_acc.decode("utf-8") == index[3]:
            ret_dic["isUpdate"] = 1

        ret_data.append(ret_dic)

    return ret_data

def BLL_get_user_data_select(user_acc, province, city, department, select_data,page):
    dep_data = BLL_get_dep_inf(user_acc)
    ret = []
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    user_position_status = dep_data["userPositionStatus"]
    page = int(page)-1
    if int(user_position_status) == 1 and department.decode("utf-8") == u"三级部门":
        ret_user_No = DAL_get_user_data_select(province, city, None, select_data, 1,page)
    if int(user_position_status) == 1 and department.decode("utf-8") != u"三级部门":
        ret_user_No = DAL_get_user_data_select(province, city, department, select_data, 0,page)
    if int(user_position_status) == 2 and department.decode("utf-8") == u"三级部门":
        ret_user_No = DAL_get_user_data_select(province, city, None, select_data, 0,page)
    if int(user_position_status) == 2 and department.decode("utf-8") != u"三级部门":
        ret_user_No = DAL_get_user_data_select(province, city, department, select_data, 0,page)
    if len(ret_user_No) > 0:
        for index in ret_user_No:
            dict = {}
            dict["userNo"] = index[0]
            dict["userName"] = index[1]
            dict["userPosition"] = index[2]
            dict["macAddr"] = index[3]
            dict["ipAddr"] = index[4]
            ret.append(dict)
    return ret

def get_user_name(user_no):
    ret_user_name = DAL_get_user_name(user_no)
    if len(ret_user_name) > 0:
        return ret_user_name[0][0]


def BLL_get_user_conn_data(user_acc, province, city, department, page,select_status):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page)-1
    ret = []
    ret_user = 0
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if int(user_position_status) == 1 and department.decode("utf-8") == u'三级部门':
        ret_user = DAL_get_user_conn_data(select_status,dep_data["province"], dep_data["city"], dep_data["departmentName"], 0, page)
    elif int(user_position_status) == 1 and department.decode("utf-8") != u'三级部门':
        ret_user = DAL_get_user_conn_data(select_status,province, city, department, 1, page)
    elif int(user_position_status) == 2 and department.decode("utf-8") == u'三级部门':
        ret_user = DAL_get_user_conn_data(select_status,province, city, None, 0, page)
    elif int(user_position_status) == 2 and department.decode("utf-8") != u'三级部门':
        ret_user = DAL_get_user_conn_data(select_status,province, city, department, 1, page)
    if len(ret_user) > 0:
        for index in ret_user:
            dict = {}
            dict["userNo"] = index[0]
            dict["userName"] = index[1]
            dict["loginStatus"] = index[2]
            dict["userNetStatus"] = index[3]
            dict["userScanStatus"] = index[4]
            dict["ipAddr"] = index[5]
            dict["macAddr"] = index[6]
            ret.append(dict)
    return ret

def select_scan_file(scanTime,province, city, department, userAcc, page):
    '''dep_data = BLL_get_dep_inf(userAcc)
    user_position_status = dep_data["userPositionStatus"]'''
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    page = int(page.decode("utf-8"))-1
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if department.decode("utf-8") == "三级部门":
        department = None
       # page = int(page.decode("utf-8"))-1
    '''if user_position_status == 1 and department.decode("utf-8") == u'三级部门':
        ret = select_scan_file_DAL(scanTime,province, city, None, 1,  page)
    elif int(user_position_status) == 1 and department.decode("utf-8") != u'三级部门':
        ret = select_scan_file_DAL(scanTime,province, city, department, 0, page)
    elif int(user_position_status) == 2 and department.decode("utf-8") == u'三级部门':
        ret = select_scan_file_DAL(scanTime,province, city, None, 0, page)
    elif int(user_position_status) == 2 and department.decode("utf-8") != u'三级部门':
        ret = select_scan_file_DAL(scanTime,province, city, department, 1, page)'''
    ret = select_scan_file_DAL(userAcc,scanTime,province, city, department, 1, page)
    ret_data = []
    if len(ret) == 0:
        return ret_data

    for i in ret:
        retDir = {}
        retDir["fileName"] = i[0]
        retDir["filePath"] = i[1]
        retDir["keywords"] = i[2]
        retDir["scanTime"] = str(i[3])
        retDir["keyExtend"] = i[4]
        retDir["userName"] = i[5]
        retDir["userNo"] = i[6]
        retDir["departmentName"] = i[7]
        retDir["city"] = i[8]
        ret_data.append(retDir)

    return ret_data


def get_file_data(errId):
    file_data = DAL_get_file_data(errId)
    if len(file_data) <= 0:
        return False
    ret = {}
    ret["file_hash"] = file_data[0][0]
    ret["file_name"] = file_data[0][1]
    ret["file_path"] = file_data[0][2]
    return ret



def BLL_select_key(user_acc, province, city, department, page):
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page.decode("utf-8"))-1
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    ret_key = []
    ret_data = []
    if user_position_status == 1:
        if department.decode("utf-8") != u'三级部门':
            ret_key = DAL_select_key(province, city, department,0, page)
        else:
            ret_key = DAL_select_key(dep_data["province"], dep_data["city"], dep_data["departmentName"], 1, page)
    elif user_position_status == 2:
        ret_key = DAL_select_key(province, city, department, 0, page)
    for index in ret_key:
        ret_dic = {}
        ret_dic["keyword"] = index[0]
        ret_dic["keyLever"] = index[1]
        ret_dic["keyId"] = index[2]
        ret_dic["isUpdate"] = 0
        if user_acc.decode("utf-8") == index[3]:
            ret_dic["isUpdate"] = 1

        ret_data.append(ret_dic)

    return ret_data

 #获取关键字条数
def getKeyCount(province, city, department):
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    ret = DALGetKeyCount(province, city, department)
    return ret[0][0]

#   获取用户自查基本信息
def BLL_get_selfcheck_data(userNo):
    ret_count = ()
    ret = []
    ret_count = DAL_get_selfcheck_data(userNo)
    if(len(ret_count)) > 0:
        for index in ret_count:
            dict = {}
            dict["userName"] = index[0]
            dict["loginStatus"] = index[1]
            dict["departmentName"] = index[2]
            dict["province"] = index[3]
            dict["city"] = index[4]
            dict["userIp"] = index[5]
            dict["hostMac"] = index[6]
            dict["userScanStatus"] = index[7]
            ret.append(dict)
    return ret

#   获取用户自查信息
def BLL_get_dep_selfcheck_data(userNo,page,scanTime):
    ret_count = ()
    ret = []
    page = int(page) - 1
    ret_count = DAL_get_dep_selfcheck_data(userNo,page,scanTime)
    if(len(ret_count))> 0:
        for index in ret_count:
            dict = {}
            dict["userIp"] = index[0]
            dict["hostMac"] = index[1]
            dict["userScanStatus"] = index[2]
            dict["usId"] = index[3]
            dict["fileName"] = index[4]
            dict["filePath"] = index[5]
            dict["keywords"] = index[6]
            dict["keyExtend"] = index[7]
            dict["scanTime"] = index[8]
            ret.append(dict)
    return ret

def BLL_get_dep_user_error_bytime(keyclass,startTime,endTime,user_acc, page, status, province, city, department):    #按时间段获取部门违规数据
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page.decode("utf-8"))-1
    ret_count = ()
    dep_data = BLL_get_dep_inf(user_acc)
    ret = []
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if keyclass.decode("utf-8") == "所有":
        keyclass = " and keyWords like '%%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "严重":
        keyclass = " and keyWords like '%级别:0%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "重要":
        keyclass = " and keyWords like '%级别:1%' and keyWords not like '%级别:0%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "一般":
        keyclass = " and keyWords like '%级别:2%' and keyWords not like '%级别:0%' and keyWords not like '%级别:1%' ".encode("utf-8")
    '''if keyclass.decode("utf-8") == "所有":
        keyclass = "(级别:\"+\"?".encode("utf-8")
    elif keyclass.decode("utf-8") == "严重":
        keyclass = "(级别:0".encode("utf-8")
    elif keyclass.decode("utf-8") == "重要":
        keyclass = "(级别:1".encode("utf-8")
    elif keyclass.decode("utf-8") == "一般":
        keyclass = "(级别:2".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if int(user_position_status) == 1:
        if len(dep_data) == 0:
            return ret
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error_bytime(keyclass,startTime,endTime,province, city, dep_data["departmentName"], page, status, True)
        else:
            ret_count = DAL_get_dep_user_error_bytime(keyclass,startTime,endTime,province, city, department, page, status, False)
    elif int(user_position_status) == 2:
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error_bytime(keyclass,startTime,endTime,province, city, None, page, status, True)
        else:
            ret_count = DAL_get_dep_user_error_bytime(keyclass,startTime,endTime,province, city, department, page, status, False)
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["userName"] = index[0]
            dict["errId"] = index[1]
            dict["errTime"] = index[2]
            dict["errOprate"] = index[3]
            dict["fileName"] = index[4]
            dict["fileHash"] = index[5]
            dict["keyWords"] = index[6]
            dict["ipAddr"] = index[7]
            dict["hostMac"] = index[8]
            dict["userNo"] = index[9]
            dict["keyExtend"] = index[10]
            dict["fileSize"] = index[11]
            dict["department"] = index[12]
            dict["city"] = index[13]
            ret.append(dict)
    return ret
	
def BLL_get_file_data(errId):
    file_data = DAL_get_file_data(errId)
    if len(file_data) <= 0:
        return False
    ret = {}
    ret["file_hash"] = file_data[0][0]
    ret["file_name"] = file_data[0][1]
    ret["file_path"] = file_data[0][2]
    return ret
	
def BLL_get_file_password(fileHash):
    ret = DAL_get_file_password(fileHash)
    if len(ret) > 0 and len(ret[0]) > 0:
        return ret[0][0]
    return False

def BLL_get_dep_user_error_byperson(keyclass,personName,user_acc, page, status, province, city, department):    #按责任人获取部门违规数据
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page.decode("utf-8"))-1
    ret_count = ()
    dep_data = BLL_get_dep_inf(user_acc)
    ret = []
    '''if province.decode("utf-8") == "所有省":
        province = "当前级别".encode("utf-8")
    if city.decode("utf-8") == "二级部门":
        city = "当前级别".encode("utf-8")'''
    if keyclass.decode("utf-8") == "所有":
        keyclass = " and keyWords like '%%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "严重":
        keyclass = " and keyWords like '%级别:0%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "重要":
        keyclass = " and keyWords like '%级别:1%' and keyWords not like '%级别:0%' ".encode("utf-8")
    elif keyclass.decode("utf-8") == "一般":
        keyclass = " and keyWords like '%级别:2%' and keyWords not like '%级别:0%' and keyWords not like '%级别:1%' ".encode("utf-8")
    '''if keyclass.decode("utf-8") == "所有":
        keyclass = "(级别:\"+\"?".encode("utf-8")
    elif keyclass.decode("utf-8") == "严重":
        keyclass = "(级别:0".encode("utf-8")
    elif keyclass.decode("utf-8") == "重要":
        keyclass = "(级别:1".encode("utf-8")
    elif keyclass.decode("utf-8") == "一般":
        keyclass = "(级别:2".encode("utf-8")'''
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if int(user_position_status) == 1:
        if len(dep_data) == 0:
            return ret
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error_byperson(keyclass,personName,province, city, dep_data["departmentName"], page, status, True)
        else:
            ret_count = DAL_get_dep_user_error_byperson(keyclass,personName,province, city, department, page, status, False)
    elif int(user_position_status) == 2:
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error_byperson(keyclass,personName,province, city, None, page, status, True)
        else:
            ret_count = DAL_get_dep_user_error_byperson(keyclass,personName,province, city, department, page, status, False)
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["userName"] = index[0]
            dict["errId"] = index[1]
            dict["errTime"] = index[2]
            dict["errOprate"] = index[3]
            dict["fileName"] = index[4]
            dict["fileHash"] = index[5]
            dict["keyWords"] = index[6]
            dict["ipAddr"] = index[7]
            dict["hostMac"] = index[8]
            dict["userNo"] = index[9]
            dict["keyExtend"] = index[10]
            dict["fileSize"] = index[11]
            dict["department"] = index[12]
            dict["city"] = index[13]
            ret.append(dict)
    return ret

#   获取用户自查总数信息
def BLL_get_dep_selfcheck_count_data(userNo,page):
    ret_count = ()
    ret = []
    page = int(page) - 1
    ret_count = DAL_get_selfcheck_count_data(userNo,page)
    if(len(ret_count))> 0:
        for index in ret_count:
            dict = {}
            dict["scanTime"] = index[0]
            dict["scanCount"] = index[1]
            ret.append(dict)
    return ret
	
def BLL_get_dep_count(province,page,errStatus):    #获取二级部门违规统计
    page = int(page)-1
    ret = []
    if province.decode("utf-8") == "一级部门":
        province = None
    ret_count = DAL_get_dep_count(province,page,errStatus)
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["province"] = index[0]
            dict["city"] = index[1]
            dict["count"] = index[2]
            ret.append(dict)
    return ret
	
def select_scan_file_bytime(province, city, department, userAcc, page):
    page = int(page.decode("utf-8"))-1
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if department.decode("utf-8") == "三级部门":
        department = None
    ret = select_scan_file_bytime_DAL(province, city, department, 1,  page)

    ret_data = []
    if len(ret) == 0:
        return ret_data

    for i in ret:
        retDir = {}
        retDir["scanTime"] = str(i[0])
        retDir["userName"] = i[1]
        retDir["userNo"] = i[2]
        retDir["departmentName"] = i[3]
        retDir["city"] = i[4]
        retDir["timecount"] = i[5]
        ret_data.append(retDir)

    return ret_data

def BLL_get_dep_user_error_detail(personName,user_acc, page, status, province, city, department):    #按责任人获取部门违规数据
    dep_data = BLL_get_dep_inf(user_acc)
    user_position_status = dep_data["userPositionStatus"]
    page = int(page.decode("utf-8"))-1
    ret_count = ()
    dep_data = BLL_get_dep_inf(user_acc)
    ret = []
    if province.decode("utf-8") == "一级部门":
        province = None
    if city.decode("utf-8") == "二级部门":
        city = None
    if int(user_position_status) == 1:
        if len(dep_data) == 0:
            return ret
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error_detail(personName,province, city, dep_data["departmentName"], page, status, True)
        else:
            ret_count = DAL_get_dep_user_error_detail(personName,province, city, department, page, status, False)
    elif int(user_position_status) == 2:
        if department.decode("utf-8") == u'三级部门':
            ret_count = DAL_get_dep_user_error_detail(personName,province, city, None, page, status, True)
        else:
            ret_count = DAL_get_dep_user_error_detail(personName,province, city, department, page, status, False)
    if len(ret_count) > 0:
        for index in ret_count:
            dict = {}
            dict["userName"] = index[0]
            dict["errId"] = index[1]
            dict["errTime"] = index[2]
            dict["errOprate"] = index[3]
            dict["fileName"] = index[4]
            dict["fileHash"] = index[5]
            dict["keyWords"] = index[6]
            dict["ipAddr"] = index[7]
            dict["hostMac"] = index[8]
            dict["userNo"] = index[9]
            dict["keyExtend"] = index[10]
            dict["fileSize"] = index[11]
            dict["department"] = index[12]
            dict["city"] = index[13]
            ret.append(dict)
    return ret
