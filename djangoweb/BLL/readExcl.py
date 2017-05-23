#-*-#-*-coding:utf-8-*-
import xlrd

def open_excel(file_name):  #打开文件
    try:
        data = xlrd.open_workbook(file_name)
        print("[data]:", data)
        return data
    except (Exception, e):
        print(e)
    return False

def excel_table_byindex(file_name,colnameindex=0,by_index=0):   #解析表格数据返回list(dir)
    try:
        data = open_excel(file_name)
    except:
        return False
    if not data:
        return False
    table = data.sheets()[by_index]
    print("[table]:", table)
    nrows = table.nrows #行数
    print("[nrows]:", nrows)
    colnames = table.row_values(colnameindex) #第一行数据（表头）
    print("[colnames]:", colnames)
    ret_list = []
    for rownum in range(1, nrows):#对于表中的一行进行操作
        row = table.row_values(rownum)#一行的数据
        if row[0]:#用户编号不为空
            app = {}
            row[0] = str(row[0])#对user_no进行单独处理，因为excel表格默认将user_no转化成了float，因为它是纯数字构成的
            app[colnames[0]] = row[0].rsplit(".",1)[0]
            for i in range(1,len(colnames)):#把一行的数据循环插进去
                app[colnames[i]] = row[i]
            ret_list.append(app)
    print("[ret_list]:", ret_list)
    return ret_list




