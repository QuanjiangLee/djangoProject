#-*-coding:utf-8-*-

import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_indentiry_code_img():   #获取验证码的图片

    file_path = os.path.join(BASE_DIR, "static/images/verficationCode")
    for parent,dirnames,filenames in os.walk(file_path):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        length = len(filenames)
        num = random.randint(0, length-1)

        return {"img":os.path.join("static/images/verficationCode",filenames[num]), "value":filenames[num].split(".")[0]}
