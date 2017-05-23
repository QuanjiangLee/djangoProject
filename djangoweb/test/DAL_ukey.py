import datetime
from .DBMethods import DBMethods
def DAL_insert_ukey_info(company,user_scale,install_num,expired_time):
        expired_time = datetime.datetime.fromtimestamp(expired_time).strftime("%Y-%m-%d %H:%M:%S")
        dbStr = "insert into ukeyInf (companyName,userScale,installNum,serviceUntilTime)values('{0}',{1},{2},'{3}');"
        dbStr = dbStr.format(company,user_scale,install_num,expired_time)
        db = DBMethods()
        print(dbStr)
        ret = db.updateMethods(dbStr)
        return ret


def DAL_get_install_num():
	dbStr = "select COUNT(*) from computerInf,userInf where registStatus=1 and computerInf.userId = userInf.userId"
	db = DBMethods()
	ret = db.selectMethods(dbStr)
	return ret


def DAL_get_ukey_info():
	dbStr = "select companyName,userscale,installNum,DATE_FORMAT( serviceUntilTime, '%Y-%m-%d %H:%i:%s') from ukeyInf;"
	db = DBMethods()
	ret = db.selectMethods(dbStr)
	return ret

