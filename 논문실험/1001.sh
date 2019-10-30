ext4_format() {
	#loc	jour		asyn				dela			bs
	#sda1 journal async_comm 	delalloc 	4
	#			mount		mount				mount			mkfs
	#			data=		jac					del				-b
	mkfs.ext4 -b $5 -F /dev/$1
	mount -t ext4 -o $4,data=$2 -w /dev/$1 /home/j/hd3
	chown j /home/j/hd3
}


f2fs_format(){
	#loc	fsync		cpoint	segpsec	secpzone
	#sda1	posix 	disable 1 			2
	#			mount		mount		mkfs		mkfs
	#			f._m.=	c.p.=		-s			-z
	mkfs.f2fs -s $4 -z $5 -f /dev/$1
	mount -t f2fs -o fsync_mode=$2,checkpoint=$3 -w /dev/$1 /home/j/hd3
	chown j /home/j/hd3
}

btrfs_format(){
	#loc	datacow secsize nodesize
	#sda1	datacow	1024		2
	#			mount		mkfs		mkfs
	#			-o			-s			-n
	echo $1 $2 $3 $4
	mkfs.btrfs -n $4 -f /dev/$1
	mount -t btrfs -w /dev/$1 /home/j/hd3
	chown j /home/j/hd3
}

my_umount() {
	umount -v /dev/$1
}


ext4_test() {
	#3*2*2*3=36

	for jour in writeback;do
		for asyn in jac;do
			for dela in delalloc;do
				for bs in 1024 2048 4096;do

					mkdir -p /home/j/jws/$2_ext4/${jour}_${asyn}_${dela}_${bs}

					ext4_format $1 ${jour} ${asyn} ${dela} ${bs}
					sync
					echo ------------------------------------------------------------------
					echo ${jour}_${asyn}_${dela}_${bs}_cohe start
					fs_test_cohe $2_ext4/${jour}_${asyn}_${dela}_${bs}
					#mount_test
					my_umount $1
					echo umount complete

					ext4_format $1 ${jour} ${asyn} ${dela} ${bs}
					sync
					echo ${jour}_${asyn}_${dela}_${bs}_scat start
					fs_test_scat $2_ext4/${jour}_${asyn}_${dela}_${bs}
					#mount_test
					my_umount $1
					echo umount complete

				done
			done
		done
	done
}

f2fs_test() {
	#3*2*3*3=54

	for fsync in posix strict nobarrier;do
		for cpoint in disable enable;do
			for segpsec in 1 2 4;do
				for secpzone in 1 2 4;do

					mkdir -p /home/j/jws/$2_f2fs/${fsync}_${cpoint}_${segpsec}_${secpzone}

					f2fs_format $1 ${fsync} ${cpoint} ${segpsec} ${secpzone}
					sync
					echo ${fsync}_${cpoint}_${segpsec}_${secpzone}_cohe start
					#fs_test_cohe $2_f2fs/${fsync}_${cpoint}_${secsize}_${segpsec}_${secpzone}
					mount_test
					my_umount $1
					echo umount complete

					f2fs_format $1 ${fsync} ${cpoint} ${segpsec} ${secpzone}
					sync
					echo ${fsync}_${cpoint}_${segpsec}_${secpzone}_scat start
					#fs_test_scat $2_f2fs/${fsync}_${cpoint}_${secsize}_${segpsec}_${secpzone}
					mount_test
					my_umount $1
					echo umount complete

				done
			done
		done
	done


}

btrfs_test() {
	#2*3*3=18

	for datacow in datacow nodatacow;do
		for secsize in 1024;do
			for nodesize in 4096 8192 16384;do

				mkdir -p /home/j/jws/$2_btrfs/${datacow}_${secsize}_${nodesize}
				btrfs_format $1 ${datacow} ${secsize} ${nodesize}
				sync
				echo ${datacow}_${secsize}_${nodesize}_cohe start
				fs_test_cohe $2_btrfs/${datacow}_${secsize}_${nodesize}
				#mount_test
				my_umount $1
				echo umount complete

				btrfs_format $1 ${datacow} ${secsize} ${nodesize}
				sync
				echo ${datacow}_${secsize}_${nodesize}_scat start
				fs_test_scat $2_btrfs/${datacow}_${secsize}_${nodesize}
				#mount_test
				my_umount $1
				echo umount complete

			done
		done
	done

}

fs_test_cohe(){
	#3*2*5*3=90
	for io_en in sync; do
		for rp in rw randrw; do
			for rr in 0 50 100; do
				for rs in 4 32 128; do
					fio --directory=/home/j/hd3 --name fio_test_file --ioengine=${io_en} --rw=${rp} --rwmixread=${rr} --bs=${rs} \
						--size=1G --numjobs=1 --time_based --runtime=100 --group_reporting \
						> /home/j/jws/$1/${io_en}_${rp}_${rr}_${rs}_cohe.txt
				done
			done
		done
	done
}

fs_test_scat(){
	#3*2*5*3=90
	for io_en in sync; do
		for rp in rw randrw; do
			for rr in 0 50 100; do
				for rs in 4 32 128; do
					fio --directory=/home/j/hd3 --name fio_test_file --ioengine=${io_en} --rw=${rp} --rwmixread=${rr} --bs=${rs} \
						--size=1m --numjobs=1000 --time_based --runtime=100 --group_reporting \
						> /home/j/jws/$1/${io_en}_${rp}_${rr}_${rs}_scat.txt
				done
			done
		done
	done
}

mount_test(){
	#fio --directory=/home/j/hd3 --name fio_test_file --rw=rw --bs=4 --ioengine=sync --rwmixread=100 \
	#	--size=1m --numjobs=1 --time_based --runtime=1 --group_reporting \
	#	> /home/j/jws/test.txt
	echo mount test-----
}

test(){
	ext4_test $1 $2
	#f2fs_test $1 $2
	#btrfs_test $1 $2
}

test sdb3 hdd
