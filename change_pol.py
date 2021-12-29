# code to change the starting point of schedule to to any other point

import pandas as pd

data = pd.read_csv('traveltime_dir.csv')
old_vals=[data['starttime'][x] for x in range(len(data['starttime']))]
new_vals=[(data['starttime'][x]+900)%1440 for x in range(len(data['starttime']))]

print(new_vals)

data['starttime']=data['starttime'].replace(old_vals,new_vals)

old_vals=[data['trips'][x] for x in range(len(data['starttime']))]
new_vals=[data['trips'][x][:6] + str(data['starttime'][x]) for x in range(len(data['starttime']))]

data['trips']=data['trips'].replace(old_vals,new_vals)

data=data.sort_values(by=['starttime'])
data.to_csv('tt_dir_9am.csv')