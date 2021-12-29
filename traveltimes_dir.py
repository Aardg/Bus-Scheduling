import pandas as pd
import csv

f = open('starttimes.csv')
data=pd.read_csv(f)
tt = pd.read_csv('traveltimes.csv')
lol=[]
for d in data:
    for i in range(len(data[d])):
        lol.append((data[d][i],d+'_'+str(data[d][i])))

lol.sort(key=lambda x : x[0])

f = {
    'trips' : [],
    'traveltime' : [],
    'waittime' : [],
    'total_time' : [],
    'starttime' : [],
    'dir' : [],
    'startpos' : []
}
f['trips']=[x[1] for x in lol]

for t in f['trips']:
    idx=0
    k=0
    if(t[:2]=='AK'):
        idx=0
        k=1
    else:
        idx=4
    if(t[3:5]=='UP'):

        idx+=0

        if k==1:
            f['startpos'].append('K')
        else : 
            f['startpos'].append('J')
    else:
        idx+=2
        f['startpos'].append('A')

    tim = int(t[6:])
    f['dir'].append(t[3:5])
    f['starttime'].append(tim)
    tim=tim//60

    f['traveltime'].append(tt[list(tt.keys())[idx]][tim])
    f['waittime'].append(tt[list(tt.keys())[idx+1]][tim])
    f['total_time'].append(f['traveltime'][-1]+f['waittime'][-1])

# print(f)

df=pd.DataFrame.from_dict(f)
df.to_csv('traveltime_dir.csv')
