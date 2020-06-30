from datetime import datetime, timedelta
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
    return dt.strftime('%Y-%m-%d %H')


data = {}
with open(filename, 'r') as file:
    for ln in file:
        ln = ln.split(",")
        ctime = parse_time(ln[1])
        user_id = ln[4]
        state = ln[2]
        if user_id in users and fcdate <= ctime.date() <= lcdate:
            state_range = None
            if len(ln) > 6:
                state_range = parse_time(ln[6]) - parse_time(ln[5])
            z = data.setdefault(user_id, {})
            z = z.setdefault(time_group(ctime), {})
            z.setdefault(state, 0)
            if state_range:
                z[state] += state_range.seconds


xticks = np.arange(fcdate, lcdate, timedelta(hours=1)).astype(datetime)
subsampled_xticks = map(lambda t: t.strftime("%m-%d"), xticks[0::24])
xvals = np.arange(len(xticks))
plt.xticks(xvals[0::24], subsampled_xticks)

plt.ylabel("Минуты")
plt.yticks(np.arange(0, 70, 10))

fuser_busy_values = [
    data[fuserid].get(time_group(time), {}).get('Busy', 0) / 60
    for time in xticks
]
fuser_ready_values = [
    data[fuserid].get(time_group(time), {}).get('Ready', 0) / 60
    for time in xticks
]

busy = plt.bar(xvals, fuser_busy_values, 0.9)
ready = plt.bar(xvals, fuser_ready_values, 0.9, bottom=fuser_busy_values)
plt.legend((busy[0], ready[0]), ('Занят', 'Готов'))

plt.show()
