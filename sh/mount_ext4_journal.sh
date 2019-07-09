mkfs.ext4 -E lazy_itable_init=0,lazy_journal_init=0 /dev/sdc3
mount -t ext4 -o nodelalloc,data=writeback -w /dev/sdc3 /home/j/hd3
chown j /home/j/hd3
