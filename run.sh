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

yum install -y vim

#安装python3和pip3
#xz -d Python-3.4.6.tar.xz
tar -xvf Python-3.4.6.tar.xz
cd Python-3.4.6
yum groupinstall -y 'Development Tools'
yum install -y zlib-devel bzip2-devel openssl-devel ncurese-devel
./configure --prefix=/usr/local/python3
make && make install
cd ..

#软链接python3和pip3到环境变量
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3

#安装django 1.10.5 版
pip3 install Django==1.10.5
pip3 install pymysql
pip3 install xlrd
#安装mysql-community
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum repolist enabled | grep "mysql.*-community*"
yum install -y mysql -community-server

#设置mysql
mysql -u root -h localhost password 'xaut.qll'
mysql -u root -h localhost -p'xaut.qll' <<EOF
create database safeDb;
create database session;
CREATE USER 'safeUser'@'localhost' IDENTIFIED BY 'xaut.qll';
grant all privileges on safeDb.* to safeUser@localhost identified by 'xaut.qll';
grant all privileges on session.* to safeUser@localhost identified by 'xaut.qll';
flush privileges;
quit;
EOF
#导入数据库文件
mysql -uroot -p'xaut.qll' safeDb < safeDbstruc.sql
mysql -uroot -p'xaut.qll' session < sessionstruc.sql

systemctl restart mysqld

#项目存储路径
folder='/home/dev'
if [ ! -d "$folder" ]; then
    mkdir -p "$folder"
fi
cp -r ./djangoWeb /home/dev/SafeProgram

#安装nginx
rpm -ivh nginx-1.11.0-1.el7.ngx.x86_64.rpm
#sudo yum install epel-release
#sudo yum install python-devel nginx
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.bakconf
cp ./http.conf /etc/nginx/conf.d/http.conf
systemctl restart nginx

#安装配置supervisord 和wsgi
pip3 install supervisor
pip install uwsgi --upgrade
cp ./supervisord.conf /etc/supervisord.conf
supervisord -c /etc/supervisord.conf
supervisorctl -c /etc/supervisord.conf start djangoWeb
clear

echo"恭喜你项目已经成功部署啦。。。"






