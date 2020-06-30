from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

filename = str(input("путь:"))
fdate = str(input("начальная дата:"))
ldate = str(input("конечная дата:"))

fcdate = datetime.strptime(fdate, '%Y-%m-%d').date()
lcdate = datetime.strptime(ldate, '%Y-%m-%d').date()

fuserid = str(input('1 id:'))
suserid = str(input('2 id:'))
users = [fuserid, suserid]

def parse_time(s):
    s = s.strip(' \n[)"') + "00"
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f%z')
    except ValueError:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S%z')


def time_group(dt):
    return dt.strftime('%Y-%m-%d')


data = {}
with open(filename, 'r') as file:
    for ln in file:
        ln = ln.split(",")
        ctime = parse_time(ln[1])
        user_id = ln[4]
        state = ln[2]
        if user_id in users and fcdate <= ctime.date() <= lcdate:
            state_range = 0
            if len(ln) > 5:
                state_range = parse_time(ln[6]) - parse_time(ln[5])
            z = data.setdefault(user_id, {})
            z = z.setdefault(time_group(ctime), {})
            z = z.setdefault(state, [])
            z.append({"ctime": ctime, "crange": state_range})

#states = data[fuserid]['2020-05-22']
#for s in states.items():
#    print(s)
#raz = lcdate - fcdate
#print(raz.days)
sr = state_range.seconds / 3600
x = np.arange(fcdate, lcdate)
y = np.float(sr)
print(state_range)
fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_facecolor('white')
fig.set_figwidth(12)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure
fig.set_facecolor('white')
plt.show()
