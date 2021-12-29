import json
from typing_extensions import runtime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

f = open("All_results/newbuswise/buswise_9hrs_9am.json")
trips = pd.read_csv("traveltime_dir_9am.csv")
data = json.load(f)
y_pos=1
labels=[]
lab_pos=[]


for i in range(9,35):

    if i<10:
        labels.append('0'+str(i%24)+':00')
    else:
        labels.append(str(i%24)+':00')

    lab_pos.append((i-9)*60)

tot_wait=[]
for d in data:
    
    tot_wait.append((-1*int(data[d]['trips'][0][6:])))

enumerate_object = enumerate(tot_wait)
sorted_pairs = sorted(enumerate_object, key=operator.itemgetter(1))
sorted_indices = []

for index, element in sorted_pairs:
    sorted_indices.append(index)

for d in sorted_indices:
    d='busno_'+str(d+1)
    print("=============================================")
    starttimes=[]
    runtimes=[]
    buftimes=[]
    dir=[]
    waittime=data[d]['waittimes']
    for t in data[d]['trips']:
        tf=0
        if t[-1]=='N':
            t=t[:-1]
            tf=1
        starttimes.append(int(t[6:]))
        if tf==1:
            starttimes[-1]+=1440
        idx=0
        while idx<len(trips["trips"]):
            if t==trips["trips"][idx]:
                runtimes.append(trips["traveltime"][idx])
                buftimes.append(trips["waittime"][idx])
                print(trips["trips"][idx][:4])
                dir.append(trips["trips"][idx][:5])
                break
            idx+=1
    sum_wait=[]

#488f31 
#89b050
#c5d275

#fcbe6e
#f48358
#de425b

    n=len(starttimes)
    ind = np.arange(n)
    for i in range(len(starttimes)):
        if dir[i]=='AJ_UP':
           col='darkolivegreen'
        elif dir[i]=='AJ_DN':
            col='yellowgreen'
    

        elif dir[i]=='AK_UP':
            col='blue'
        elif dir[i]=='AK_DN':
            col='cyan'

        if starttimes[i]>=1440 and col=='yellowgreen':
            col='yellow'
        if starttimes[i]>=1440 and col=='cyan':
            col='purple'
    

        plt.barh(y=y_pos, left=starttimes[i],width=runtimes[i],height=1, color=col)
        plt.barh(y=y_pos, left=starttimes[i]+runtimes[i],width=buftimes[i],height=1, color='black')
    
    if data[d]["breakend"]-data[d]["breakstart"]>=0:
        plt.barh(y=y_pos, left=data[d]["breakstart"],width=data[d]["breakend"]-data[d]["breakstart"],height=1, color='gold')




    y_pos+=2
plt.xticks(lab_pos,labels)
plt.grid()
plt.show()