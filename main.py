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

rneeddate = {}
rneed = []
rneedstate = {}
i = 0
pp = 0
while pp != 2:
    pp += 1
    for key, value in data[fuserid].items():
        for smt, need in value.items():
            if need > 3600:
                rneedstate[smt] = 3600
                rneed.append(need)
                key = datetime.strptime(key, '%Y-%m-%d %H')
                rneeddate[key] = key
                while need > 3600:
                    need -= 3600

    for l in rneeddate:
        groups = np.arange(rneeddate[l], lcdate, timedelta(hours=1)).astype(datetime)
        try:
            while rneed[i] > 3600:
                rneed[i] -= 3600
                grp_key = time_group(groups[i])
                data[fuserid][grp_key] = rneedstate
                this_group = data[fuserid][grp_key]
                i += 1
        except IndexError:
            continue

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
fuser_rest_values = [
    data[fuserid].get(time_group(time), {}).get('Rest', 0) / 60
    for time in xticks
]
fuser_loggedout_values = [
    data[fuserid].get(time_group(time), {}).get('LoggedOut', 0) / 60
    for time in xticks
]
fuser_na_values = [
    data[fuserid].get(time_group(time), {}).get('NA', 0) / 60
    for time in xticks
]
fuser_servicebreak_values = [
    data[fuserid].get(time_group(time), {}).get('ServiceBreak', 0) / 60
    for time in xticks
]
fuser_dinner_values = [
    data[fuserid].get(time_group(time), {}).get('Dinner', 0) / 60
    for time in xticks
]

busy = plt.bar(xvals, fuser_busy_values, 0.9)
ready = plt.bar(xvals, fuser_ready_values, 0.9, bottom=fuser_busy_values)
rest = plt.bar(xvals, fuser_rest_values, 0.9, bottom=fuser_ready_values)
loggedout = plt.bar(xvals, fuser_loggedout_values, 0.9, bottom=fuser_rest_values)
dinner = plt.bar(xvals, fuser_dinner_values, 0.9, bottom=fuser_loggedout_values)
servicebreak = plt.bar(xvals, fuser_servicebreak_values, 0.9, bottom=fuser_dinner_values)
na = plt.bar(xvals, fuser_na_values, 0.9, bottom=fuser_servicebreak_values)
plt.legend((busy[0], ready[0], rest[0], loggedout[0], dinner[0], servicebreak[0], na[0]),
           ('Занят', 'Готов', 'Отдых', 'Вышел', 'Обед', 'тех.перерыв', '-'))

plt.show()
