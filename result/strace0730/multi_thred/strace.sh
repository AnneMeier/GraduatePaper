strace -f -v -o result_r.txt sudo ./fio_r.sh
strace -f -v -c -o result_r_c.txt sudo ./fio_r.sh
strace -f -v -o result_rr.txt sudo ./fio_rr.sh
strace -f -v -c -o result_rr_c.txt sudo ./fio_rr.sh
strace -f -v -o result_w.txt sudo ./fio_w.sh
strace -f -v -c -o result_w_c.txt sudo ./fio_w.sh
strace -f -v -o result_rw.txt sudo ./fio_rw.sh
strace -f -v -c -o result_rw_c.txt sudo ./fio_rw.sh

