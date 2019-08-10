from collections import defaultdict

file_list = {'result_r.txt', 'result_rr.txt', 'result_rw.txt', 'result_w.txt'}

dics = defaultdict(list)

for file_name in file_list:
    fr = open('./' + file_name, 'r')
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
        line = line.replace("<", "")
        line = line.replace(">", "")
        line = line.replace(".", "")
        line = line.split(" ")
        line = filter(None, line)
        line = list(line)
        key = line[1]
        if key in dic:
            dic[key] += 1
        else:
            dic[key] = 1
    print(file_name)
    print(dic)
    for key in dic:
        if key in dics:
            dics[key] = dics[key] + [dic[key]]
        else:
            dics[key] = []
            dics[key] = dics[key] + [dic[key]]

    fr.close()

for dic in dics:
    print(dic, ':', dics[dic])
#fw.close()
