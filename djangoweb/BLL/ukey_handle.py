#!/usr/bin/env python3
import datetime
from ctypes import CDLL, c_int, c_size_t, POINTER, c_void_p, string_at
import subprocess
import struct
import time
import sys
import os
from DAL.insert import DAL_insert_ukey_info
from DAL.select import DAL_is_ukey_exist,DAL_get_ukey_info

FORMAT = "256s64s32sQQQQ"
SHM_SIZE = struct.calcsize(FORMAT)
SHM_KEY = 0x9511


def load_ukey():
    rt = CDLL('librt.so')
    shmget = rt.shmget
    shmget.argtypes = [c_int, c_size_t, c_int]
    shmget.restype = c_int
    shmat = rt.shmat
    shmat.argtypes = [c_int, POINTER(c_void_p), c_int]
    shmat.restype = c_void_p

    shmid = shmget(SHM_KEY, SHM_SIZE, 0o666)
    if shmid < 0:
        sys.stderr.write("shmget %x failed\n" % SHM_KEY)
        sys.stderr.flush()
        return False
    else:
        addr = shmat(shmid, None, 0)

    s = struct.Struct(FORMAT)
    try:
        buf = s.unpack_from(string_at(addr, SHM_SIZE))
    except UnboundLocalError:
        return {}

    wanted = ['company',
            'user_scale',
            'expired_time']

    fields = ['company',
            'identity',
            'usb_id',

            'user_scale',
            'auth_time',
            'expired_time', 'crc']

    data = []
    for cur_value in buf:
        if isinstance(cur_value, bytes):
            cur_value = cur_value.decode().rstrip('\0')
        data.append(cur_value)

    _data = dict(zip(fields, data))

    # 只返回必要的信息
    _deltas = set(fields) - set(wanted)
    for i in _deltas:
        if i in _data:
            _data.pop(i)
    return _data


'''
success:
    {
        'company': str(),
        'user_scale': int(),
        'expired_time': int()
    }
failed: {}
'''
def load_granted_info():
    data = load_ukey()
    if not data:
        ukey_app = 'check_ukey'
        ukey_app_path = os.path.join(os.path.dirname(__file__), ukey_app)
        print("spawning %s" % ukey_app_path)
        out = subprocess.Popen(ukey_app_path, shell=True, stdout=subprocess.PIPE).wait()
        data = load_ukey()

    if data:
        print('-' * 32)
        for k, v in data.items():
            print(k, v)
        print('-' * 32 + '\n')
    else:
        sys.stderr.write("no ukey device detected\n")

    return data


def BLL_insert_ukey_info(company,user_scale,expired_time):
    DAL_insert_ukey_info(company,user_scale,expired_time)


def BLL_get_ukey_info():
    ukey_info = DAL_get_ukey_info()
    ret_ukey = {}
    for index in ukey_info:
        ret_ukey["company"] = index[0]
        ret_ukey["user_scale"] = index[1]
        ret_ukey["install_num"] = index[2]
        ret_ukey["expired_time"] = index[3]
    print("[ukey information]:",ret_ukey)
    return ret_ukey


def is_server_granted():
    data = load_granted_info()
    company = data["company"]
    user_scale = data["user_scale"]
    expired_time = data["expired_time"]
    if not data:
        return False
    else:
        cur = int(time.time())
        if expired_time > cur:
            expired_time = datetime.datetime.fromtimestamp(expired_time).strftime("%Y-%m-%d %H:%M:%S")
            if DAL_is_ukey_exist():
                return True
            else:
                BLL_insert_ukey_info(company,user_scale,expired_time)
                return True
        else:
            return False


if __name__ == '__main__':
    print("is_server_granted:", is_server_granted())
