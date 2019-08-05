
qds = ["1","2","4","8","16","32","64"]
rss = ["1","4","8","16","32","64","128"]
rps = ["rw","randrw"]
rrs = ["0","5","25","50","75","95","100"]
sum=0
flag=1
for k, rp in enumerate(rps):
    for l, rr in enumerate(rrs):
        for i, qd in enumerate(qds):
            for j, rs in enumerate(rss):
                filename = qd+"_"+rs+"_"+rp+"_"+rr+".txt"
                fr = open('./result/' + filename, 'r')
                #fw = open('../result/strace/result_r_p.txt', 'w')
                dic = {}
                while True:
                    line = fr.readline()
                    if not line: break;
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
                            s=int(float(line[2][0:4])*1000)
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
