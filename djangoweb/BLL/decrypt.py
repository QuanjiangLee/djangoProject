#encoding: utf-8
import os
import sys
import subprocess

ENCRYPTED_SUFFIX = ".aes"

ENCRYPT_CMD = """7z {IS_ENCRYPTED} -y -p{PASS} "{SRC}" """


def sys_run(cmd=None):
    if cmd is None:
        return
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as error:
        print(error)
        return False
    else:
        return True


class Openssl:
    def __init__(self, filepath, passwd="123456", generatePath=None):
        self.filePath = filepath
        self.password = passwd
        self.generatePath = None
        self.isEncrypted = True    # 记录文件是否为加密状态

        # 如果文件的后缀含有 ".aes" 则说明这是一个已经加密过的文件
        pos = filepath.find(ENCRYPTED_SUFFIX)
        if pos == -1:
            self.isEncrypted = False

        # 如果没有指定生成路径，则自动构造生成路径
        if generatePath is None:
            if self.isEncrypted:
                self.generatePath = filepath[:pos]
            else:
                self.generatePath = filepath + ENCRYPTED_SUFFIX
        else:
            self.generatePath = generatePath

    # 解密一个文件
    def decrypt(self):
        if self.isEncrypted is False:
            print("%s is not a encrypted file!" %(self.filePath))
            return
        cmd = ENCRYPT_CMD.format(IS_ENCRYPTED="e", SRC=self.filePath, PASS=self.password)
        print(cmd)
        return sys_run(cmd)

    # 加密一个文件
    def encrypt(self):
        if self.isEncrypted:
            print("%s is already encrypted before!")
        cmd = ENCRYPT_CMD.format(IS_ENCRYPTED="a", SRC=self.filePath, PASS=self.password)
        print(cmd)
        return sys_run(cmd.decode())


# 至少需要两个参数，分别为‘待解密文件路径’、解密密码
# 当然，也可以指定保存路径
def Decrypt(filePath, realName, passwd=None, dstPath=None):
    pos = realName.find(ENCRYPTED_SUFFIX)
    if pos != -1:
    	realName = realName[0:pos]

    abs_path = os.path.join(dstPath, realName)
    cmd = "openssl enc -d -aes-128-cbc -k {PASSWD} -in {SOURCE} -out '{TARGET}'".format(\
        PASSWD=passwd, SOURCE=filePath, TARGET=abs_path)
    return sys_run(cmd)



if __name__ == '__main__':
    realName = "我的世界.docx"
    srcPath = "/tmp/win/test.docx.aes"
    dstPath = "/tmp/win/"
    passwd = "123456"
    Decrypt(srcPath, realName, passwd, dstPath)

def delete_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except:
            return False
