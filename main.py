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
users = [fuserid, suserid]

with open(filename, 'r') as file:
    for ln in file:
        ln = ln.split(",")
        ln[1] = ln[1].strip('\n')
        ln[1] += "00"
        try:
            ctime = datetime.strptime(ln[1], '%Y-%m-%d %H:%M:%S.%f%z')
        except ValueError:
            ctime = datetime.strptime(ln[1], '%Y-%m-%d %H:%M:%S%z')
        if ln[4] in users and fcdate <= ctime.date() <= lcdate:
            row = {
                "userId": ln[4],
                "state": ln[2],
                "ctime": ctime
            }
            cdict[row["userId"]].append(row)

print(len(cdict[fuserid]))
print(len(cdict[suserid]))
