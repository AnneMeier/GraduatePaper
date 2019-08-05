ext4_format() {
	mkfs.xfs -f /dev/sdb3
	mount -t xfs -w /dev/sdb3 /home/j/hd3
	chown j /home/j/hd3
}

ext4_umount() {
	umount -v /dev/sdb3
}

ext4_test() {
	for qd in "1" "2" "4" "8" "16" "32" "64"; do
		for rs in "1" "4" "8" "16" "32" "64" "128" "256"; do
			for rp in "rw" "randrw"; do
				for rr in "0" "5" "25" "50" "75" "95" "100"; do
					ext4_format
					sync
					fio --directory=/home/j/hd3 --name fio_test_file --direct=1 --rw=${rp} --bs=${rs}K --iodepth=${qd} --rwmixread=${rr} --size=1G --numjobs=16 --time_based --runtime=120 --group_reporting > "/home/j/fio0730/result_xfs/"${qd}"_"${rs}"_"${rp}"_"${rr}".txt"
					ext4_umount
					echo "umount complete"
				done
			done
		done
	done
}

ext4_test
