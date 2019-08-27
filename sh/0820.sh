ext4_format() {
	mkfs.ext4 -F /dev/sdb3
	mount -t ext4 -w /dev/sdb3 /home/j/hd3
	chown j /home/j/hd3
}

ext4_umount() {
	umount -v /dev/sdb3
}

ext4_test1() {
	for io_en in "sync"; do
		for fsync in "0" "100" "1000"; do
			for rp in "rw" "randrw"; do
				for rr in "0" "25" "50" "100"; do
					#ext4_format
					sync
					strace -f -v -o "/home/j/now/result_fio_2/"${io_en}"_"${fsync}"_"${rp}"_"${rr}".txt" fio --directory=/home/j/hd3 --name fio_test_file --direct=1 --rw=${rp} --bs=4K --fsync=${fsync} --ioengine=${io_en} --rwmixread=${rr} --size=1G --numjobs=1 --time_based --runtime=60 --group_reporting
					#ext4_umount
					echo "umount complete"
				done
			done
		done
	done
}

ext4_test2() {
	for io_en in "psync" "libaio" "pvsync2" "vsync"; do
		for fsync in "100"; do
			for rp in "rw"; do
				for rr in "50"; do
					#ext4_format
					sync
					strace -f -v -o "/home/j/now/result_fio_2/"${io_en}"_"${fsync}"_"${rp}"_"${rr}".txt" fio --directory=/home/j/hd3 --name fio_test_file --direct=1 --rw=${rp} --bs=4K --fsync=${fsync} --ioengine=${io_en} --rwmixread=${rr} --size=1G --numjobs=1 --time_based --runtime=60 --group_reporting
					#ext4_umount
					echo "umount complete"
				done
			done
		done
	done
}

ext4_test2

ext4_test1
