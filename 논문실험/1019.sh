strace -f -o result1.strace fio --directory=/home/j/hd3 --name fio_test_file1 \
--ioengine=pvsync2 --fsync=1000 --rw=rw --rwmixread=0 --bs=16 \
--size=1G --numjobs=1 --time_based --runtime=60 --group_reporting

strace -f -o result2.strace fio --directory=/home/j/hd3 --name fio_test_file2 \
--ioengine=libaio --fsync=10 --rw=randrw --rwmixread=50 --bs=4 \
--size=10m --numjobs=100 --time_based --runtime=60 --group_reporting

strace -f -o result3.strace fio --directory=/home/j/hd3 --name fio_test_file3 \
--ioengine=sync --fsync=0 --rw=randrw --rwmixread=75 --bs=64 \
--size=1m --numjobs=1000 --time_based --runtime=60 --group_reporting
