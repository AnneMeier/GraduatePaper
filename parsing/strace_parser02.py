fr = open('./result_w.txt', 'r')

while True:
    line = fr.readline()
    if not line: break;
    line = line.replace("\"", " ")
    line = line.replace("(", " ")
    line = line.replace(")", " ")
    line = line.replace(",", " ")
    line = line.replace("\n", "")
    line = line.replace(",", "")
    line = line.split(" ")
    line = filter(None, line)
    line = list(line)
    if line[1]=='pread64':
        print(line[-3], line[-4])
    if line[1]=='pwrite64':
        print(line[-3], line[-4])

fr.close()
