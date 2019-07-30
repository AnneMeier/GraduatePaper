strace -o result_r.txt sudo ./fio_r.sh
strace -c -o result_r_c.txt sudo ./fio_r.sh
strace -o result_rr.txt sudo ./fio_rr.sh
strace -c -o result_rr_c.txt sudo ./fio_rr.sh
strace -o result_w.txt sudo ./fio_w.sh
strace -c -o result_w_c.txt sudo ./fio_w.sh
strace -o result_rw.txt sudo ./fio_rw.sh
strace -c -o result_rw_c.txt sudo ./fio_rw.sh

