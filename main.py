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

#
l = 0
fs = []
kucha = {}
allraz = {}
print('data1:', data[fuserid])

# Overflow
for key, value in data[fuserid].items():
    lneed = []
    while l == 0:
        rkey = datetime.strptime(key, '%Y-%m-%d %H')
        l += 1
    for smt, need in value.items():
        if need < 3600:
            lneed.append(need)
        if sum(lneed) > 3600:
            lneed.sort()
            data[fuserid][key].update({smt: need + 3600 - sum(lneed)})
            allraz[key] = {smt: sum(lneed) - 3600}
        if need > 3600:
            if len(lneed) != 0:
                allraz[key] = {smt: need - (3600 - sum(lneed))}
                data[fuserid][key].update({smt: 3600 - sum(lneed)})
            else:
                allraz[key] = {smt: need - 3600}
                data[fuserid][key].update({smt: 3600})

for key, value in data[fuserid].items():
    for smt, need in value.items():
        fs.append(need)

    kucha[key] = sum(fs)
    fs.clear()

print('data2:', data[fuserid])
print('raz:', allraz)
print('kucha:', kucha)

'''groups = np.arange(rkey, lcdate, timedelta(hours=1)).astype(datetime)
j = 0

for k in groups:
    grp_key = time_group(groups[j])
    j += 1
    for raz_key, raz_value in allraz.items():
        for raz_state, raz_time in raz_value.items():

            h = 0
            print(grp_key)
            try:
                if (kucha[grp_key]) < 3600:
                    print('!')
                    print(data[fuserid][grp_key][smt])
                    if raz_time <= 3600 - data[fuserid][grp_key][smt]:
                        data[fuserid][grp_key].update({raz_state: data[fuserid][grp_key][smt] + raz_time})
                    else:
                        data[fuserid][grp_key].update({raz_state: 3600})
                        allraz[raz_key].update({raz_state: raz_time + data[fuserid][grp_key][raz_state] - 3600})
            except KeyError:
                break

        else:
            continue
            print('!!')
            j = 0
            for k in groups:
                grp_key = time_group(groups[j])
                if grp_key in data[fuserid]:
                    j += 1
                    continue
                if h == 1:
                    break
                data[fuserid].update({grp_key: {raz_state: raz_time}})
                h += 1

    print(grp_key)
    print(allraz)
    print(data[fuserid])'''

# Test bar chart
xticks = np.arange(fcdate, lcdate, timedelta(hours=1)).astype(datetime)
subsampled_xticks = map(lambda t: t.strftime("%m-%d"), xticks[0::24])
xvals = np.arange(len(xticks))
plt.xticks(xvals[0::24], subsampled_xticks)
plt.yticks(np.arange(0, 70, 10))

# Legend
bars = [('Busy', 'Занят'), ('Ready', 'Готов'), ('Rest', 'Отдых'),
        ('LoggedOut', 'Вышел'), ('Dinner', 'Обед'),
        ('ServiceBreak', 'Тех. перерыв'), ('NA', '-')]

legend_bars = []
prev_values = None

for (state, label) in bars:
    values = [
        data[fuserid].get(time_group(time), {}).get(state, 0) / 60
        for time in xticks
    ]
    bar = plt.bar(xvals, values, 0.8, bottom=prev_values)
    print(bar)
    legend_bars.append(bar[0])
    prev_values = values

plt.legend(legend_bars, map(lambda x: x[1], bars))

print(legend_bars)
print(values)

# Multiple bar charts
fig, (ax1, ax2) = plt.subplots(2)

ax1.bar(xticks, values, 0.35)
ax1.set_yticks(np.arange(0, 61, 10))
ax1.set_title('fuser')
ax1.set_ylabel('Минуты')

ax2.bar(xticks, values, 0.35)
ax2.set_yticks(np.arange(0, 61, 10))
ax2.set_title('fuser2')
ax2.set_ylabel('Минуты')

fig.legend(legend_bars, map(lambda x: x[1], bars))

# Graphs
plt.show()
