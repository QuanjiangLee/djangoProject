#! /bin/bash 
#PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
#export PATH

#clear
set -e

if [[ $EUID -ne 0 ]]; then
     echo "错误:请在root用户权限下运行!" 1>&2;
     exit 1;
fi

if [ ! -x "$0" ]; then
    chmod +x "$0"
    echo "已为此文件添加可执行权限，请再次运行安装命令！";
    exit 1;
fi

read -r -p "您确定要运行安装项目程序吗? [Y/n] " input
case $input in
    [yY][eE][sS]|[yY])
            echo "您选择了YES!"
            ;;
*)
        echo "你选择了其他选项，安装停止！"
        exit 1;
        ;;
esac

#让用户自定义数据库密码（暂时注释）
#while :;
#do
#read -r -p "请输入mysql数据库密码：" -s  mysqlPasswd
#echo ""
#read -r -p "请确认您输入的mysql数据库密码：" -s mysqlPasswd2
#if [ "$mysqlPasswd2" != "$mysqlPasswd" ];then
#    echo "您输入的mysql密码不一致，请重新输入！";
#else 
#    break;
#fi
#done

#初始化数据库密码为'xaut.qll'
mysqlPasswd='xaut.qll'

clear
echo "开始安装准备..."

#yum update -y
yum groupinstall -y 'Development Tools'
yum install -y zlib-devel bzip2-devel openssl-devel ncurese-devel
yum install -y vim

#安装python3和pip3
#xz -d Python-3.4.6.tar.xz
echo "安装python3和pip3..."

if [ ! -f "/usr/bin/python3" ]; then
tar -xvf Python-3.4.6.tar
cd Python-3.4.6
./configure --prefix=/usr/local/python3
make && make install
cd ..
fi

#软链接python3和pip3到环境变量

echo "添加python3到环境变量..."

if [ ! -f "/usr/bin/python3" ]; then
	ln -s /usr/local/python3/bin/python3 /usr/bin/python3
fi
if [ ! -f "/usr/bin/pip3" ]; then
	ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
fi

#安装django 1.10.5 版
echo "安装django和所需模块..."

pip3 install Django==1.10.5
pip3 install pymysql
pip3 install xlrd
pip3 install twisted 
pip3 install pyopenssl

#安装mysql-community
echo "安装mysql数据库..."

if command -v mysql >/dev/null 2>error.log; then
	echo "mysql 已经存在！"
else
#rpm -qa | grep mysql-community-release-el7-5.noarch &>/dev/null
if [ $? -ne 0 ]; then
rpm -ivh mysql-community-release-el7-5.noarch.rpm &
fi
#yum repolist enabled | grep "mysql.*-community*"
yum install -y mysql-community-server
fi
systemctl enable mysqld
systemctl start mysqld

#设置mysql
echo "设置数据库密码和创建数据库用户safeUser..."
#drop user 'safeUser'@'localhost';flush privileges;   ---drop databaseUser
#create user 'safeUser'@'localhost' identified by 'xaut.qll'; ---create databaseUser
mysqladmin -u root -h localhost password "$mysqlPasswd" >/dev/null 2>error.log &  
echo "continue..."
mysql -uroot -p$mysqlPasswd -e "flush privileges;" >/dev/null 2>error.log &
if [ $? -ne 0 ]; then
     echo "数据库密码设置可能错误或者您已设置过密码了,请在error.log中查看错误！"
else echo "成功设置数据库密码！"
fi

cmdUser="select count(*) from mysql.user where user='safeUser';"
usercount=$(mysql -uroot -p$mysqlPasswd -s -e "${cmdUser}")

echo "continue..."
if [ $usercount -eq 0 ]; then	
echo $usercount
createUser="create user 'safeUser'@'localhost' identified by '${mysqlPasswd}';"
else 
createUser="drop user 'safeUser'@'localhost';flush privileges;create user 'safeUser'@'localhost' identified by '${mysqlPasswd}';"
fi	

createcount=$(mysql -uroot -p$mysqlPasswd -s -e "${createUser}")
if [ $createcount == 0 ]; then
    echo "创建数据库用户失败！"
else echo "创建数据库用户成功！"
fi

echo "创建数据库并赋予权限..."

#创建safeUser数据库用户并赋予其权限
databaseSQL="create database if not exists safeDb;
create database if not exists session;
grant all privileges on safeDb.* to safeUser@localhost identified by '${mysqlPasswd}';
grant all privileges on session.* to safeUser@localhost identified by '${mysqlPasswd}';
flush privileges;"

grantDatabase= $(mysql -u root -h localhost -p$mysqlPasswd -s -e "${databaseSQL}");
if [ $grantDatabase == 0 ]; then
    echo "创建数据库并赋予权限失败！"
else echo "创建数据库并赋予权限成功！"
fi  


#导入数据库文件
echo "导入数据库文件并重启数据库"

cmd="select count(*) from information_schema.tables where table_schema='userInf';"
tablecount=$(mysql -uroot -p$mysqlPasswd -s -e "${cmd}")

if [ $tablecount == 0 ]; then
mysql -uroot -p$mysqlPasswd safeDb < safeDb.sql
mysql -uroot -p$mysqlPasswd session < sessionStruc.sql
fi

systemctl restart mysqld
#systemctl restart mariadb

#项目存储路径
echo "正在存放项目到/home/dev目录下..."

folder='/home/dev'
if [ ! -d "$folder" ]; then
    mkdir -p "$folder"
fi
folder2='/home/zanshi'
if [ ! -d "$folder2" ]; then
    mkdir -p "$folder2"
fi
mkdir -p /home/dev/safeFile
cp -r ./SafeProgram /home/dev/SafeProgram
cp -r ./SafeProgram2 /home/zanshi/SafeProgram
if [ ! -d "./RecvFile" ]; then
cp -r ./ClientServer /home/dev/RecvFile
else
cp -r ./RecvFile /home/dev/RecvFile
fi

#安装nginx
echo "安装nginx并配置nginx..."
if command -v nginx >/dev/null 2>error.log; then 
echo "nginx exists"
else
rpm -ivh nginx-1.11.0-1.el7.ngx.x86_64.rpm
fi

#sudo yum install epel-release
#sudo yum install python-devel nginx
#mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.bakconf
cp -r ./http.conf /etc/nginx/conf.d/http.conf
cp -r ./http2.conf /etc/nginx/conf.d/http2.conf
if [ -f "/etc/nginx/conf.d/default.conf" ]; then
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.bak
fi
systemctl restart nginx
systemctl enable nginx


#安装升级pip2
echo "安装升级pip2..."
yum -y install epel-release
yum -y install python-pip
pip install --upgrade pip

#安装配置supervisor 和wsgi
echo "安装配置supervisor和wsgi..."
pip install supervisor
pip3 install uwsgi --upgrade

#配置supervisor并运行
echo "配置supervisor并运行..."
cp ./supervisord.conf /etc/supervisord.conf
supervisord -c /etc/supervisord.conf >/dev/null 2>error.log &
setsebool -P httpd_can_network_connect 1
chown -R nginx:nginx /home/dev/SafeProgram/
chmod -R 775 /home/dev/SafeProgram/
chcon -Rt httpd_sys_content_t /home/dev/SafeProgram/

echo "启动项目进程..."
supervisorctl -c /etc/supervisord.conf start DjangoWeb
#supervisorctl -c /etc/supervisord.conf restart DjangoWeb
cp supervisord.service /usr/lib/systemd/system/
systemctl enable supervisord
cp restartService.sh  /home/dev/
echo "/home/dev/restartService.sh" >> /etc/rc.local
chmod +x /etc/rc.d/rc.local
chmod +x /home/dev/restartService.sh
rm -rf Python-3.4.6
#rm -rf djangoweb
#rm -rf RecvFile
echo "DjangoWeb和RecvFile部署成功！"


echo "现在安装ukey环境..."
if [ ! -d "./jdk1.6.0_45/" ];then
chmod +x jdk-6u45-linux-x64.bin
./jdk-6u45-linux-x64.bin  #安装jdk
fi
if [ ! -d "/usr/lib/jvm/jdk1.6.0_45/" ];then
mv ./jdk1.6.0_45 /usr/lib/jvm/
#rm -rf ./jdk1.6.0_45
echo "continue..." 
fi 
echo "安装jdk1.6.0成功！"
if command -v java >/dev/null 2>error.log; then
    mv /usr/bin/java /usr/bin/javabak
    ln -s /usr/lib/jvm/jdk1.6.0_45/bin/java /usr/bin/java
else 
    ln -s /usr/lib/jvm/jdk1.6.0_45/bin/java /usr/bin/java
fi

if command -v javac >/dev/null 2>error.log; then
    mv /usr/bin/javac /usr/bin/javacbak
    ln -s /usr/lib/jvm/jdk1.6.0_45/bin/javac /usr/bin/javac
else 
    ln -s /usr/lib/jvm/jdk1.6.0_45/bin/javac /usr/bin/javac
fi
echo "export JAVA_HOME=/usr/lib/jvm/jdk1.6.0_45" >> /etc/profile
source /etc/profile
echo $JAVA_HOME
chmod +x config_dev_env/inst
chmod +x config_dev_env/uninst
#./config_dev_env/uninst > /dev/null 2>error.log
echo "yes" | ./config_dev_env/inst    #安装ukey检测环境

echo "disable firewalled and enable sshd..."
systemctl stop firewalld.service 
systemctl start sshd
systemctl enable sshd
systemctl disable firewalld.service 

echo "现在开始安装vsftp服务器..."

yum install ftp vsftpd -y

echo "vsftp服务器安装成功！"
if [ -f "/etc/vsftpd/vsftpd.conf" ];then
   mv /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.bak
fi
cp vsftpd.conf /etc/vsftpd/ #复制ftpd配置文件

mkdir -p /var/ftp/CloudMonitor
mkdir -p /var/ftp/CloudMonitor-xp
echo "创建ftp用户..."
#id safeUser  > /dev/null 2>error.log
#if [ $? -eq 0 ]
#then
#        echo "safeUser:safeUsersafeUser" | chpasswd
#else
useradd safeUser && echo "safeUser:safeUsersafeUser" | chpasswd > /dev/null 2>error.log
#fi

systemctl restart vsftpd
systemctl enable vsftpd

#clear
echo "恭喜你项目已经成功部署啦。。。"


