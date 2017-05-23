#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 在数据库删除数据
@time: 2017-1-13
'''

from DAL.DBMethods import DBMethods


def delete_userInf_user_no(user_no):
    dbStr = "delete from  userInf where userNo='{0}';"
    dbStr = dbStr.format(user_no.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


def delete_computerInf_user_no(user_no):
    dbStr = "delete from computerInf where userId=(select userId from userInf where userNo='{0}');"
    dbStr = dbStr.format(user_no.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def delete_userErrInf_user_no(user_no):
    dbStr = "delete from userErrInf where userId=(select userId from userInf where userNo='{0}');"
    dbStr = dbStr.format(user_no.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def delete_fileUploadInf_user_no(user_no):
    dbStr = "delete from fileUploadInf where userId=(select userId from userInf where userNo='{0}');"
    dbStr = dbStr.format(user_no.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def delete_login_user_no(user_no):
    dbStr = "delete from loginInf where userId=(select userId from userInf where userNo='{0}');"
    dbStr = dbStr.format(user_no.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def delete_dep_key(keyId):
    dbStr = "delete from departmentKey where keyId={0};"
    dbStr = dbStr.format(keyId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def delete_key(keyId):
    dbStr = "delete from keywordsInf where keyId={0};"
    dbStr = dbStr.format(keyId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def delete_department(departmentId):
    dbStr = "delete from departmentInf where departmentId={0};"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


#   删除用户自查信息
def DAL_delete_selfcheck_data(usId):
    dbStr = "delete from selfCheck where usId={0}"
    dbStr = dbStr.format(usId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


def delete_selfcheck_userId(departmentId):
    dbStr = "delete from selfCheck where userId IN(SELECT userId FROM userInf WHERE departmentId = {0});"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def delete_userscan_userId(departmentId):
    dbStr = "delete from userScan where userId IN(SELECT userId FROM userInf WHERE departmentId = {0});"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret
	
def delete_computerInf_userId(departmentId):
    dbStr = "delete from computerInf where userId IN(SELECT userId FROM userInf WHERE departmentId = {0});"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret
	
def delete_userErrInf_userId(departmentId):
    dbStr = "delete from userErrInf where userId IN(SELECT userId FROM userInf WHERE departmentId = {0});"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret
	
def delete_loginInf_userId(departmentId):
    dbStr = "delete from loginInf where userId IN(SELECT userId FROM userInf WHERE departmentId = {0});"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret
	
def delete_fileUploadInf_userId(departmentId):
    dbStr = "delete from fileUploadInf where userId IN(SELECT userId FROM userInf WHERE departmentId = {0});"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret
	
def delete_userInf_userId(departmentId):
    dbStr = "delete from userInf where departmentId={0};"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret
	
def delete_loginLog_userId(departmentId):
    dbStr = "delete from loginLog where userId IN(SELECT userId FROM userInf WHERE departmentId = {0});"
    dbStr = dbStr.format(departmentId.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_deleteTimeSpan_selfcheck_data(scanTime):
    dbStr = "delete from selfCheck where scanTime='{0}'"
    dbStr = dbStr.format(scanTime.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret
	
def DAL_del_user_error(secretId):
    dbStr = "delete from userErrInf where errId='{0}';"
    dbStr = dbStr.format(secretId)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


def DAL_del_from_fileinf(index):
    dbStr = "delete from fileInf where fileHash='{0}'"
    dbStr = dbStr.format(index)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_del_from_upload(index):
    dbStr = "delete from fileUploadInf where fileHash='{0}'"
    dbStr = dbStr.format(index)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_del_from_usererr(index):
    dbStr = "delete from userErrInf where fileHash='{0}'"
    dbStr = dbStr.format(index)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret