import os
import numpy as np
"""
찾아야하는 정보
R/W 비율, R/W 종류, fsync 여부, request size, device 종류, random or sequential를 파악한다.
queue depth를 알 수 있는 지 확인한다.
"""

def remove_character(line, chars="\"\n(),+-:=;"):
    for c in chars:
        line = line.replace(c, " ")
    return line

def parser():
    filename='./fileserver_result.txt'
    fr = open(filename, 'r')

    #pread preadv는 offset 상관없이
    #read readv는 현재 offset위치에 따라
    #open할 때 옵션을 보고 offset위치 확인
    #fibmap으로 lba확인

    read_cnt = {"read":0, "pread64":0, "readv":0, "preadv":0}
    write_cnt = {"write":0, "pwrite64":0, "writev":0, "pwritev":0}
    open_cnt = {"open":0, "openat":0}
    file_fd = {}
    fd_file = {}
    fd_offset = {}
    fd_lba = {}
    #file fibmap
    file_fm = {}
    rs = []

    #sendfile, lseek, stat 등등의 함수는?
    #sudo hdparm --fibmap filename

    while True:
        line = fr.readline()
        if not line: break;
        line = remove_character(line, "\n\"\n(){}[],+:=|")
        line = line.split(" ")
        line = list(filter(None, line))
        comm = line[1]
        if comm in read_cnt:
            read_cnt[comm]+=1
            fd_=line[2]
            if(int(fd_)<3):
                continue
            try:
                r_byte=int(line[-1])
            except:
                #read error인 경우 숫자가 아님
                r_byte=-1
            if(r_byte>0):
                rs=np.append(rs, r_byte)
                fd_offset[fd_]+=rs
        elif comm in write_cnt:
            write_cnt[comm]+=1
            fd_=line[2]
            if(int(fd_)<3):
                #stdio인 경우
                continue
            try:
                w_byte=int(line[-1])
            except:
                #write error인 경우 숫자가 아님
                w_byte=-1
            if(w_byte>0):
                rs=np.append(rs, w_byte)
                fd_offset[fd_]+=rs
        elif comm in open_cnt:
            #print(line)
            open_cnt[comm]+=1
            filename_=line[3]
            fd_=line[-1]
            file_fd[filename_]=fd_
            if fd_ in fd_file:
                filename_=fd_file[fd_]
                del file_fd[filename_]
            fd_file[fd_]=filename_
            if "O_APPEND" in line:
                fd_offset[fd_]=-1
            else:
                fd_offset[fd_]=0

            result = os.popen("hdparm --fibmap "+filename_).read()
            line = remove_character(result)
            line = line.split(" ")
            line = list(filter(None, line))
            fd_lba[fd_]=line[16:]

        elif comm == "close":
            fd_=line[2]
            filename_=fd_file[fd_]
            del file_fd[filename_]
            del fd_file[fd_]

    fr.close()
    print(read_cnt)
    print(write_cnt)
    print(open_cnt)
    print(file_fd)
    print(fd_file)
    print("request mean, std, size:",np.mean(rs), np.std(rs), np.size(rs))
if __name__=="__main__":
    parser()
