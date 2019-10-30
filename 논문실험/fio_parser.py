def fio_parsing(filename, rr):
    fr = open(filename, 'r')
    #fw = open('../result/strace/result_r_p.txt', 'w')
    dic = {}
    throughput = 0
    sum=0
    flag=1

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
            elif line[2][-1]=='M':
                s=int(float(line[2][0:-1])*1000000)
            else:
                s=int(line[2])
            if line[0]=='read' and rr!='0' and rr!='100':
                sum+=s
                flag=1
            elif flag==1:
                throughput=sum+s
                sum=0
                flag=0
            else:
                throughput=s
    fr.close()
    return throughput

def fios_parsing(foldername):
    io_ens = ["sync", "libaio", "pvsync2"]
    rps = ["rw", "randrw"]
    rrs = ["0", "25", "50", "75", "100"]
    rss = ["4", "32", "128"]

    for io_en in io_ens:
        for rp in rps:
            for rr in rrs:
                for rs in rss:
                    filename=io_en+"_"+rp+"_"+rr+"_"+rs+"_cohe.txt"
                    cohe_out=fio_parsing(foldername+filename, rr)
                    filename=io_en+"_"+rp+"_"+rr+"_"+rs+"_scat.txt"
                    scat_out=fio_parsing(foldername+filename, rr)
                    print(cohe_out, scat_out)

def ext4_parsing():
    drives = ["hdd", "ssd"]
    jours = ["journal", "ordered", "writeback"]
    asyns = ["jac", "nojac"]
    delas = ["delalloc", "nodelalloc"]
    bss = ["1024", "2048", "4096"]

    for drive in drives:
        for jour in jours:
            for asyn in asyns:
                for dela in delas:
                    for bs in bss:
                        foldername1 = "/home/j/jws/result/"+drive+"_ext4/"
                        foldername2 = jour+"_"+asyn+"_"+dela+"_"+bs+"/"
                        print(drive, foldername2)
                        fios_parsing(foldername1+foldername2)

def f2fs_parsing():
    drives = ["hdd", "ssd"]
    fsyncs = ["posix", "strict", "nobarrier"]
    cpoints = ["disable", "enable"]
    segpsecs = ["1", "2", "4"]
    secpzones = ["1", "2", "4"]

    for drive in drives:
        for fsync in fsyncs:
            for cpoint in cpoints:
                for segpsec in segpsecs:
                    for secpzone in secpzones:
                        foldername1 = "/home/j/jws/result/"+drive+"_f2fs/"
                        foldername2 = fsync+"_"+cpoint+"_"+segpsec+"_"+secpzone+"/"
                        print(drive, foldername2)
                        fios_parsing(foldername1+foldername2)

def btrfs_parsing():
    drives = ["hdd", "ssd"]
    datacows = ["datacow", "nodatacow"]
    secsizes = ["1024", "2048", "4096"]
    nodesizes = ["4096", "8192", "16384"]

    for drive in drives:
        for datacow in datacows:
            for secsize in secsizes:
                for nodesize in nodesizes:
                    foldername1 = "/home/j/jws/result/"+drive+"_btrfs/"
                    foldername2 = datacow+"_"+secsize+"_"+nodesize+"/"
                    print(drive, foldername2)
                    fios_parsing(foldername1+foldername2)

def fio_parsing2():
    cohes = ["cohe", "scat"]
    io_ens = ["sync", "libaio", "pvsync2"]
    rps = ["rw", "randrw"]
    rrs = ["0", "25", "50", "75", "100"]
    rss = ["4", "32", "128"]

    for cohe in cohes:
        for io_en in io_ens:
            for rp in rps:
                for rr in rrs:
                    for rs in rss:
                        filename=io_en+"_"+rp+"_"+rr+"_"+rs+"_"+cohe+".txt"
                        print(filename)
                        #ext4_parsing2(filename, rr)
                        f2fs_parsing2(filename, rr)
                        #btrfs_parsing2(filename, rr)

def ext4_parsing2(filename, rr):
    drives = ["hdd", "ssd"]
    jours = ["journal", "ordered", "writeback"]
    asyns = ["jac", "nojac"]
    delas = ["delalloc", "nodelalloc"]
    bss = ["1024", "2048", "4096"]

    for drive in drives:
        for jour in jours:
            for asyn in asyns:
                for dela in delas:
                    for bs in bss:
                        foldername1 = "/home/j/jws/result/"+drive+"_ext4/"
                        foldername2 = jour+"_"+asyn+"_"+dela+"_"+bs+"/"
                        out = fio_parsing(foldername1+foldername2+filename, rr)
                        print(out)

def f2fs_parsing2(filename, rr):
    drives = ["hdd", "ssd"]
    fsyncs = ["posix", "strict", "nobarrier"]
    cpoints = ["disable", "enable"]
    segpsecs = ["1", "2", "4"]
    secpzones = ["1", "2", "4"]

    for drive in drives:
        for fsync in fsyncs:
            for cpoint in cpoints:
                for segpsec in segpsecs:
                    for secpzone in secpzones:
                        foldername1 = "/home/j/jws/result/"+drive+"_f2fs/"
                        foldername2 = fsync+"_"+cpoint+"_"+segpsec+"_"+secpzone+"/"
                        out = fio_parsing(foldername1+foldername2+filename, rr)
                        print(out)

def btrfs_parsing2(filename, rr):
    drives = ["hdd", "ssd"]
    datacows = ["datacow", "nodatacow"]
    secsizes = ["1024", "2048", "4096"]
    nodesizes = ["4096", "8192", "16384"]

    for drive in drives:
        for datacow in datacows:
            for secsize in secsizes:
                for nodesize in nodesizes:
                    foldername1 = "/home/j/jws/result/"+drive+"_btrfs/"
                    foldername2 = datacow+"_"+secsize+"_"+nodesize+"/"
                    out = fio_parsing(foldername1+foldername2+filename, rr)
                    print(out)

fio_parsing2()
#ext4_parsing()
#f2fs_parsing()
#btrfs_parsing()
