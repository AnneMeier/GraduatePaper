import os
import sys
import numpy as np
"""
찾아야하는 정보
R/W 비율,fsync 간격, request size, random or sequential
queue depth를 알 수 있는 지 확인한다.
"""

read_cnt = {"read":0, "pread64":0, "readv":0, "preadv":0, "io_getevents": 0, "preadv2":0}
write_cnt = {"write":0, "pwrite64":0, "writev":0, "pwritev":0, "io_submit": 0, "pwritev2":0}
open_cnt = {"open":0, "openat":0, "io_setup":0}
sync_cnt = {"fsync":0, "sync":0}
lseek_cnt = {"lseek":0, "lseek64":0}
close_cnt = {"close":0, "io_destroy":0}
pid_fd_sync_temp = {}
pid_fd_read_offset = {}
pid_fd_read_offset_before = {}
pid_fd_read_offset_len = {}
pid_fd_write_offset = {}
pid_fd_write_offset_before = {}
pid_fd_write_offset_len = {}
seq_request_size = []
sync_interval = []
pid_file_fd = {}
pid_fd_file = {}
request_size = []
resume_queue = {}
pid_list = []

def remove_character(line, chars="\"\n(),+-:=;"):
    for c in chars:
        line = line.replace(c, " ")
    return line

def resume_process(line):
    global resume_queue
    try:
        pid_=int(line[0])
        saved_line=resume_queue[pid_]
        del resume_queue[pid_]
        saved_line=saved_line[:-2]
        line=line[4:]
        saved_line.extend(line)
        #print(saved_line)
        command_control(saved_line)
    except:
        pass
    return

def unfinished_process(line):
    global resume_queue
    try:
        pid_=int(line[0])
        resume_queue[pid_]=line
    except:
        pass
    return

def pid_dict_intialize(pid_):
    global pid_file_fd, pid_fd_file
    global pid_fd_read_offset, pid_fd_read_offset_len
    global pid_fd_write_offset, pid_fd_write_offset_len
    global seq_request_size

    if not pid_ in pid_file_fd:
        pid_file_fd[pid_]={}
    if not pid_ in pid_fd_file:
        pid_fd_file[pid_]={}
    if not pid_ in pid_fd_read_offset:
        pid_fd_read_offset[pid_]={}
    if not pid_ in pid_fd_read_offset_before:
        pid_fd_read_offset_before[pid_]={}
    if not pid_ in pid_fd_read_offset_len:
        pid_fd_read_offset_len[pid_]={}
    if not pid_ in pid_fd_write_offset:
        pid_fd_write_offset[pid_]={}
    if not pid_ in pid_fd_write_offset_before:
        pid_fd_write_offset_before[pid_]={}
    if not pid_ in pid_fd_write_offset_len:
        pid_fd_write_offset_len[pid_]={}
    if not pid_ in pid_fd_sync_temp:
        pid_fd_sync_temp[pid_]=-1

def open_process(line):
    global pid_file_fd, pid_fd_file
    global pid_fd_read_offset, pid_fd_read_offset_len
    global pid_fd_write_offset, pid_fd_write_offset_len
    global seq_request_size, pid_list

    filename_=line[3]
    comm = line[1]

    try:
        pid_=int(line[0])
        if comm=="io_setup":
            fd_=line[3]
        else:
            fd_=int(line[-1])
    except:
        return

    if not pid_ in pid_list:
        pid_dict_intialize(pid_)
        pid_list=np.append(pid_list, pid_)

    pid_file_fd[pid_][filename_]=fd_
    pid_fd_file[pid_][fd_]=filename_
    if "O_APPEND" in line:
        file_stat = os.stat(filename_)
        pid_fd_read_offset[pid_][fd_]=file_stat.st_size
        pid_fd_write_offset[pid_][fd_]=file_stat.st_size
    else:
        pid_fd_read_offset[pid_][fd_]=0
        pid_fd_write_offset[pid_][fd_]=0

    if fd_ in pid_fd_read_offset[pid_] and fd_ in pid_fd_read_offset_len[pid_] and pid_fd_read_offset_len[pid_][fd_]>=1:
        seq_request_size=np.append(seq_request_size, pid_fd_read_offset_len[pid_][fd_])
    pid_fd_read_offset_len[pid_][fd_]=0
    pid_fd_read_offset_before[pid_][fd_]=pid_fd_read_offset[pid_][fd_]

    if fd_ in pid_fd_write_offset[pid_] and fd_ in pid_fd_write_offset_len[pid_] and pid_fd_write_offset_len[pid_][fd_]>=1:
        seq_request_size=np.append(seq_request_size, pid_fd_write_offset_len[pid_][fd_])
    pid_fd_write_offset_len[pid_][fd_]=0
    pid_fd_write_offset_before[pid_][fd_]=pid_fd_write_offset[pid_][fd_]

def close_process(line):
    global pid_file_fd
    global pid_fd_file

    comm=line[1]

    try:
        pid_=int(line[0])
        if comm=="io_destroy":
            fd_=line[2]
        else:
            fd_=int(line[2])
        filename_=pid_fd_file[pid_][fd_]
        del pid_file_fd[pid_][filename_]
        del pid_fd_file[pid_][fd_]
    except:
        pass

    return

def read_process(line):
    global request_size
    global pid_fd_read_offset, pid_fd_read_offset_before
    global pid_fd_read_offset_len, seq_request_size
    comm=line[1]
    fd_=line[2]

    try:
        pid_=int(line[0])
    except:
        return
    if comm=="io_getevents":
        pass
    else:
        try:
            fd_=int(fd_)
        except:
            fd_=0
        if(fd_<3):#stdio
            return
    try:
        if comm=="io_getevents":
            r_byte=int(line[-5])
        else:
            r_byte=int(line[-1])
    except:
        print(line)
        r_byte=0
    if(r_byte>0):
        if comm=='pread64':
            try:
                pid_fd_read_offset[pid_][fd_]=int(line[-2])
            except:
                pid_fd_read_offset[pid_][fd_]=-1
        elif comm=='preadv2':
            try:
                pid_fd_read_offset[pid_][fd_]=int(line[-3])
            except:
                pid_fd_read_offset[pid_][fd_]=-1
        #print("r", pid_fd_read_offset_before[pid_][fd_],pid_fd_read_offset[pid_][fd_])
        if pid_fd_read_offset_before[pid_][fd_]==pid_fd_read_offset[pid_][fd_]:
            pid_fd_read_offset_len[pid_][fd_]+=r_byte
        else:
            if pid_fd_read_offset_len[pid_][fd_]>=1:
                #print(pid_fd_read_offset_len[pid_][fd_], line)
                seq_request_size = np.append(seq_request_size, pid_fd_read_offset_len[pid_][fd_])
            pid_fd_read_offset_len[pid_][fd_]=r_byte
        pid_fd_read_offset[pid_][fd_]+=r_byte
        pid_fd_read_offset_before[pid_][fd_]=pid_fd_read_offset[pid_][fd_]
        request_size=np.append(request_size, r_byte)
    return

def write_process(line):
    global request_size
    global pid_fd_sync_temp
    global pid_fd_write_offset, pid_fd_write_offset_len, seq_request_size
    comm=line[1]
    fd_=line[2]

    try:
        pid_=int(line[0])
    except:
        return
    if comm=="io_submit":
        pass
    else:
        try:
            fd_=int(fd_)
        except:
            fd_=0
        if(fd_<3):#stdio인 경우
            return

    if pid_fd_sync_temp[pid_]>=0:
        pid_fd_sync_temp[pid_]+=1

    try:
        if comm=="io_submit":
            w_byte=int(line[-4])
        else:
            w_byte=int(line[-1])
    except:
        print(line)
        w_byte=0
    if(w_byte>0):
        if comm=='pwrite64':
            try:
                pid_fd_write_offset[pid_][fd_]=int(line[-2])
            except:
                pid_fd_write_offset[pid_][fd_]=0
        elif comm=='pwritev2':
            try:
                pid_fd_write_offset[pid_][fd_]=int(line[-3])
            except:
                pid_fd_write_offset[pid_][fd_]=0
        #print("w", pid_fd_write_offset_before[pid_][fd_],pid_fd_write_offset[pid_][fd_])
        if pid_fd_write_offset_before[pid_][fd_]==pid_fd_write_offset[pid_][fd_]:
            pid_fd_write_offset_len[pid_][fd_]+=w_byte
        else:
            if pid_fd_write_offset_len[pid_][fd_]>=1:
                #print(pid_fd_write_offset_len[pid_][fd_], line)
                seq_request_size = np.append(seq_request_size, pid_fd_write_offset_len[pid_][fd_])
            pid_fd_write_offset_len[pid_][fd_]=w_byte
        pid_fd_write_offset[pid_][fd_]+=w_byte
        pid_fd_write_offset_before[pid_][fd_]=pid_fd_write_offset[pid_][fd_]
        request_size=np.append(request_size, w_byte)
    return

def pop_remain_():
    global pid_fd_read_offset_len ,pid_fd_write_offset_len, seq_request_size
    for pid_ in pid_fd_read_offset_len:
        for fd_ in pid_fd_read_offset_len[pid_]:
            if pid_fd_read_offset_len[pid_][fd_]>=1:
                seq_request_size = np.append(seq_request_size, pid_fd_read_offset_len[pid_][fd_])
                pid_fd_read_offset_len[pid_][fd_]=0
    for pid_ in pid_fd_write_offset_len:
        for fd_ in pid_fd_write_offset_len[pid_]:
            if pid_fd_write_offset_len[pid_][fd_]>=1:
                seq_request_size = np.append(seq_request_size, pid_fd_write_offset_len[pid_][fd_])
                pid_fd_write_offset_len[pid_][fd_]=0

def sync_process(line):
    global sync_interval, pid_fd_sync_temp
    comm=line[1]
    try:
        pid_=int(line[0])
    except:
        return
    if(comm=="sync"):
        fd_=0
    elif(comm=="fsync"):
        try:
            fd_=int(line[2])
        except:
            return
    if pid_ in pid_fd_sync_temp and pid_fd_sync_temp[pid_]>=1:
        sync_interval=np.append(sync_interval, pid_fd_sync_temp[pid_])
    pid_fd_sync_temp[pid_]=0

def lseek_process(line):
    global pid_fd_read_offset_before, pid_fd_write_offset_before
    try:
        pid_=int(line[0])
        fd_=int(line[2])
        offset_=int(line[3])
        pid_fd_read_offset[pid_][fd_]=offset_
        pid_fd_write_offset[pid_][fd_]=offset_
    except:
        return

def command_control(line):
    comm = line[1]

    if comm in sync_cnt:
        sync_cnt[comm]+=1
        sync_process(line)

    elif comm in read_cnt:
        if line[-1]=="...>":
            unfinished_process(line)
        else:
            read_cnt[comm]+=1
            read_process(line)

    elif comm in write_cnt:
        if line[-1]=="...>":
            unfinished_process(line)
        else:
            write_cnt[comm]+=1
            write_process(line)

    elif comm in open_cnt:
        if line[-1]=="...>":
            unfinished_process(line)
        open_cnt[comm]+=1
        open_process(line)

    elif comm == "close":
        close_cnt[comm]+=1
        close_process(line)

    elif comm in lseek_cnt:
        lseek_cnt[comm]+=1
        lseek_process(line)

    elif comm=="<...":
        resume_process(line)

def parser():
    global read_cnt, write_cnt, open_cnt, pid_file_fd, pid_fd_file
    global request_size, resume_queue

    filename='./result_fio_2/'+sys.argv[1]
    print("\n\n", filename, "\n")
    fr = open(filename, 'r')

    #pread preadv는 offset 상관없이
    #read readv는 현재 offset위치에 따라
    #open할 때 옵션을 보고 offset위치 확인
    #fibmap으로 lba확인

    #sendfile, lseek, stat 등등의 함수는?
    #sudo hdparm --fibmap filename

    while True:
        line = fr.readline()
        if not line: break;
        line = remove_character(line, "\n\"\n(){}[],+:=|")
        line = line.split(" ")
        line = list(filter(None, line))
        command_control(line)

    pop_remain_()

    fr.close()
    print(pid_fd_write_offset_len)
    #print(seq_request_size)
    print(read_cnt)
    print(write_cnt)
    print(open_cnt)
    print(sync_cnt)
    print(pid_file_fd)
    print(pid_fd_file)
    if np.size(request_size):
        print("request size     (mean, std, size):",np.mean(request_size), np.std(request_size), np.size(request_size))
    if np.size(sync_interval):
        print("sync interval    (mean, std, size):",np.mean(sync_interval), np.std(sync_interval), np.size(sync_interval))
    if np.size(seq_request_size):
        print("seq request size (mean, std, size):",np.mean(seq_request_size), np.std(seq_request_size), np.size(seq_request_size))
        seq_128H=seq_request_size[np.where(seq_request_size>=130000)]
        seq_128L=seq_request_size[np.where(seq_request_size<130000)]
        print("seq, rand", np.size(seq_128H), np.size(seq_128L))
        print("seq vs rand:",np.sum(seq_128H)/1024,"KB /",np.sum(seq_128L)/1024,"KB")
if __name__=="__main__":
    parser()
