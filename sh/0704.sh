ext4_format() {
	echo $1"//"$2"//"$3
	mkfs.ext4 -F -E $3 /dev/sdc3
	mount -t ext4 -o $2,data=$1 -w /dev/sdc3 /home/j/hd3
	chown j /home/j/hd3
}

ext4_umount() {
	umount -v /dev/sdc3
}

ext4_test() {
	for jour_opt in "ordered" "writeback" "journal"; do
		for ext4_opt in "dolo" "dolx" "dxlo" "dxlx"; do
		#delayed allocation on/off, lazy init on/off
			case ${ext4_opt} in
				dolo)
					dlyd_opt="delalloc"
					lzy_opt="lazy_itable_init=1,lazy_journal_init=1"
					;;
				dolx)
					dlyd_opt="delalloc"
					lzy_opt="lazy_itable_init=0,lazy_journal_init=0"
					;;
				dxlo)
					dlyd_opt="nodelalloc"
					lzy_opt="lazy_itable_init=1,lazy_journal_init=1"
					;;
				dxlx)
					dlyd_opt="nodelalloc"
					lzy_opt="lazy_itable_init=0,lazy_journal_init=0"
					;;
			esac
			
			case ${jour_opt} in
				journal)
					dlyd_opt="nodelalloc"
				;;
			esac

			echo ${jour_opt}"_"${ext4_opt}
			ext4_format ${jour_opt} ${dlyd_opt} ${lzy_opt}
			cp -r /home/j/cp/* /home/j/hd3
			sync
			filebench -f /home/j/hd3/fileserver/fileserver.f > "/home/j/result/fileserver/"${jour_opt}"_"${ext4_opt}".txt"
			ext4_umount
			echo "umount complete"

		done
	done
}

ext4_test
