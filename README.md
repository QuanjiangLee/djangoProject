# installProject
部署WEB项目。
## 使用说明
```
git clone https://github.com/QuanjiangLee/installProject.git
cd installProject
sh run.sh
```
##脚本执行过程中遇到的问题和解决方法
1.系统自带mariaDb无法启动：启动文件权限问题，查看错误日志并修改文件权限。

2.mariaDb5.5 在导入数据库表结构时出现表结构不兼容（Invalid default value of 'dbTime'）,于是移除了mariaDb，安装了前服务器mysql版本。

3.mysql语句冲突问题：检测数据库用户名，数据库名是否存在时，使用”不对应“命令导致错误，例如:"create user test...;""delete from mysql.user where user = 'test';"
再次"create user test...;"无法再创建test用户。解决方法是使用"对应sql" "drop user test ..."

4.win下和linux下导出的mysql 数据库文件的差异导致导入数据库文件和导出数据库文件错误（导入必须用source,再导出的数据库文件就为空了）。最后是在linux下完成数据库文件的数据初始化。

5.修改表AUTO_INCREMENT值.
使用mysqldump -uroot -p -d safeDb > safeDbstruc.sql 导出的表结构，表中AUTO_INCREMENT 值依然未初始化，使用alter table userInf  auto_increment = 1;修改userInf 初始值为1；最后通过打印修改语句并执行的方法实现了批量修改，使AUTO_INCREMENT的值初始化为1.

6.防火墙设置
 项目部署程序运行完成后，依然不能正常访问，错误日志说是权限问题，但改了好几遍文件和某些配置文件使用者权限，依然未能解决，后来才发现是centos7的firewalled 的问题，后续又配置firewalled，然后又关闭了它，还改了web目录的content_http 属性才得以正常访问。

7.还有需要注意的就是，在使用supervisor管理运行项目前，需运行其配置文件，生成其自定义socket，并且每次更改配置，都需重新运行生成，生成命令为：sudo supervisord -c /etc/supervisord.conf

8.uwsgi进程夯余导致启动的DjangoWeb，无法正常访问和使用。解决办法时先停掉supervisor 运行的djangoweb程序，再手动全部清除uwsgi进程，然后再用supervisor 启动项目
