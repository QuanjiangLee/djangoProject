#! /bin/bash 
#PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
#export PATH

#clear
set -e

if [ ! -x "$0" ]; then
    chmod +x "$0"
    echo "已为此文件添加可执行权限，请再次运行安装命令！";
    exit 1;
fi

if [[ $EUID -ne 0 ]]; then
     echo "错误:请在root用户权限下运行!" 1>&2;
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

while :;
do
read -r -p "请输入mysql数据库密码：" -s  mysqlPasswd
echo ""
read -r -p "请确认您输入的mysql数据库密码：" -s mysqlPasswd2
if [ "$mysqlPasswd2" != "$mysqlPasswd" ];then
    echo "您输入的mysql密码不一致，请重新输入！";
else 
    break;
fi
done

clear

echo "开始安装准备..."

yum update -y
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

#安装mysql-community
echo "安装mysql数据库..."

if command -v mysql >/dev/null 2>error.log; then
	echo "mysql 已经存在！"
else
#rpm -qa | grep mysql-community-release-el7-5.noarch &>/dev/null
if [ $? -ne 0 ]; then
rpm -ivh mysql-community-release-el7-5.noarch.rpm
fi
#yum repolist enabled | grep "mysql.*-community*"
yum install -y mysql-community-server
fi
systemctl enable mysqld
systemctl start mysqld

#设置mysql
echo "设置数据库密码和创建数据库用户safeUser..."
#drop user 'safeUser'@'localhost';
#flush privileges;
#create user 'safeUser'@'localhost' identified by 'xaut.qll';
mysqladmin -u root -h localhost password "$mysqlPasswd" >/dev/null 2>error.log &  
echo "continue..."
mysql -uroot -p$mysqlPasswd -e "" &>/dev/null && echo "成功设置数据库密码！" || echo "数据库密码设置错误，您可能已经设置过密码了！请在error.log中查看详情。"

cmdUser="select count(*) from mysql.user where user='safeUser';"
usercount=$(mysql -uroot -p$mysqlPasswd -s -e "${cmdUser}")

echo "continue..."
if [ $usercount -eq 0 ]; then	
echo $usercount
createUser="drop user 'safeUser'@'localhost';flush privileges;create user 'safeUser'@'localhost' identified by '${mysqlPasswd}';"
createcount=$(mysql -uroot -p$mysqlPasswd -s -e "${createUser}")
if [ $createcount == 0 ]; then
	echo "创建数据库用户失败！"
fi
else echo "数据库用户已存在！"
fi	

echo "创建数据库并赋予权限..."

databaseSQL="create database if not exists safeDb;
create database if not exists session;
grant all privileges on safeDb.* to safeUser@localhost identified by '${mysqlPasswd}';
grant all privileges on session.* to safeUser@localhost identified by '${mysqlPasswd}';
flush privileges;"

grantDatabase= $(mysql -u root -h localhost -p$mysqlPasswd -s -e "${databaseSQL}");
if [ $grantDatabase == 0 ]; then
    echo "创建数据库并赋予权限失败！"
else echo "数据库用户并赋予权限成功！"
fi  


#导入数据库文件
echo "导入数据库文件并重启数据库"

cmd="select count(*) from information_schema.tables where table_schema='userInf';"
tablecount=$(mysql -uroot -p$mysqlPasswd -s -e "${cmd}")

if [ $tablecount == 0 ]; then
mysql -uroot -p'xaut.qll' safeDb < safeDbStruc.sql
mysql -uroot -p'xaut.qll' session < sessionStruc.sql
fi

systemctl restart mysqld
#systemctl restart mariadb

#项目存储路径
echo "正在存放项目到/home/dev目录下..."

folder='/home/dev'
if [ ! -d "$folder" ]; then
    mkdir -p "$folder"
fi
cp -r ./djangoweb /home/dev/SafeProgram

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
if [ -f "/etc/nginx/conf.d/default.conf" ]; then
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.bak
fi
systemctl restart nginx

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
echo "supervisorctl -c /etc/supervisord.conf start all" >> /etc/rc.local
rm -rf Python-3.4.6

clear
echo "恭喜你项目已经成功部署啦。。。"

