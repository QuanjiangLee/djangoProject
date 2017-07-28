# !/bin/bash
# add for chkconfig
#description:auto restart
sleep 15
echo "hello" > `pwd`\/test.txt
supervisorctl -c /etc/supervisord.conf restart all

