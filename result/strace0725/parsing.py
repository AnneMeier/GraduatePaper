fr = open('./result_r.txt', 'r')
fw = open('./result_r_p.txt', 'w')

while True:
    line = fr.readline()
    if not line: break;
    line = line.replace("\"", " ")
    line = line.replace("(", " ")
    line = line.replace(")", " ")
    line = line.replace(",", " ")
    line = line.replace("\n", "")
    line = line.split(" ")
    line = filter(None, line)
    line = list(line)
    if line[1]=='openat':
        print(line[3])
    if line[1]=='write':
        print(line[-1])

fr.close()
fw.close()
