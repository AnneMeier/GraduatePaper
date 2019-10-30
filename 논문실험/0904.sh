ext4_format() {
	#loc	jour		asyn				dela			bs
	#sda1 journal async_comm 	delalloc 	4
	#			mount		mount				mount			mkfs
	#			data=		jac					del				-b
	mkfs.ext4 -F /dev/$1
	mount -t ext4 -w /dev/$1 /home/j/hd3
	chown j /home/j/hd3
}


f2fs_format(){
	#loc	fsync		cpoint	secsize	segpsec	secpzone
	#sda1	posix 	disable 1024 		1 			2
	#			mount		mount		mkfs		mkfs		mkfs
	#			f._m.=	c.p.=		-w			-s			-z
	mkfs.f2fs -f /dev/$1
	mount -t f2fs -w /dev/$1 /home/j/hd3
	chown j /home/j/hd3
}

btrfs_format(){
	#loc	datacow secsize nodesize
	#sda1	datacow	1024		2
	#			mount		mkfs		mkfs
	#			-o			-s			-n
	mkfs.btrfs -f /dev/$1
	mount -t btrfs -w /dev/$1 /home/j/hd3
	chown j /home/j/hd3
}

my_umount() {
	umount -v /dev/sda1
}


ext4_test() {
	#sda1 hdd libaio randrw 50 4
	#3*2*2*3=36
	mkdir -p /home/j/jws/$2_ext4/$3_$4_$5_$6
	for jour in "journal" "ordered" "writeback";do
		for asyn in "journal_async_commit" "no_jac";do
			for dela in "delalloc" "nodelalloc";do
				for bs in "1024" "2048" "4096";do

					ext4_format $1 ${jour} ${asyn} ${dela} ${bs}
					sync
					echo ${jour}_${asyn}_${dela}_${bs}_cohe start
					fio --directory=/home/j/hd3 --name fio_test_file --rw=$4 --bs=$6 --ioengine=$3 --rwmixread=$5 \
						--size=1G --numjobs=1 --time_based --runtime=1 --group_reporting \
						> /home/j/jws/$2_ext4/$3_$4_$5_$6/${jour}_${asyn}_${dela}_${bs}_cohe.txt
					my_umount
					echo "umount complete"

					ext4_format $1 ${jour} ${asyn} ${dela} ${bs}
					sync
					echo ${jour}_${asyn}_${dela}_${bs}_scat start
					fio --directory=/home/j/hd3 --name fio_test_file --rw=$4 --bs=$6 --ioengine=$3 --rwmixread=$5 \
						--size=1m --numjobs=500 --time_based --runtime=1 --group_reporting \
						> /home/j/jws/$2_ext4/$3_$4_$5_$6/${jour}_${asyn}_${dela}_${bs}_scat.txt
					my_umount
					echo "umount complete"

				done
			done
		done
	done
}

f2fs_test() {
	#sda1 hdd libaio randrw 50 4
	#3*2*3*2*2=72
	mkdir -p /home/j/jws/$2_f2fs/$3_$4_$5_$6
	for fsync in "posix" "strict" "nobarrier";do
		for cpoint in "disable" "enable";do
			for secsize in "1024" "2048" "4096";do
				for segpsec in "1" "2";do
					for secpzone in "1" "2";do

						f2fs_format $1 ${fsync} ${cpoint} ${secsize} ${segpsec} ${secpzone}
						sync
						echo ${fsync}_${cpoint}_${secsize}_${segpsec}_${secpzone}_cohe start
						fio --directory=/home/j/hd3 --name fio_test_file --rw=$4 --bs=$6 --ioengine=$3 --rwmixread=$5 \
							--size=1G --numjobs=1 --time_based --runtime=120 --group_reporting \
							> /home/j/jws/$2_f2fs/$3_$4_$5_$6/${fsync}_${cpoint}_${secsize}_${segpsec}_${secpzone}_cohe.txt
						my_umount
						echo "umount complete"

						f2fs_format $1 ${fsync} ${cpoint} ${secsize} ${segpsec} ${secpzone}
						sync
						echo ${fsync}_${cpoint}_${secsize}_${segpsec}_${secpzone}_scat start
						fio --directory=/home/j/hd3 --name fio_test_file --rw=$4 --bs=$6 --ioengine=$3 --rwmixread=$5 \
							--size=1m --numjobs=500 --time_based --runtime=120 --group_reporting \
							> /home/j/jws/$2_f2fs/$3_$4_$5_$6/${fsync}_${cpoint}_${secsize}_${segpsec}_${secpzone}_scat.txt
						my_umount
						echo "umount complete"

					done
				done
			done
		done
	done


}

btrfs_test() {
	#sda1 hdd libaio randrw 50 4
	#2*2*3*3=36
	mkdir -p /home/j/jws/$2_btrfs/$3_$4_$5_$6
	for datacow in "datacow" "nodatacow";do
		for secsize in "1024" "2048" "4096";do
			for nodesize_mul in "1" "2" "4";do
				nodesize=$(${secsize}*${nodesize_mul})

				btrfs_format $1 ${datacow} ${secsize} ${nodesize}
				sync
				echo ${datacow}_${secsize}_${nodesize_mul}_cohe start
				fio --directory=/home/j/hd3 --name fio_test_file --rw=$4 --bs=$6 --ioengine=$3 --rwmixread=$5 \
					--size=1G --numjobs=1 --time_based --runtime=1 --group_reporting \
					> /home/j/jws/$2_btrfs/${io_en}_${rp}_${rr}_${rs}/${datacow}_${secsize}_${nodesize_mul}_cohe.txt
				my_umount
				echo "umount complete"

				btrfs_format $1 ${datacow} ${secsize} ${nodesize}
				sync
				echo ${datacow}_${secsize}_${nodesize_mul}_scat start
				fio --directory=/home/j/hd3 --name fio_test_file --rw=$4 --bs=$6 --ioengine=$3 --rwmixread=$5 \
					--size=1m --numjobs=500 --time_based --runtime=1 --group_reporting \
					> /home/j/jws/$2_btrfs/${io_en}_${rp}_${rr}_${rs}/${datacow}_${secsize}_${nodesize_mul}_scat.txt
				my_umount
				echo "umount complete"

			done
		done
	done

}

fs_test(){
	#3*2*5*3=90
	#90*(36+72+36)=12960
	#12960*20s=72h=3d+alpha
	for io_en in "sync" "libaio" "pvsync2"; do
		for rp in "rw" "randrw"; do
			for rr in "0" "25" "50" "75" "100"; do
				for rs in "4" "32" "128"; do
					${fs}_test $1 $2 ${io_en} ${rp} ${rr} ${rs}
				done
			done
		done
	done
}

test(){
	for fs in "ext4" "btrfs" "f2fs";do
		fs_test $1 $2 ${fs}
	done
}

test "sda1" "hdd"
