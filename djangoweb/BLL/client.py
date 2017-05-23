# -*- coding:utf-8 -*-

import socket
import struct

web_proxy_ip = '127.0.0.1'
server_adress = (web_proxy_ip, 50006)

messages = []
frm = "I10s10sI255s"

def init_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_adress)
    except:
        return False
    return client_socket


def set_values_port(data=""):   #获取端口信息
    values = ("GET".encode("utf-8"), "PORT".encode("utf-8"), len(data), data.encode("utf-8"))
    return values


def set_values_close_port(data=""): #关闭端口
    values = ("CLOSE".encode("utf-8"), "PORT".encode("utf-8"), len(data), data.encode("utf-8"))
    return values


def set_values_close_net(data=""): #关闭网络
    values = ("CLOSE".encode("utf-8"), "NET".encode("utf-8"), len(data), data.encode("utf-8"))
    return values

def set_values_open_net(data=""): #关闭网络
    values = ("OPEN".encode("utf-8"), "NET".encode("utf-8"), len(data), data.encode("utf-8"))
    return values

def set_values_scan_file(data=""): #扫描用户文件
    values = ("SCAN".encode("utf-8"), "FILE".encode("utf-8"), len(data), data.encode("utf-8"))
    return values

def set_values_scan_self(data=""): #用户自查
    values = ("SCAN".encode("utf-8"), "SELF".encode("utf-8"), len(data), data.encode("utf-8"))
    return values

def set_values_remove_self(data=""):
    values = ("REMOVE".encode("utf-8"), "SELF".encode("utf-8"), len(data), data.encode("utf-8"))
    return values


def pack_messages(values):  #数据打包
    frm = "I10s10sI950s"
    length = struct.calcsize(frm)
    pack_data = struct.pack(frm ,length, *values)
    return pack_data


def get_data(info): #数据解包
    frm = "10s10sI950s"
    method, thing, size, data = struct.unpack(frm, info)
    method = method.decode("utf-8").strip("\0")
    thing = thing.decode("utf-8").strip("\0")
    data = data.decode("utf-8").strip("\0")
    if size - len(data) != 0:
        return None, None, None

    return method, thing, data


def recv_data(sock):    #接收数据
    s = struct.calcsize("I")
    length, = struct.unpack("I", sock.recv(s))
    bite = sock.recv(length)
    return bite

def set_img(index):
    if index == "101":
        return ["101","static/images/qq.png"]
    if index == "103":
        return ["103", "static/images/ie.png"]
    if index == "104":
        return ["104", "static/images/qqBrowser.png"]
    if index == "105":
        return ["105", "static/images/360.png"]
    if index == "107":
        return ["106", "static/images/firefox.png"]
    if index == "108":
        return ["107", "static/images/google.png"]
    if index == "109":
        return ["108", "static/images/sougou.png"]
    if index == "110":
        return ["110", "static/images/opera.png"]
    if index == "111":
        return ["111", "static/images/cheetah.png"]
    if index == "112":
        return ["112", "static/images/others.png"]
    if index == "201":
        return ["201", "static/images/wps.png"]
    return index


def oprate_data(data):  #解析数据
    data = data.split("|")[0:-1]
    ret_dir = []
    for index in data:
        img_list = []
        index = index.split(",")[0: ]
        img = ""
        for i in index:
            img = set_img(i)
            img_list.append(img) 
            ret_dir.append(img_list)
    return ret_dir

def recv_conn(client_sock):
    retData = False
    while 1:
        bite = recv_data(client_sock)
        method, thing, data = get_data(bite)
        if method == "GET" and thing == "PORT":
            if data == "OK":
                break
            else:
                retData = oprate_data(data)
                user_list = "OK"
                values = set_values_port(user_list)
                pack_data = pack_messages(values)
                client_sock.send(pack_data)
        elif method == "CLOSE" and thing == "PORT":
            if data == "OK":
                retData = True
                ret = "OK"
                values = set_values_close_port(ret)
                pack_data = pack_messages(values)
                client_sock.send(pack_data)
                break
            print("recv data err.")
            retData = False
            break
        
        elif method == "CLOSE" and thing == "NET":
            if data == "OK":
                retData = True
                ret = "OK"
                values = set_values_close_net(ret)
                pack_data = pack_messages(values)
                client_sock.send(pack_data)
                
                break
            print("recv data err.")
            retData = False
            break
        
        elif method == "OPEN" and thing == "NET":
            if data == "OK":
                retData = True
                ret = "OK"
                values = set_values_open_net(ret)
                pack_data = pack_messages(values)
                client_sock.send(pack_data)
                break
            print("recv data err.")
            retData = False
            break
        elif method == "SCAN" and thing == "FILE":
            if data == "OK":
                retData = True
                ret = "OK"
                values = set_values_scan_file(ret)
                pack_data = pack_messages(values)
                client_sock.send(pack_data)
                break
            print("recv data err.")
            retData = False
            break
        elif method == "SCAN" and thing == "SELF":
            if data == "OK":
                retData = True
                ret = "OK"
                values = set_values_scan_self(ret)
                pack_data = pack_messages(values)
                client_sock.send(pack_data)
                break
            else:
                print("recv data err.")
                retData = False
                break
        elif method == "REMOVE" and thing == "SELF":
            if data == "OK":
                retData = True
                ret = "OK"
                values = set_values_remove_self(ret)
                pack_data = pack_messages(values)
                client_sock.send(pack_data)
                break
            else:
                print("recv data err.")
                retData = False
                break
    client_sock.close()
    return retData


def conn_run(comm, user_list=None, program_list=None):
    if comm != "get_por" and comm != "close_Pro" and comm != "close_net" and comm != "open_net" and comm != "scan_file" and comm !="scan_self" and comm != "remove_self":
        return False

    client_sock = init_socket()
    if client_sock == False:
        return False
    if comm == "get_por":
        if user_list == None:
            return False

        values = set_values_port(user_list)
        pack_data = pack_messages(values)
        client_sock.send(pack_data)
        data = recv_conn(client_sock)
        return data
    elif comm == "close_Pro":
        if program_list == None:
            return False
        
        values = set_values_close_port(program_list)
        pack_data = pack_messages(values)
        client_sock.send(pack_data)
        data = recv_conn(client_sock)
        if(data):
            return True
        else:
            return False
    elif comm == "close_net":
        if user_list == None:
            return False
        values = set_values_close_net(user_list)
        pack_data = pack_messages(values)
        client_sock.send(pack_data)
        data = recv_conn(client_sock)
        return data
    elif comm == "open_net":
        if user_list == None:
            return False
        values = set_values_open_net(user_list)
        pack_data = pack_messages(values)
        client_sock.send(pack_data)
        data = recv_conn(client_sock)
        return data
    elif comm == "scan_file":
        if user_list == None:
            return False
        values = set_values_scan_file(user_list)
        pack_data = pack_messages(values)
        client_sock.send(pack_data)
        data = recv_conn(client_sock)
        return data
    elif comm == "scan_self":
        if user_list == None:
            return False
        values = set_values_scan_self(user_list)
        pack_data = pack_messages(values)
        client_sock.send(pack_data)
        data = recv_conn(client_sock)
        return data
    elif comm == "remove_self":
        if user_list == None:
            return False
        values = set_values_remove_self(user_list)
        pack_data = pack_messages(values)
        client_sock.send(pack_data)
        data = recv_conn(client_sock)
        return data
