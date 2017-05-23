#-*-coding:utf-8-*-

'''
@authon: jefferson
@function: 抽象数据库连接
@time: 2017-1-13
'''

import pymysql
from ..DAL.analysisDb import analysis


CONFIG_NAME = "all.conf"
CONFIG_PATH = "programFile/config/db"

class DBMethods:
    def __init__(self):
       pass


    def connectMysql(self):
        db = analysis(CONFIG_NAME, CONFIG_PATH)
        db_info = db.get_result()
        print("read the information of database:",db_info)
        conn = None
        if db_info == False:
            return False
        try:
            conn=pymysql.connect(host=str(db_info["HOST"].decode("utf-8")), user=str(db_info["USER"].decode("utf-8")), passwd=str(db_info["PASSWORD"].decode("utf-8")), db=str(db_info["NAME"].decode("utf-8")), port=int(db_info["PORT"].decode("utf-8")), charset="utf8")
        except Exception as e:
            print(e)
        return conn


    '''
    @author:        屈亮亮
    @createTime:    2017-10-13
    @function:    执行数据库查询工作
    @inputs:     数据库查询语句,要查询的数据条数(str, num)
    @outputs:    查询的数据
    @error:      抛出数据查询的异常
    '''
    def selectMethods(self, dbStr, num=-1):
        e = None
        retData = None
        try:
            conn = self.connectMysql()
            cur=conn.cursor()
            cur.execute(dbStr)
            if num == -1:
                retData = cur.fetchall()
            else:
                retData = cur.fetchmany(num)
            cur.close()
            conn.close()
        except pymysql.Error as e:
            raise e
        except Exception as e:
            print(e)

        return retData

    '''
    @author:        屈亮亮conn=pymysql.connect(host=db_info["HOST"], user=self.db_info["USER"], passwd=self.db_info["PASSWORD"], db=self.db_info["NAME"], port=int(self.db_info["PORT"]), charset="utf8")
    @createTime:    2017-10-13
    @function:    执行数据库增加，删除，修改
    @inputs:     数据库查询语句,要查询的数据条数(dbStr)
    @outputs:    数据操作个条数
    @error:      抛出数据操作的异常
    '''
    def updateMethods(self, dbStr):

        e = None
        try:
            conn = self.connectMysql()
            cur=conn.cursor()
            retData = cur.execute(dbStr)
            conn.commit()
            cur.close()
            conn.close()

        except(pymysql.Error,e):
            raise e

        return retData
