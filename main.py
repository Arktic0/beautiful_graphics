# Libs
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from console_progressbar import ProgressBar

# Input
filename = str(input("Path:"))
fdate = str(input("First Date:"))
ldate = str(input("Last Date:"))

try:
    fcdate = datetime.strptime(fdate, '%Y-%m-%d').date()
    lcdate = datetime.strptime(ldate, '%Y-%m-%d').date()
except ValueError:
    print('Date Input Error, Invalid Date Format')
    quit()

fuserid = str(input('1 ID:'))
suserid = str(input('2 ID:'))
users = [fuserid, suserid]


# Defs
def parse_time(s):

    s = s.strip(' \n[)"') + "00"

    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f%z')
    except ValueError:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S%z')


def group_time(dt):

    return dt.strftime('%Y-%m-%d %H')


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def distribute_overflows(du):

    ost = {}
    j = 0
    groups = np.arange(fcdate, lcdate, timedelta(hours=1)).astype(datetime)

    for k in groups:
        grp_key = group_time(groups[j])
        j += 1
        for key, value in du.items():
            if grp_key == key:
                for du_state, du_time in value.items():
                    if du_time > 3600:
                        if du_state in ost:
                            ost.update({du_state: ost[du_state] + du_time - 3600})
                        else:
                            ost.update({du_state: du_time - 3600})
                        du[grp_key].update({du_state: 3600})
                    if sum(list(du[grp_key].values())) < 3600:
                        if sum(list(ost.values())) != 0:
                            try:
                                ost.update({du_state: ost[du_state] - 3600 + sum(list(du[grp_key].values()))})
                                du[grp_key].update({du_state: du_time + 3600 - sum(list(du[grp_key].values()))})
                            except KeyError:
                                for ost_state, ost_time in ost.items():
                                    if ost_time != 0:
                                        break
                                ost.update({ost_state: ost_time - 3600 + sum(list(du[grp_key].values()))})
                                du[grp_key].update({du_state: 3600 - sum(list(du[grp_key].values()))})
                    if sum(list(du[grp_key].values())) > 3600:
                        key_max_value = get_key(du[grp_key], max(du[grp_key].values()))
                        if du_state in ost:
                            ost.update({key_max_value: ost[du_state] + sum(list(du[grp_key].values())) - 3600})
                        else:
                            ost.update({key_max_value: sum(list(du[grp_key].values())) - 3600})
                        du[grp_key].update({key_max_value: max(du[grp_key].values()) + 3600 - sum(list(du[grp_key].values()))})

    return du


# Parsing
print('Preparing...')
try:
    with open(filename, 'r') as file:
        pbp = sum(1 for line in file)
except FileNotFoundError:
    print('Path Input Error, File Not Found')
    quit()
print('Success!')
pb = ProgressBar(total=pbp, prefix='Progress:', suffix='', decimals=1, length=50, fill='█', zfill='-')

pbt = 0
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
            z = z.setdefault(group_time(ctime), {})
            z.setdefault(state, 0)
            if state_range:
                z[state] += state_range.seconds
        pbt += 1
        pb.print_progress_bar(pbt)
print('Done!')

# Overflow
try:
    distribute_overflows(data[fuserid])
    distribute_overflows(data[suserid])
except KeyError:
    print('Input Error, ID Or Date Incorrect')
    quit()

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
prev_values = 0

for (state, label) in bars:
    values = [
        data[fuserid].get(group_time(time), {}).get(state, 0) / 60
        for time in xticks
    ]
    bar = plt.bar(xvals, values, 0.8, bottom=prev_values)
    legend_bars.append(bar[0])
    prev_values += np.array(values)

plt.legend(legend_bars, map(lambda x: x[1], bars))

# Multiple bar charts
'''fig, (ax1, ax2) = plt.subplots(2)

ax1.bar(xticks, legend_bars, 0.35)
ax1.set_yticks(np.arange(0, 61, 10))
ax1.set_title('fuser')
ax1.set_ylabel('Минуты')

ax2.bar(xticks, legend_bars, 0.35)
ax2.set_yticks(np.arange(0, 61, 10))
ax2.set_title('fuser2')
ax2.set_ylabel('Минуты')

fig.legend(legend_bars, map(lambda x: x[1], bars))'''

# Output
plt.show()
