ext4_format() {
	mkfs.ext4 -F /dev/sdb3
	mount -t ext4 -w /dev/sdb3 /home/j/hd3
	chown j /home/j/hd3
}


f2fs_format(){
	mkfs.f2fs /dev/sdb3
	mount -t f2fs -w /dev/sdb3 /home/j/hd3
	chown j /home/j/hd3
}

btrfs_format(){
	mkfs.btrfs /dev/sdb3
	mount -t btrfs -w /dev/sdb3 /home/j/hd3
	chown j /home/j/hd3
}

my_umount() {
	umount -v /dev/sdb3
}


ext4_test() {
	for io_en in "sync" "libaio" "pvsync2"; do		
		for rp in "rw" "randrw"; do
			for rr in "0" "25" "50" "75" "100"; do
				for rs in "4" "32" "128"; do
					ext4_format
					echo ${io_en}_${rp}_${rr}_${rs}" start"
					sync
					fio --directory=/home/j/hd3 --name fio_test_file --direct=1 --rw=${rp} --bs=${rs} --ioengine=${io_en} --rwmixread=${rr} --size=1G --numjobs=1 --time_based --runtime=1 --group_reporting > /home/j/now/result/${io_en}_${rp}_${rr}_${rs}
					my_umount
					echo "umount complete"
				done
			done
		done
	done
}

f2fs_test() {
	for io_en in "sync" "libaio" "pvsync2"; do		
		for rp in "rw" "randrw"; do
			for rr in "0" "25" "50" "75" "100"; do
				for rs in "4" "32" "128"; do
					f2fs_format
					echo ${io_en}_${rp}_${rr}_${rs}" start"
					sync
					fio --directory=/home/j/hd3 --name fio_test_file --direct=1 --rw=${rp} --bs=${rs} --ioengine=${io_en} --rwmixread=${rr} --size=1G --numjobs=1 --time_based --runtime=1 --group_reporting > /home/j/now/result/${io_en}_${rp}_${rr}_${rs}
					my_umount
					echo "umount complete"
				done
			done
		done
	done
}

btrfs_test() {
	for io_en in "sync" "libaio" "pvsync2"; do		
		for rp in "rw" "randrw"; do
			for rr in "0" "25" "50" "75" "100"; do
				for rs in "4" "32" "128"; do
					btrfs_format
					echo ${io_en}_${rp}_${rr}_${rs}" start"
					sync
					fio --directory=/home/j/hd3 --name fio_test_file --direct=1 --rw=${rp} --bs=${rs} --ioengine=${io_en} --rwmixread=${rr} --size=1G --numjobs=1 --time_based --runtime=1 --group_reporting > /home/j/now/result/${io_en}_${rp}_${rr}_${rs}
					my_umount
					echo "umount complete"
				done
			done
		done
	done
}

test(){
	ext4_test
	btrfs_test
	f2fs_test
}

f2fs_test
