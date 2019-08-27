ext4_test1() {
	for io_en in "sync"; do
		for fsync in "0" "100" "1000"; do
			for rp in "rw" "randrw"; do
				for rr in "0" "25" "50" "100"; do
					python3 parser.py ${io_en}"_"${fsync}"_"${rp}"_"${rr}".txt"
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
					python3 parser.py ${io_en}"_"${fsync}"_"${rp}"_"${rr}".txt"
				done
			done
		done
	done
}

ext4_test2

ext4_test1
