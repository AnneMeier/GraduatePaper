## sh folder

실험을 진행하기 위한 shell script file

***
#### files

setting.sh : 실험을 진행하기 위해 관리자 권한으로 memory cache 비우기<br>
mount_ext4_journal.sh : ext4 file system의 journal option을 journal로 mount<br>
mount_ext4_ordered.sh : ext4 file system의 journal option을 ordered로 mount<br>
mount_ext4_writeback.sh : ext4 file system의 journal option을 writeback으로 mount<br>
mount_xfs.sh : xfs file system을 mount<br>
umount.sh : filesystem을 umount<br>
umount_busy : filesystem을 사용하는 process가 있는 경우 kill하고 umount<br>
<br>
0704.sh : filebench의 fileserver workload/ journal option, lazy initialize, delayed allocation option/ throughput 실험<br>
0708.sh : filebench의 varmail workload/ journal option, lazy initialize, delayed allocation 옵션/ throughput 실험<br>
0709.sh : filebench의 webserver workload/ journal option, lazy initialize, delayed allocation 옵션/ throughput 실험<br>
