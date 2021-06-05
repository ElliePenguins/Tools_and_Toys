#!/bin/bash

IP_ADDR="192.168.1.1"

for i in {1..255}
do
	ping -c 1 $IP_ADDR;
	if [ $? == 0 ]
	then
		# Example: mount -t nfs $IP_ADDR:/srv/data /srv/data
		echo "Enter commands here"
		break
	fi
	sleep 1
done

# Example: /home/user/script that_acts_on_nfs_data 
echo "Run anything else here"
