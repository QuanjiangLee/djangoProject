#-*-coding:utf-8-*-
'''
@authon: jefferson
@function: 通用处理
@time: 2017-1-14
'''


def get_data_list(data):
    data_list = str(data.decode("utf-8")).split("|")
    return data_list[0:-1]

def get_user_data(data):
    ret_list = []
    data_list = str(data.decode("utf-8")).split("|")[0:-1]
    for index in data_list:
        try:
            ret_list.append([index.split(",")[0].strip(), index.split(",")[1].strip()])
        except:
            return False

    for index in ret_list:
        data_list = index[0].split("&")
        index[0] = []
        index[0] += data_list
    return ret_list