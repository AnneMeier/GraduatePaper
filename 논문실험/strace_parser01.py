drives = ["hdd", "ssd"]
fss = ["ext4","f2fs","btrfs"]
ios = ["sync", "pvsync2", "libaio"]
rps = ["rw","randrw"]
rss = ["4","32","128"]
rrs = ["0","25","50","75","100"]
sum=0
flag=1
for i, drive in enumerate(drives):
    for j, fs in enumerate(fss):
        for k, io in enumerate(ios):
            for l, rp in enumerate(rps):
                print(drive, fs, io, rp)
                for m, rs in enumerate(rss):
                    for n, rr in enumerate(rrs):
                        filename = "./"+drive+"_"+fs+"_result/"+io+"_"+rp+"_"+rr+"_"+rs
                        fr = open(filename, 'r')
                        #fw = open('../result/strace/result_r_p.txt', 'w')
                        dic = {}
                        while True:
                            line = fr.readline()
                            if not line:
                                break
                            line = line.replace("\"", " ")
                            line = line.replace("(", " ")
                            line = line.replace(")", " ")
                            line = line.replace(",", " ")
                            line = line.replace("\n", "")
                            line = line.replace("+", "")
                            line = line.replace("-", "")
                            line = line.replace(":", "")
                            line = line.replace("=", " ")
                            line = line.split(" ")
                            line = filter(None, line)
                            line = list(line)
                            if not line:
                                continue
                            if line[0]=='write' or line[0]=='read':
                                if line[2][-1]=='k':
                                    s=int(float(line[2][0:-1])*1000)
                                else:
                                    s=int(line[2])
                                if line[0]=='read' and rr!='0' and rr!='100':
                                    sum+=s
                                    flag=1
                                elif flag==1:
                                    print(sum+s)
                                    sum=0
                                    flag=0
                                else:
                                    print(s)
                        fr.close()
                    print("---------------------")
                print("=====================")
#fw.close()
