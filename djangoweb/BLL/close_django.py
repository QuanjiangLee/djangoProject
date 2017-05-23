import os, time
from BLL.ukey_handle import is_server_granted

def close_django():
    os.system("supervisorctl stop DjangoWeb")

def check_auth():
    if not is_server_granted():
        close_django()
        raise("UEKY IS DEFAULT")

