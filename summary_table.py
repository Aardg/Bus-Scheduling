import json
import csv

f = open("Buswise/Buswise results/buswise_9hrs_4pm.json")

data = json.load(f)
pos = {
    "AJ_UP" : 44,
    "AJ_DN" : 40,
    "AK_UP" : 40,
    "AK_DN" : 42
}

file_data = {
    "BusNum" : [],
    "start_time" : [],
    "end_time" : [],
    "total_hours" : [],
    "running_hours" : [],
    "dead_km" : [],
    "distance travelled" : [],
    "vehicle_efficiency(t)" : [],
    "vehicle_efficiency(d)" : []
}
i=0

for d in data:

    i+=1
    file_data["BusNum"].append(i)
    start_time = int(data[d]["trips"][0][6:])
    cp=start_time
    if cp%60<10:
        sep = ":0"
    else:
        sep=":"
    file_data["start_time"].append(str(start_time//60)+sep+str(cp%60))
    
    end_time=int(data[d]["busytill"])
    cp=end_time
    if cp%60<10:
        sep = ":0"
    else:
        sep=":"
    file_data["end_time"].append(str(end_time//60)+sep+str(cp%60))

    
    tot=end_time-start_time
    print(tot)
    cp=tot
    if cp%60<10:
        sep = ":0"
    else:
        sep=":"
    file_data["total_hours"].append(str(tot//60)+sep+str(cp%60))

    travel_time=data[d]["traveltime"]
    print(travel_time)
    cp=travel_time
    if cp%60<10:
        sep = ":0"
    else:
        sep=":"
    file_data["running_hours"].append(str(int(travel_time//60))+sep+str(int(cp%60)))
    file_data["dead_km"].append(0)
    file_data["vehicle_efficiency(t)"].append(round((travel_time/tot)*100,2))
    file_data["vehicle_efficiency(d)"].append(100)
    dist=0
    for stop in data[d]["trips"]:
       dist+=pos[stop[:5]]
    file_data["distance travelled"].append(dist)


with open("Buswise/summary_buswise_9.5hrs.csv", "w") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(file_data.keys())
    writer.writerows(zip(*file_data.values()))

