import json
from typing_extensions import runtime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator

f = open("All_results/newbuswise/buswise_9hrs.json")
trips = pd.read_csv("traveltime_dir.csv")
data = json.load(f)
y_pos=1
labels=[]

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
    for t in data[d]['trips']:
        print(t)

