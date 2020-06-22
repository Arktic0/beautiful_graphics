from datetime import datetime
from collections import defaultdict

filename = str(input("путь:"))
fdate = str(input("начальная дата:"))
ldate = str(input("конечная дата:"))

cdict = defaultdict(list)
fcdate = datetime.strptime(fdate, '%Y-%m-%d').date()
lcdate = datetime.strptime(ldate, '%Y-%m-%d').date()

fuserid = str(input('1 id:'))
suserid = str(input('2 id:'))

with open(filename, 'r') as file:
    for ln in file:
        ln = ln.split(",")
        ln[1] = ln[1].strip('\n')
        ln[1] += "00"
        try:
            ctime = datetime.strptime(ln[1], '%Y-%m-%d %H:%M:%S.%f%z')
        except ValueError:
            ctime = datetime.strptime(ln[1], '%Y-%m-%d %H:%M:%S%z')
        if ln[0] == fuserid:
            if fcdate <= ctime.date() <= lcdate:
                cdict[ln[0]].append(ln[1])
        if ln[0] == suserid:
            if fcdate <= ctime.date() <= lcdate:
                cdict[ln[0]].append(ln[1])

print(cdict)
