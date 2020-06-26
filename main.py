from datetime import datetime
from collections import defaultdict

filename = str(input("путь:"))
fdate = str(input("начальная дата:"))
ldate = str(input("конечная дата:"))

fcdate = datetime.strptime(fdate, '%Y-%m-%d').date()
lcdate = datetime.strptime(ldate, '%Y-%m-%d').date()

fuserid = str(input('1 id:'))
suserid = str(input('2 id:'))
users = [fuserid, suserid]


def parse_time(s):
    s = s.strip(' \n') + "00"
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f%z')
    except ValueError:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S%z')


def time_group(dt):
    return dt.strftime('%Y-%m-%d %H')


data = {}
with open(filename, 'r') as file:
    for ln in file:
        ln = ln.split(",")

        ctime = parse_time(ln[1])
        user_id = ln[4]
        state = ln[2]
        state_range = None
        if len(ln) > 5:
            state_range = ln[5] # TODO: parse time range

        if user_id in users and fcdate <= ctime.date() <= lcdate:
            z = data.setdefault(user_id, {})
            z = z.setdefault(time_group(ctime), {})
            z = z.setdefault(state, [])
            z.append({"ctime": ctime, "range": state_range})


states = data[fuserid]['2017-03-13 17']
for s in states.items():
    print(s)
