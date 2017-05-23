#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 在数据库查询数据
@time: 2017-1-13
'''

from DAL.DBMethods import DBMethods

#获取用户登陆数据
def DAL_get_user_login(userName, passwd):
    values = (userName.decode("utf-8"), passwd.decode("utf-8"))
    dbStr = "select Count(*), userPositionStatus from userInf where userNo='{0}' and userPasswd=password('{1}');"
    dbStr = dbStr.format( *values )
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_dep_user_count(province=None, city=None, department=None, page=0, errStatus=1, page_num=20,status=0):   #获取部门违规统计
    if province != None and city == None and department != None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d'),city,province"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf,fileInf,fileUploadInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId and fileInf.fileHash=userErrInf.fileHash and uploadTime=errTime"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and province='{1}' and departmentName like '{2}%' group by userInf.userId order by Count(*) desc "
        dbStr = dbStr.format(errStatus, province.decode("utf-8"), department.decode("utf-8"))
    if province == None and city == None and department == None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d'),city,province"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf,fileInf,fileUploadInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId and fileInf.fileHash=userErrInf.fileHash and uploadTime=errTime"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} group by userInf.userId order by Count(*) desc "
        dbStr = dbStr.format(errStatus)
    if province != None and city == None and department == None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d'),city,province"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf,fileInf,fileUploadInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId and fileInf.fileHash=userErrInf.fileHash and uploadTime=errTime"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and province='{1}' group by userInf.userId order by Count(*) desc "
        dbStr = dbStr.format(errStatus, province.decode("utf-8"))
    if province != None and city != None and department == None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d'),city,province"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf,fileInf,fileUploadInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId and fileInf.fileHash=userErrInf.fileHash and uploadTime=errTime"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and province='{1}' and city='{2}'  group by userInf.userId order by Count(*) desc "
        dbStr = dbStr.format(errStatus, province.decode("utf-8"), city.decode("utf-8"))
    if province != None and city != None and department != None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d'),city,province"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf,fileInf,fileUploadInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId and fileInf.fileHash=userErrInf.fileHash and uploadTime=errTime"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and province='{1}' and city='{2}' and departmentName like '{3}%' group by userInf.userId order by Count(*) desc "
        dbStr = dbStr.format(errStatus, province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
    if page != -1:
        dbStr += "limit {0},{1};"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


'''
def DAL_get_dep_user_count(province=None, city=None, department=None, err_status=2, page_num=12, page=0, status=0):   #获取部门违规统计
    if province == None and city == None and department == None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d')"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and to_days(now())=to_days(errTime) group by userInf.userId order by Count(*) desc limit {1}, {2};"
        dbStr = dbStr.format(err_status, int(page)*int(page_num), page_num)
    if province != None and city == None and department == None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d')"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and province='{1}' and to_days(now())=to_days(errTime) group by userInf.userId order by Count(*) desc limit {2}, {3};;"
        dbStr = dbStr.format(err_status, province.decode("utf-8"), int(page)*int(page_num), page_num)
    if province != None and city != None and department == None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d')"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and province='{1}' and city='{2}' and to_days(now())=to_days(errTime) group by userInf.userId order by Count(*) desc limit {3}, {4};"
        dbStr = dbStr.format(err_status, province.decode("utf-8"), city.decode("utf-8"), int(page)*int(page_num), page_num)
    if province != None and city != None and department != None:
        dbStr = "select departmentName, userNo, userName, hostMac, userIp, Count(*), DATE_FORMAT( errTime, '%Y-%m-%d')"
        dbStr += " from userInf, userErrInf, computerInf, departmentInf"
        dbStr += " where userInf.departmentId=departmentInf.departmentId"
        dbStr += " and userErrInf.userId=userInf.userId and computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} and province='{1}' and city='{2}' and departmentName like '{3}%' and to_days(now())=to_days(errTime) group by userInf.userId order by Count(*) desc limit {4}, {5};"
        dbStr = dbStr.format(err_status, province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"), int(page_num)*int(page), page_num)
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret
'''

#获取用户部门信息
def DAL_get_dep_inf(user_acc):
    dbStr = "select province, city, departmentName, userPositionStatus, userName"
    dbStr += " from departmentInf, userInf where userInf.departmentId=departmentInf.departmentId and userNo='{0}';"
    dbStr = dbStr.format(user_acc.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_deprtment_data(province, city, department, page=0, page_num=20):
    dbStr = ""
    if province == None:
        dbStr = "select departmentId, departmentName, createTime, createUser, province, city from departmentInf "
    elif city == None:
        if department == None:
            dbStr = "select departmentId, departmentName, createTime, createUser, province, city from departmentInf where province='{0}'"
            dbStr = dbStr.format(province.decode("utf-8"))
        else:
            dbStr = "select departmentId, departmentName, createTime, createUser, province, city from departmentInf where province='{0}' and departmentName like '{1}%'"
            dbStr = dbStr.format(province.decode("utf-8"),department.decode("utf-8"))
    elif department == None:
        dbStr = "select departmentId, departmentName, createTime, createUser, province, city from departmentInf where province='{0}' and city='{1}'"
        dbStr = dbStr.format(province.decode("utf-8"),city.decode("utf-8"))
    else:
        dbStr = "select departmentId, departmentName, createTime, createUser, province, city from departmentInf where province='{0}' and city='{1}' and departmentName like '{2}%'"
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
    if page > -1:
        dbStr += " limit {0}, {1};"
        dbStr = dbStr.format(int(page)*int(page_num), page_num)
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def get_department_DAL(city, province, department=None):
    '''if city.decode("utf-8") == u'二级部门':
        if department == None:
            dbStr = "select distinct departmentName, status from departmentInf where province='{0}';"
            dbStr = dbStr.format(province.decode("utf-8"))
        else:
            dbStr = "select distinct departmentName, status from departmentInf where province='{0}' and departmentName like '{1}%';"
            dbStr = dbStr.format(province.decode("utf-8"), department.decode("utf-8"))
    elif department != None:'''
    if department == None:
        dbStr = "select distinct departmentName, status from departmentInf where province='{0}' and city='{1}';"
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
    elif department.decode("utf-8") != u'三级部门':
        dbStr = "select distinct departmentName, status from departmentInf where province='{0}' and city='{1}' and departmentName like '{2}%';"
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
    else:
        dbStr = "select distinct departmentName, status from departmentInf where province='{0}' and city='{1}';"
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(dbStr)
    print("!!!!!!!!!!!!!!ddddddddddddddddd")
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    print(ret)
    print("ddddddddddddddddddddddddddddddd")
    return ret

def get_city_DAL(province):
    dbStr = "select distinct city from departmentInf where province='%s';" %(province.decode("utf-8"), )
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    print("ccccccccccccccccccccccccccccccccc")
    print(dbStr)
    print(ret);
    print("ccccccccccccccccccccccccccccccccc")
    return ret

def DAL_get_user_name(user_no):
    dbStr = "select userName from userInf where userNo='{0}';"
    dbStr = dbStr.format(user_no)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

def get_province_DAL():
    dbStr = "select distinct province from departmentInf;"
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    print("pppppppppppppppppppppppppppppppppp")
    print(dbStr)
    print(ret);
    print("pppppppppppppppppppppppppppppppppp")
    return ret

 #获取异常数据
def DAL_get_dep_user_error(keyclass,province, city, department, page, status, like, page_num=20):
    if province == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf,departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {1} and userStatus=1 and userInf.departmentId in'
        dbStr += '(select departmentId from departmentInf) order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        dbStr = dbStr.format(str(status.decode("utf-8")),keyclass.decode("utf-8"))
    elif province != None and city != None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf,departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {3} and userStatus=1 and userInf.departmentId in '
        dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}") order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        dbStr = dbStr.format(str(status.decode("utf-8")), province.decode("utf-8"), city.decode("utf-8"),keyclass.decode("utf-8"))
    elif province != None and city != None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf,departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {4} and userStatus=1 and userInf.departmentId in'
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName like "{3}%") order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName = "{3}") order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        dbStr = dbStr.format(str(status.decode("utf-8")), province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"),keyclass.decode("utf-8"))
    elif province != None and city == None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf,departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {3} and userStatus=1 and userInf.departmentId in'
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName like "{2}%") order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName = "{2}") order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        dbStr = dbStr.format(str(status.decode("utf-8")), province.decode("utf-8"), department.decode("utf-8"),keyclass.decode("utf-8"))
    elif province != None and city == None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf,departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {2} and userStatus=1 and userInf.departmentId in'
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" ) order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" ) order by DATE_FORMAT( errTime, "%Y-%m-%d %H:%i:%s") desc '
        dbStr = dbStr.format(str(status.decode("utf-8")), province.decode("utf-8"),keyclass.decode("utf-8"))
    if page != -1:
        dbStr += "limit {0},{1};"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print(dbStr)

    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_user_data( province, city, department, page, page_num=20):
    if province == None:
        dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
        dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId "
        dbStr += " and userStatus = 1 "
        dbStr += " order by userPositionStatus desc, registStatus desc"
    elif city == None:
        if department == None:
            dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
            dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId and province='{0}'"
            dbStr += " and userStatus = 1 "
            dbStr += " order by userPositionStatus desc, registStatus desc"
            dbStr = dbStr.format(province.decode("utf-8"))
        else:
            dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
            dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId and province='{0}'"
            dbStr += " and userStatus = 1 "
            dbStr += "and departmentName='{1}' order by userPositionStatus desc, registStatus desc"
            dbStr = dbStr.format(province.decode("utf-8"), department.decode("utf-8"))
    else:
        if department == None:
            dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
            dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId and province='{0}'"
            dbStr += "and city='{1}' and userStatus = 1 "
            dbStr += " order by userPositionStatus desc, registStatus desc"
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
        else:
            dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
            dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId and province='{0}'"
            dbStr += "and city='{1}' and userStatus = 1 "
            dbStr += "and departmentName='{2}' order by userPositionStatus desc, registStatus desc"
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
    if page != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


#按工号或姓名查找信息
def DAL_get_user_data_select( province, city, department, select_data, like,page,page_num=20):
    if province == None:
        dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
        dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId "
        dbStr += " and userStatus = 1 "
        dbStr += " and (userNo like '%{0}%' or userName like '%{0}%') order by userPositionStatus desc, registStatus desc"
        dbStr = dbStr.format(select_data.decode("utf-8").strip())
    elif city == None:
        dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
        dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId and province='{0}'"
        dbStr += " and userStatus = 1 "
        dbStr += " and (userNo like '%{1}%' or userName like '%{1}%') order by userPositionStatus desc, registStatus desc"
        dbStr = dbStr.format(province.decode("utf-8"), select_data.decode("utf-8").strip())
    elif department != None:
        dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
        dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId and province='{0}'"
        dbStr += "and city='{1}' and userStatus = 1 "
        if like == 1:
            dbStr += "and departmentName like '{2}%' and (userNo like '%{3}%' or userName like '%{3}%') order by userPositionStatus desc, registStatus desc"
        else:
            dbStr += "and departmentName='{2}' and (userNo like '%{3}%' or userName like '%{3}%') order by userPositionStatus desc, registStatus desc"
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"), select_data.decode("utf-8").strip())
    else:
            dbStr = "select userNo, userName, userPositionStatus, hostMac, userIp from departmentInf, userInf left join computerInf"
            dbStr +=" on computerInf.userId=userInf.userId where departmentInf.departmentId=userInf.departmentId and province='{0}'"
            dbStr += "and city='{1}' and userStatus = 1 "
            dbStr += "and (userNo like '%{2}%' or userName like '%{2}%') order by userPositionStatus desc, registStatus desc"
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), select_data.decode("utf-8").strip())
    if page != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))       
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_user_conn_data(select_status, province, city, department, status, page, page_num=20):
    if  select_status == '0':
        if province == None:
            dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
            dbStr += 'where userStatus=1 and loginStatus=0 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf)'
            dbStr += " order by userInf.userId desc"
        elif city == None:
            if department == None:
                dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
                dbStr += 'where userStatus=1 and loginStatus=0 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
                dbStr += ' where province="{0}")  order by userInf.userId desc'
                dbStr = dbStr.format(province.decode("utf-8"))
            else:
                dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
                dbStr += 'where userStatus=1 and loginStatus=0 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
                dbStr += ' where province="{0}"  '
                dbStr = dbStr.format(province.decode("utf-8"))
                if status == 0:
                    dbStr += "and departmentName like '{1}%') order by userInf.userId desc"
                else:
                    dbStr += "and departmentName='{1}') order by userInf.userId desc"
                dbStr = dbStr.format(province.decode("utf-8"), department.decode("utf-8"))
        elif department != None:
            dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
            dbStr += 'where userStatus=1 and loginStatus=0 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
            dbStr += ' where province="{0}" and city="{1}" '
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
            if status == 0:
                dbStr += "and departmentName like '{2}%') order by userInf.userId desc"
            else:
                dbStr += "and departmentName='{2}') order by userInf.userId desc"

            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
        else:
            dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
            dbStr += 'where userStatus=1 and loginStatus=0 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
            dbStr += ' where province="{0}" and city="{1}") '
            dbStr += "order by userInf.userId desc"
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
    else:
        if province == None:
            dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
            dbStr += 'where userStatus=1 and loginStatus=1 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf)'
            dbStr += " order by userInf.userId desc"
        elif city == None:
            if department == None:
                dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
                dbStr += 'where userStatus=1 and loginStatus=1 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
                dbStr += ' where province="{0}") '
                dbStr = dbStr.format(province.decode("utf-8"))
            else:
                dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
                dbStr += 'where userStatus=1 and loginStatus=1 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
                dbStr += ' where province="{0}" '
                dbStr = dbStr.format(province.decode("utf-8"))
                if status == 0:
                    dbStr += "and departmentName like '{1}%') order by userInf.userId desc"
                else:
                    dbStr += "and departmentName='{1}') order by userInf.userId desc"

                dbStr = dbStr.format(province.decode("utf-8"), department.decode("utf-8"))
        elif department != None:
            dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
            dbStr += 'where userStatus=1 and loginStatus=1 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
            dbStr += ' where province="{0}" and city="{1}" '
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
            if status == 0:
                dbStr += "and departmentName like '{2}%') order by userInf.userId desc"
            else:
                dbStr += "and departmentName='{2}') order by userInf.userId desc"

            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
        else:
            dbStr = 'select userNo, userName, loginStatus, userNetStatus, userScanStatus, userIp, hostMac from userInf, computerInf '
            dbStr += 'where userStatus=1 and loginStatus=1 and  computerInf.userId=userInf.userId and departmentId in (select departmentId from departmentInf'
            dbStr += ' where province="{0}" and city="{1}") '
            dbStr += "order by userInf.userId desc"
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
    if page != -1:
            dbStr += " limit {0}, {1}"
            dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_userNo_count(userNo):
    dbStr = "select count(*) from userInf where userNo='{0}';"
    dbStr = dbStr.format(userNo)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

def DAL_get_department_count(province, city, department):
    dbStr = "select count(*) from departmentInf where province='{0}' and province='{1}' and departmentName='{2}';"
    dbStr = dbStr.format(province, city, department)
    db = DBMethods()
    print(dbStr)
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_key_count(updata_status,key, keyLever,department, createUserStatus=None):
    if updata_status == 0:
        if department != None:
            dbStr = "select count(*) from keywordsInf, departmentKey where keywordsInf.keyId=departmentKey.keyId and keyword='{0}' "
            dbStr += " and departmentId={1};"
            dbStr = dbStr.format(key.strip(), department)
        else:
            if createUserStatus == None or createUserStatus == 1:
                dbStr = "select count(*), keyId from keywordsInf where keyword='{0}' and createUserStatus=1;"  #1：普管
            else:
                dbStr = "select count(*), keyId from keywordsInf where keyword='{0}' and createUserStatus=0;"  #0：超管
            dbStr = dbStr.format(key.strip())
    else:
        dbStr = "select count(*) from keywordsInf where keyword='{0}'and  keyLever={1} "
        dbStr = dbStr.format(key.strip(),keyLever)
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def get_dep_id_user_acc(user_acc):
    dbStr = "select departmentId from userInf where userNo='{0}';"
    dbStr = dbStr.format(user_acc.decode("utf-8"))
    db = DBMethods()
    print(dbStr)
    ret = db.selectMethods(dbStr)
    return ret

def get_dep_id(province, city, department):
    dbStr = "select departmentId from departmentInf where province='{0}' and city='{1}' and departmentName='{2}';"
    dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
    db = DBMethods()
    print(dbStr)
    ret = db.selectMethods(dbStr)
    return ret


def select_scan_file_DAL(userAcc,scanTime,province, city, department, like, page,  page_size=20):
    if province == None:
        dbStr = 'select fileName, filePath, keywords, scanTime, keyExtend, userName, userInf.userNo,departmentName,city from userScan, userInf,departmentInf where scanTime="{0}" and userInf.userNo="{1}" and userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf '
        dbStr += ')) order by scanTime desc, userInf.userId'
        dbStr = dbStr.format(scanTime.decode("utf-8"),userAcc.decode("utf-8"))
    elif city == None:
        dbStr = 'select fileName, filePath, keywords, scanTime, keyExtend, userName, userInf.userNo,departmentName,city from userScan, userInf,departmentInf where scanTime="{1}" and userInf.userNo="{2}" and userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf where province="{0}" '
        dbStr += ')) order by scanTime desc, userInf.userId'
        dbStr = dbStr.format(province.decode("utf-8"),scanTime.decode("utf-8"),userAcc.decode("utf-8"))
    elif department != None:
        dbStr = 'select fileName, filePath, keywords, scanTime, keyExtend, userName, userInf.userNo,departmentName,city from userScan, userInf,departmentInf where scanTime="{3}" and userInf.userNo="{4}" and userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf where province="{0}" '
        if like == 0:
            dbStr += 'and city="{1}" and departmentName="{2}")) order by scanTime desc, userInf.userId'
        else:
            dbStr += 'and city="{1}" and departmentName like "{2}%")) order by scanTime desc, userInf.userId'
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"),scanTime.decode("utf-8"),userAcc.decode("utf-8"))
    else:
        dbStr = 'select fileName, filePath, keywords, scanTime, keyExtend, userName, userInf.userNo,departmentName,city from userScan, userInf,departmentInf where scanTime="{2}" and userInf.userNo="{3}" and userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf where province="{0}" '
        dbStr += 'and city="{1}")) order by scanTime desc, userInf.userId'
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"),scanTime.decode("utf-8"),userAcc.decode("utf-8"))

    '''if page > 1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(page*page_size, page_size)'''
    if page != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page)*int(page_size)), str(page_size))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

def DAL_get_user_key_select(province, city, department,like_status,select_data,page_num,page_size=20):
    if province == None:
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 and keyword like "%{0}%" union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId  and keyword like "%{0}%" and departmentId in (select departmentId'
        dbStr+= ' from departmentInf) order by keyLever'
        dbStr = dbStr.format(select_data.decode("utf-8"))
    elif city == None:
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 and keyword  like "%{0}%" union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId and departmentId in (select departmentId'
        if like_status == 0:
            dbStr+= ' from departmentInf where province="{1}" and departmentName="{2}" and keyword like "%{3}%") order by keyLever'
            dbStr = dbStr.format(select_data.decode("utf-8"),province.decode("utf-8"), department.decode("utf-8"),select_data.decode("utf-8"))
        else:
            dbStr+= ' from departmentInf where province="{1}" and departmentName like "%{2}%" and keyword like "%{3}%") order by keyLever'
            dbStr = dbStr.format(select_data.decode("utf-8"),province.decode("utf-8"), department.decode("utf-8"),select_data.decode("utf-8"))
    elif department.decode("utf-8") != u'三级部门':
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 and keyword  like "%{0}%" union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId and departmentId in (select departmentId'
        if like_status == 0:
            dbStr+= ' from departmentInf where province="{1}" and city="{2}" and departmentName="{3}" and keyword like "%{4}%") order by keyLever'
            dbStr = dbStr.format(select_data.decode("utf-8"),province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"),select_data.decode("utf-8"))
        else:
            dbStr+= ' from departmentInf where province="{1}" and city="{2}" and departmentName like "%{3}%" and keyword like "%{4}%") order by keyLever'
            dbStr = dbStr.format(select_data.decode("utf-8"),province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"),select_data.decode("utf-8"))
    else:
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 and keyword like "%{0}%" union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId  and departmentId in (select departmentId'
        dbStr+= ' from departmentInf where province="{1}" and city="{2}" and keyword like "%{3}%") order by keyLever'
        dbStr = dbStr.format(select_data.decode("utf-8"),province.decode("utf-8"), city.decode("utf-8"),select_data.decode("utf-8"))
    if page_num != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page_num)*int(page_size)), str(page_size))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

def DAL_select_key(province, city, department, like_status, page_num = 0, page_size=20): #获取关键字信息
    if province == None:
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId and departmentId in (select departmentId'
        dbStr+= ' from departmentInf) order by keyLever'
    elif city == None:
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId and departmentId in (select departmentId'
        if like_status == 0:
            dbStr+= ' from departmentInf where province="{0}" and departmentName="{1}") order by keyLever'
            dbStr = dbStr.format(province.decode("utf-8"), department.decode("utf-8"))
        else:
            dbStr+= ' from departmentInf where province="{0}" and departmentName like "{1}%") order by keyLever'
            dbStr = dbStr.format(province.decode("utf-8"), department.decode("utf-8"))
    elif department.decode("utf-8") != u'三级部门':
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId and departmentId in (select departmentId'
        if like_status == 0:
            dbStr+= ' from departmentInf where province="{0}" and city="{1}" and departmentName="{2}") order by keyLever'
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
        else:
            dbStr+= ' from departmentInf where province="{0}" and city="{1}" and departmentName like "{2}%") order by keyLever'
            dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
    else:
        dbStr = 'select keyword, keyLever, keyId, createUserId from keywordsInf where createUserStatus=0 union'
        dbStr += ' select keyword, keyLever, keywordsInf.keyId, createUserId from keywordsInf, departmentKey'
        dbStr += ' where keywordsInf.keyId=departmentKey.keyId and departmentId in (select departmentId'
        dbStr+= ' from departmentInf where province="{0}" and city="{1}") order by keyLever'
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
    if page_num != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page_num)*int(page_size)), str(page_size))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_file_data(errId):
    dbStr = "select userErrInf.fileHash, fileLocalName, filePath from userErrInf, fileInf where userErrInf.fileHash=fileInf.fileHash and errId={0};"
    dbStr = dbStr.format(errId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


#获得关键字总条数
def DALGetKeyCount(province, city,department):
    #dbStr = 'select count(*) from keywordsInf'
    if province == None:
        dbStr = 'SELECT COUNT(*) FROM (SELECT  keyId FROM keywordsInf WHERE createUserStatus=0 UNION  SELECT keywordsInf.keyId FROM keywordsInf, departmentKey WHERE keywordsInf.keyId=departmentKey.keyId AND departmentId IN (SELECT departmentId FROM departmentInf )) AS countall'
    elif city == None:
        dbStr = 'SELECT COUNT(*) FROM (SELECT  keyId FROM keywordsInf WHERE createUserStatus=0 UNION  SELECT keywordsInf.keyId FROM keywordsInf, departmentKey WHERE keywordsInf.keyId=departmentKey.keyId AND departmentId IN (SELECT departmentId FROM departmentInf WHERE province="{0}" AND departmentName="{1}")) AS countall'
        dbStr = dbStr.format(province.decode("utf-8"),department.decode("utf-8"))
    elif department.decode("utf-8") == u'三级部门':
        dbStr = 'SELECT COUNT(*) FROM (SELECT  keyId FROM keywordsInf WHERE createUserStatus=0 UNION  SELECT keywordsInf.keyId FROM keywordsInf, departmentKey WHERE keywordsInf.keyId=departmentKey.keyId AND departmentId IN (SELECT departmentId FROM departmentInf WHERE province="{0}" AND city="{1}")) AS countall'
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
    else:
        dbStr = 'SELECT COUNT(*) FROM (SELECT  keyId FROM keywordsInf WHERE createUserStatus=0 UNION  SELECT keywordsInf.keyId FROM keywordsInf, departmentKey WHERE keywordsInf.keyId=departmentKey.keyId AND departmentId IN (SELECT departmentId FROM departmentInf WHERE province="{0}" AND city="{1}" AND departmentName="{2}")) AS countall'
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"),department.decode("utf-8"))
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

#获取用户自查基本信息
def DAL_get_selfcheck_data(userNo):
    dbStr = "select userName,loginStatus,departmentName,province,city,userIp,hostMac,userScanStatus" \
            " from departmentInf,userInf left join computerInf on userInf.userId=" \
            "computerInf.userId where userInf.departmentId=departmentInf.departmentId" \
            " and userInf.userNo='{0}'"
    dbStr = dbStr.format(str(userNo.decode("utf-8")))
    db = DBMethods()
    print(dbStr)
    ret = db.selectMethods(dbStr)
    return ret

#   获取用户自查信息
def DAL_get_dep_selfcheck_data(userNo,page,scanTime,page_num=20):
    dbStr = "SELECT userIp,hostMac,userScanStatus,usId,fileName,filePath,keywords,keyExtend,DATE_FORMAT(scanTime,'%H:%i:%s %Y-%m-%d')"
    dbStr += " FROM userInf,computerInf,selfCheck,departmentInf"
    dbStr += " WHERE departmentInf.departmentId=userInf.departmentId AND userInf.userId=computerInf.userId"
    dbStr += " AND userInf.userId=selfCheck.userId AND userInf.userNo='{0}' AND selfCheck.scanTime='{1}' ORDER BY scanTime desc "
    dbStr = dbStr.format(str(userNo.decode("utf-8")),str(scanTime.decode("utf-8")))
    if page != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    db = DBMethods()
    print(dbStr)
    ret = db.selectMethods(dbStr)
    return ret

def DAL_get_dep_user_error_bytime(keyclass,startTime,endTime,province, city, department, page, status, like, page_num=20):  #按日期获取异常数据
    if province == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf, fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {3} and userStatus=1 and (errTime  between  "{1}"  and  "{2}") and userInf.departmentId in '
        dbStr += '(select departmentId from departmentInf) order by errTime desc '
        dbStr = dbStr.format(str(status.decode("utf-8")),startTime.decode("utf-8") + " 00:00:00",endTime.decode("utf-8") + " 23:59:59",keyclass.decode("utf-8"))
    elif province != None and city != None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf, fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {5} and userStatus=1 and userInf.departmentId in '
        dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}") and (errTime  BETWEEN "{3}" AND "{4}") order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"), city.decode("utf-8"),startTime.decode("utf-8") + " 00:00:00",endTime.decode("utf-8") + " 23:59:59",keyclass.decode("utf-8")) 
    elif province != None and city != None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf, fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {6} and userStatus=1 and (errTime  between  "{4}"  and  "{5}") and userInf.departmentId in '
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName like "{3}%") order by errTime desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName = "{3}") order by errTime desc '
        dbStr = dbStr.format(str(status.decode("utf-8")), province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"),startTime.decode("utf-8") + " 00:00:00",endTime.decode("utf-8") + " 23:59:59",keyclass.decode("utf-8"))
    elif province != None and city == None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf, fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {5} and userStatus=1 and (errTime  between  "{3}"  and  "{4}") and userInf.departmentId in '
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName like "{2}%") order by errTime desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName = "{2}") order by errTime desc '
        dbStr = dbStr.format(str(status.decode("utf-8")), province.decode("utf-8"), department.decode("utf-8"),startTime.decode("utf-8") + " 00:00:00",endTime.decode("utf-8") + " 23:59:59",keyclass.decode("utf-8"))
    elif province != None and city == None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize ,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf, fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {4} and userStatus=1 and (errTime  between  "{2}"  and  "{3}") '
        dbStr = dbStr.format(str(status.decode("utf-8")), province.decode("utf-8"),startTime.decode("utf-8") + " 00:00:00",endTime.decode("utf-8") + " 23:59:59",keyclass.decode("utf-8"))
    if page != -1:
        dbStr += "limit {0},{1};"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print("[dbStr] %s" %(dbStr) )

    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret
	
def DAL_get_file_password(file_hash):
    values = (file_hash, )
    dbStr = "select filePasswd from fileInf where fileHash='%s';"%values
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret
	
def DAL_get_dep_user_error_byperson(keyclass,personName,province, city, department, page, status, like, page_num=20):  #按日期获取异常数据
    if province == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {2} and userStatus=1 and (userName LIKE "%{1}%" OR userNo LIKE "%{1}%") and userInf.departmentId in '
        dbStr += '(select departmentId from departmentInf) order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"),personName.decode("utf-8"),keyclass.decode("utf-8"))
    elif province != None and city != None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and fileInf.fileHash=userErrInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {4} and userStatus=1 and userInf.departmentId in '
        dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}") and (userName LIKE "%{3}%" OR userNo LIKE "%{3}%") order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"), city.decode("utf-8"),personName.decode("utf-8"),keyclass.decode("utf-8")) 
    elif province != None and city != None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {5} and userStatus=1 and (userName LIKE "%{4}%" OR userNo LIKE "%{4}%") and userInf.departmentId in '
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName like "{3}%") order by errTime desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName = "{3}") order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"),personName.decode("utf-8"),keyclass.decode("utf-8"))
    elif province != None and city == None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {4} and userStatus=1 and (userName LIKE "%{3}%" OR userNo LIKE "%{3}%") and userInf.departmentId in '
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName like "{2}%") order by errTime desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName = "{2}") order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"), department.decode("utf-8"),personName.decode("utf-8"),keyclass.decode("utf-8"))
    elif province != None and city == None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} {3} and userStatus=1 and (userName LIKE "%{2}%" OR userNo LIKE "%{2}%")'
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"),personName.decode("utf-8"),keyclass.decode("utf-8"))
    if page != -1:
        dbStr += "limit {0},{1};"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print("[dbStr] %s" %(dbStr) )


    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

	
#   获取用户自查时间信息
def DAL_get_selfcheck_count_data(userNo,page, page_num=20):
    dbStr = "SELECT DATE_FORMAT(scanTime,'%H:%i:%s %Y-%m-%d'), COUNT(*) "
    dbStr += " FROM userInf,computerInf,selfCheck,departmentInf"
    dbStr += " WHERE departmentInf.departmentId=userInf.departmentId AND userInf.userId=computerInf.userId"
    dbStr += " AND userInf.userId=selfCheck.userId AND userInf.userNo='{0}' GROUP BY selfCheck.scanTime ORDER BY scanTime DESC "
    dbStr = dbStr.format(str(userNo.decode("utf-8")))
    if page != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    db = DBMethods()
    print(dbStr)
    ret = db.selectMethods(dbStr)
    return ret
	
def DAL_get_dep_count(province, page=0, errStatus=1, page_num=20,status=0):   #获取二级部门违规统计
    if province == None:
        dbStr = "SELECT province,city, COUNT(*) "
        dbStr += " FROM userInf, userErrInf, computerInf, departmentInf,fileInf,fileUploadInf"
        dbStr += " WHERE userInf.departmentId=departmentInf.departmentId and fileInf.fileHash=userErrInf.fileHash AND uploadTime=errTime "
        dbStr += " AND userErrInf.userId=userInf.userId AND computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} AND city != '二级部门' GROUP BY departmentInf.province,departmentInf.city  ORDER BY COUNT(*) DESC "
        dbStr = dbStr.format(errStatus)
    else:
        dbStr = "SELECT province,city, COUNT(*) "
        dbStr += " FROM userInf, userErrInf, computerInf, departmentInf,fileInf,fileUploadInf"
        dbStr += " WHERE userInf.departmentId=departmentInf.departmentId and fileInf.fileHash=userErrInf.fileHash AND uploadTime=errTime "
        dbStr += " AND userErrInf.userId=userInf.userId AND computerInf.userId=userInf.userId"
        dbStr += " and errStatus={0} AND city != '二级部门' AND province='{1}' GROUP BY departmentInf.province,departmentInf.city  ORDER BY COUNT(*) DESC "
        dbStr = dbStr.format(errStatus, province.decode("utf-8"))
    if page != -1:
        dbStr += "limit {0},{1};"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret
	
def select_scan_file_bytime_DAL(province, city, department, like, page,  page_size=20):
    if province == None:
        dbStr = 'select scanTime, userName, userInf.userNo,departmentName,city,COUNT(*) from userScan, userInf,departmentInf where  userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf '
        dbStr += ')) GROUP BY scanTime  order by scanTime desc, userInf.userId'
    elif city == None:
        dbStr = 'select scanTime, userName, userInf.userNo,departmentName,city,COUNT(*) from userScan, userInf,departmentInf where userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf where province="{0}" '
        dbStr += ')) GROUP BY scanTime  order by scanTime desc, userInf.userId'
        dbStr = dbStr.format(province.decode("utf-8"))
    elif department != None:
        dbStr = 'select scanTime, userName, userInf.userNo,departmentName,city,COUNT(*) from userScan, userInf,departmentInf where  userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf where province="{0}" '
        if like == 0:
            dbStr += 'and city="{1}" and departmentName="{2}")) GROUP BY scanTime  order by scanTime desc, userInf.userId'
        else:
            dbStr += 'and city="{1}" and departmentName like "{2}%")) GROUP BY scanTime  order by scanTime desc, userInf.userId'
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"))
    else:
        dbStr = 'select scanTime, userName, userInf.userNo,departmentName,city,COUNT(*) from userScan, userInf,departmentInf where  userInf.departmentId=departmentInf.departmentId and userInf.userId=userScan.userId and userInf.userId in ('
        dbStr += 'select userId from userInf where departmentId in (select departmentId from departmentInf where province="{0}" '
        dbStr += 'and city="{1}")) GROUP BY scanTime  order by scanTime desc, userInf.userId'
        dbStr = dbStr.format(province.decode("utf-8"), city.decode("utf-8"))
    if page != -1:
        dbStr += " limit {0}, {1}"
        dbStr = dbStr.format(str(int(page)*int(page_size)), str(page_size))
    print(dbStr)
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_file():
    dbStr = "select filePath,fileLocalName from fileInf"
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret

def DAL_find_filehash(index):
    dbStr = "select fileHash from fileInf where fileLocalName='{0}'"
    db = DBMethods()
    dbStr = dbStr.format(index)
    ret = db.selectMethods(dbStr)
    return ret

def DAL_from_fileupload(index):
    dbStr = "select * from fileUploadInf where fileHash='{0}'"
    db = DBMethods()
    dbStr = dbStr.format(index)
    ret = db.selectMethods(dbStr)
    return ret

def DAL_from_usererr(index):
    dbStr = "select * from userErrInf where fileHash='{0}'"
    db = DBMethods()
    dbStr = dbStr.format(index)
    ret = db.selectMethods(dbStr)
    return ret
	
def DAL_get_dep_user_error_detail(personName,province, city, department, page, status, like, page_num=20):  #按日期获取异常数据
    if province == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0}  and userStatus=1 and userName="{1}" and userInf.departmentId in '
        dbStr += '(select departmentId from departmentInf) order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"),personName.decode("utf-8"))
    elif province != None and city != None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize,departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and fileInf.fileHash=userErrInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} and userStatus=1 and userInf.departmentId in '
        dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}") and userName="{3}" order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"), city.decode("utf-8"),personName.decode("utf-8")) 
    elif province != None and city != None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} and userStatus=1 and userName="{4}" and userInf.departmentId in '
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName like "{3}%") order by errTime desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and city="{2}" and departmentName = "{3}") order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"), city.decode("utf-8"), department.decode("utf-8"),personName.decode("utf-8"))
    elif province != None and city == None and department != None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} and userStatus=1 and userName="{3}" and userInf.departmentId in '
        if like == True:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName like "{2}%") order by errTime desc '
        else:
            dbStr += '(select departmentId from departmentInf where province="{1}" and departmentName = "{2}") order by errTime desc '
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"), department.decode("utf-8"),personName.decode("utf-8"))
    elif province != None and city == None and department == None:
        dbStr = 'select userName, userErrInf.errId, DATE_FORMAT( errTime, "%H:%i:%s %Y-%m-%d"), errOperate, fileName, userErrInf.fileHash, keyWords, userIp, hostMac, userNo, keyExtend, fileSize, departmentName,city '
        dbStr += 'from userInf, userErrInf, fileUploadInf, computerInf,fileInf, departmentInf '
        dbStr += ' where computerInf.userId=userInf.userId and userErrInf.fileHash=fileInf.fileHash and uploadTime=errTime and userInf.userId=userErrInf.userId and userInf.departmentId = departmentInf.departmentId '
        dbStr += ' and errStatus={0} and userStatus=1 and userName="{2}"'
        dbStr = dbStr.format(status.decode("utf-8"), province.decode("utf-8"),personName.decode("utf-8"))
    if page != -1:
        dbStr += "limit {0},{1};"
        dbStr = dbStr.format(str(int(page)*int(page_num)), str(page_num))
    print("[dbStr] %s" %(dbStr) )


    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_install_num():
    dbStr = "select COUNT(*) from computerInf,userInf where registStatus=1 and computerInf.userId = userInf.userId;"
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_get_ukey_info():
    dbStr = "select companyName,userscale,installNum,DATE_FORMAT( serviceUntilTime, '%Y-%m-%d %H:%i:%s') from ukeyInf;"
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret


def DAL_is_ukey_exist():
    dbStr = "select * from ukeyInf;"
    db = DBMethods()
    ret = db.selectMethods(dbStr)
    return ret
