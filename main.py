# Libs
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from console_progressbar import ProgressBar
#from progress.bar import IncrementalBar
#import pdb, time, sys

# Input
filename = str(input("Path:"))
fdate = str(input("First Date:"))
ldate = str(input("Last Date:"))

try:
    fcdate = datetime.strptime(fdate, '%Y-%m-%d').date()
    lcdate = datetime.strptime(ldate, '%Y-%m-%d').date()
except ValueError:
    print('Date Input Error, Incorrect Date')
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


def distribute_overflows(du):

    ost = {}

    for key, value in du.items():
        lneed = []
        for smt, need in value.items():
            if need < 3600:
                lneed.append(need)
            if sum(lneed) > 3600:
                lneed.sort()
                du[key].update({smt: need + 3600 - sum(lneed)})
                ost[key] = {smt: sum(lneed) - 3600}
            if need > 3600:
                if len(lneed) != 0:
                    ost[key] = {smt: need - (3600 - sum(lneed))}
                    du[key].update({smt: 3600 - sum(lneed)})
                else:
                    ost[key] = {smt: need - 3600}
                    du[key].update({smt: 3600})

    rkey = datetime.strptime(key, '%Y-%m-%d %H')
    groups = np.arange(rkey, lcdate, timedelta(hours=1)).astype(datetime)
    j = 0

    for k in groups:
        grp_key = group_time(groups[j])
        j += 1
        if grp_key not in du:
            du.update({grp_key: {}})
        for ost_key, ost_value in ost.items():
            if sum(list(du[grp_key].values())) == 3600:
                break
            for ost_state, ost_time in ost_value.items():
                if sum(list(du[grp_key].values())) > 3600:
                    ost[ost_key].update({ost_state: ost_time + sum(list(du[grp_key].values())) - 3600})
                    du[grp_key].update({ost_state: 3600 - (sum(list(du[grp_key].values())) - 3600)})
                    break
                #if sum(list(du[grp_key].values())) > 3600:
                    #pdb.set_trace()
                if ost_state in du[grp_key]:
                    if ost_time <= 3600 - sum(list(du[grp_key].values())):
                        du[grp_key].update({ost_state: ost_time + du[grp_key][ost_state]})
                        ost[ost_key].update({ost_state: 0})
                    else:
                        i = j
                        try:
                            for kk in groups:
                                if ost_time > 3600:
                                    ost_time -= 3600 - sum(list(du[grp_key].values()))
                                    du[grp_key].update({ost_state: du[grp_key][ost_state] + 3600 - sum(list(du[grp_key].values()))})
                                    ost[ost_key].update({ost_state: ost_time})
                                    grp_key = group_time(groups[j])
                                    i += 1
                                else:
                                    du[grp_key].update({ost_state: ost_time})
                                    ost[ost_key].update({ost_state: 0})
                        except KeyError:
                            try:
                                for kkk in groups:
                                    if ost_time > 3600:
                                        if grp_key not in du:
                                            du.update({grp_key: {}})
                                        ost_time -= 3600 - sum(list(du[grp_key].values()))
                                        du[grp_key].update({ost_state: 3600 - sum(list(du[grp_key].values()))})
                                        ost[ost_key].update({ost_state: ost_time})
                                        grp_key = group_time(groups[i])
                                        i += 1
                                    else:
                                        grp_key = group_time(groups[i])
                                        if grp_key not in du:
                                            du.update({grp_key: {}})
                                        du[grp_key].update({ost_state: ost_time})
                                        ost[ost_key].update({ost_state: 0})
                            except IndexError:
                                pass
                else:
                    if ost_time <= 3600 - sum(list(du[grp_key].values())):
                        du[grp_key].update({ost_state: ost_time})
                        ost[ost_key].update({ost_state: 0})
                    else:
                        i = j
                        try:
                            for kkkk in groups:
                                if ost_time > 3600:
                                    if grp_key not in du:
                                        du.update({grp_key: {}})
                                    ost_time -= 3600 - sum(list(du[grp_key].values()))
                                    du[grp_key].update({ost_state: 3600 - sum(list(du[grp_key].values()))})
                                    ost[ost_key].update({ost_state: ost_time})
                                    grp_key = group_time(groups[i])
                                    i += 1
                                else:
                                    grp_key = group_time(groups[i])
                                    if grp_key not in du:
                                        du.update({grp_key: {}})
                                    du[grp_key].update({ost_state: ost_time})
                                    ost[ost_key].update({ost_state: 0})
                        except IndexError:
                            pass

    return du


# Parsing
'''print('Preparing...')
try:
    with open(filename, 'r') as file:
        pbp = sum(1 for line in file)
except FileNotFoundError:
    print('Path Input Error, File Not Found')
    quit()
print('Success!')
pb = ProgressBar(total=pbp, prefix='Progress:', suffix='', decimals=1, length=50, fill='█', zfill='-')

pbt = 0'''
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
        #pbt += 1
        #pb.print_progress_bar(pbt)
print('Done!')

# Overflow
try:
    distribute_overflows(data[fuserid])
    #distribute_overflows(data[suserid])
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

ax1.bar(xticks, values, 0.35)
ax1.set_yticks(np.arange(0, 61, 10))
ax1.set_title('fuser')
ax1.set_ylabel('Минуты')

ax2.bar(xticks, values, 0.35)
ax2.set_yticks(np.arange(0, 61, 10))
ax2.set_title('fuser2')
ax2.set_ylabel('Минуты')

fig.legend(legend_bars, map(lambda x: x[1], bars))'''

# Output
plt.show()
