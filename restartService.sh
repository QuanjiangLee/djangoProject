# !/bin/bash
# add for chkconfig
#description:auto restart
sleep 15
#UUID='EAA7-A356'
#Device=`blkid | grep $UUID | cut -d : -f 1`
#if [ $Device ]; then
#mount $Device /mnt
#cp /mnt/check_ukey .
#./check_ukey t 
#rm check_ukey
#else echo "No Ukey devices found!"
#fi
supervisorctl -c /etc/supervisord.conf restart all

