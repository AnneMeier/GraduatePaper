mkfs.ext4 /dev/sdc3
mount -t ext4 -o data=writeback -w /dev/sdc3 /home/j/hd3
chown j /home/j/hd3
