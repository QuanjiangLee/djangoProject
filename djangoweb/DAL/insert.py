#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 在数据库插入数据
@time: 2017-1-13
'''

from DAL.DBMethods import DBMethods
from DAL.select import DAL_get_install_num

def DAL_insert_user_inf(userNo, userName, userPositionStatus, dep):
    dbStr = "insert into userInf(userNo, userName, userPositionStatus, departmentId) values('{0}', '{1}', {2}, {3});"
    dbStr = dbStr.format(userNo, userName, userPositionStatus, dep)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_insert_department_inf(department, create_time, province, city, status, create_user):
    dbStr = "insert into departmentInf(departmentName, createTime, province, city, status, createUser) values('{0}', '{1}', '{2}', '{3}', {4}, '{5}');"
    dbStr = dbStr.format(department, create_time, province, city, status, create_user)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_insert_key_inf(key, keyLever, user_acc, keyStatus=1):
    dbStr = "insert into keywordsInf(keyword, keyLever, createUserStatus, createUserId) values('{0}', '{1}', {2}, '{3}');"
    dbStr = dbStr.format(key, keyLever, keyStatus, user_acc.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_insert_dep_key(key, dep):
    dbStr = "insert into departmentKey(keyId, departmentId) values({0}, {1});"
    dbStr = dbStr.format(key, dep)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_insert_remote_record(send_no, receive_no, comm, send_time, send_status):
    dbStr = "insert into remoteRecord(sendNo, receiveNo, orderName, sendTime, sendStatus) values('{0}' \
            ,'{1}','{2}','{3}','{4}');"
    dbStr = dbStr.format(send_no, receive_no, comm, send_time, send_status)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_insert_by_excel(user_no, user_name,department_no):
    dbStr = "insert into userInf(userNo,userName,departmentId) values ('{0}','{1}',{2});"
    dbStr = dbStr.format(user_no, user_name, department_no)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


def DAL_insert_ukey_info(company,user_scale,expired_time):
    print("[company]:",company,"[user_scale]:",user_scale,"[expired_time]:",expired_time)
    install_num = DAL_get_install_num()[0][0]
    print("[install_num]:",install_num)
    dbStr = "insert into ukeyInf (companyName,userScale,installNum,serviceUntilTime)values('{0}',{1},{2},'{3}');"
    dbStr = dbStr.format(company,user_scale,install_num,expired_time)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
