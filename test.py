# This function will read list of health center from a text file and store it in two different array of health center name and their assigned code.

import shlex
f = open('list.txt')
dic = {}
for line in f:
    line = shlex.split(line.strip())
    dic[line[1]] = line[2]
f.close()
print dic["pal"]