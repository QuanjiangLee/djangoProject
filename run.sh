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
        echo "安装停止！"
        exit 1;
        ;;
esac

clear
yum update -y
yum install -y vim

#安装python3和pip3
#xz -d Python-3.4.6.tar.xz

if [ ! -f "/usr/bin/python3" ]; then
tar -xvf Python-3.4.6.tar
cd Python-3.4.6
yum groupinstall -y 'Development Tools'
yum install -y zlib-devel bzip2-devel openssl-devel ncurese-devel
./configure --prefix=/usr/local/python3
make && make install
cd ..
fi

#软链接python3和pip3到环境变量

if [ ! -f "/usr/bin/python3" ]; then
	ln -s /usr/local/python3/bin/python3 /usr/bin/python3
fi
if [ ! -f "/usr/bin/pip3" ]; then
	ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
fi

#安装django 1.10.5 版

pip3 install Django==1.10.5
pip3 install pymysql
pip3 install xlrd

#安装mysql-community
echo "安装mysql"
if command -v mysql >/dev/null 2&>1; then
	echo "mysql 已经存在！"
else
#rpm -qa | grep mysql-community-release-el7-5.noarch &>/dev/null
if [ $? -ne 0 ]; then
rpm -ivh mysql-community-release-el7-5.noarch.rpm
fi
#yum repolist enabled | grep "mysql.*-community*"
yum install -y mysql-community-server
fi
sudo systemctl enable mysqld
sudo systemctl start mysqld

#设置mysql
#drop user 'safeUser'@'localhost';
#flush privileges;
#create user 'safeUser'@'localhost' identified by 'xaut.qll';
mysqladmin -u root -h localhost password 'xaut.qll'  
cmdUser="select count(*) from mysql.user where user='safeUser';"
usercount=$(mysql -uroot -p'xaut.qll' -s -e "${cmdUser}")
if [ $usercount -eq 0 ]; then	
echo $usercount
createUser="create user 'safeUser'@'localhost' identified by 'xaut.qll';"
createcount=$(mysql -uroot -p'xaut.qll' -s -e "${createUser}")
if [ $createcount -eq 0 ]; then
	echo "创建数据库用户失败！"
fi
else echo "数据库用户已存在！"
fi	
mysql -u root -h localhost -p'xaut.qll' <<EOF
create database if not exists safeDb;
create database if not exists session;
grant all privileges on safeDb.* to safeUser@localhost identified by 'xaut.qll';
grant all privileges on session.* to safeUser@localhost identified by 'xaut.qll';
flush privileges;
EOF

#导入数据库文件
cmd="select count(*) from information_schema.tables where table_schema='userInf';"
tablecount=$(mysql -uroot -p'xaut.qll' -s -e "${cmd}")
if [ $tablecount -eq 0 ]; then
mysql -uroot -p'xaut.qll' safeDb < safeDbStruc.sql
mysql -uroot -p'xaut.qll' session < sessionStruc.sql
fi
systemctl restart mysqld
#systemctl restart mariadb

#项目存储路径
folder='/home/dev'
if [ ! -d "$folder" ]; then
    mkdir -p "$folder"
fi
cp -r ./djangoweb /home/dev/SafeProgram

#安装nginx
if command -v nginx >/dev/null 2&>1; then 
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
yum -y install epel-release
yum -y install python-pip
pip install --upgrade pip

#安装配置supervisor 和wsgi
pip install supervisor
pip3 install uwsgi --upgrade

#配置supervisor并运行
cp ./supervisord.conf /etc/supervisord.conf
supervisord -c /etc/supervisord.conf
setsebool -P httpd_can_network_connect 1
chown -R nginx:nginx /home/dev/SafeProgram/
chmod -R 775 /home/dev/SafeProgram/
chcon -Rt httpd_sys_content_t /home/dev/SafeProgram/
supervisorctl -c /etc/supervisord.conf start djangoWeb
#supervisorctl -c /etc/supervisord.conf restart djangoWeb
rm -rf Python-3.4.6
rm -rf 1
clear

echo "恭喜你项目已经成功部署啦。。。"

