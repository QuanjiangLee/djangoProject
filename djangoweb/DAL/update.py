#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 在数据库更新数据
@time: 2017-1-13
'''


from DAL.DBMethods import DBMethods


def DAL_update_user_error(secretId, status):
    dbStr = "update userErrInf set errStatus={0} where errId='{1}';"
    dbStr = dbStr.format(status.decode("utf-8"), secretId)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


def DAL_update_department_inf(departmentId, departmentName):
    dbStr = "update departmentInf set departmentName='{0}' where departmentId={1};"
    dbStr = dbStr.format(departmentName, departmentId)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


def DAL_update_user_inf(userNo, userName, userStatus):
    dbStr = "update userInf set userName='{0}' , userPositionStatus={1} where userNo='{2}';"
    dbStr = dbStr.format(userName, userStatus, userNo)
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret

def DAL_reset_userInf(userNo):
    dbStr = "update userInf set registStatus=0, loginStatus=0, userPasswd=password('1234567') where userNo='{0}';"
    dbStr = dbStr.format(userNo.decode("utf-8"))
    print(dbStr)
    db = DBMethods()
    ret = db.updateMethods(dbStr)
    return ret


def DAL_update_user_net_status(user_no, status):
    db = DBMethods()
    values = (status, user_no)
    dbStr = 'update computerInf set userNetStatus="{0}" where userId=(select userId from userInf where userNo="{1}" and userStatus=1);'
    dbStr = dbStr.format(*values)
    print(dbStr)
    ret = db.updateMethods(dbStr)
    return ret


def DAL_update_user_scan_status(user_no, status):
    db = DBMethods()
    values = (status, user_no)
    dbStr = 'update computerInf set userScanStatus={0} where userId=(select userId from userInf where userNo="{1}" and userStatus=1);'
    dbStr = dbStr.format(*values)
    print(dbStr)
    ret = db.updateMethods(dbStr)
    return ret

def DAL_update_key_inf(keyId, keyword, keyLever):
    db = DBMethods()
    values = (keyword.strip(), keyLever, keyId)
    dbStr = 'update keywordsInf set keyword="{0}", keyLever={1} where keyId={2};'
    dbStr = dbStr.format(*values)
    ret = db.updateMethods(dbStr)
    return ret
	
def DAL_update_passwd(user_acc,passwd):
    db = DBMethods()
    values = (user_acc.decode("utf-8"), passwd.decode("utf-8"))
    dbStr = 'update userInf set userPasswd=PASSWORD({1}) where userNo="{0}";'
    dbStr = dbStr.format(*values)
    ret = db.updateMethods(dbStr)
    return ret