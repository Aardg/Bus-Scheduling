import pandas as pd
import json

trips = pd.read_csv("traveltime_dir.csv")

class bus:

	start_time=-1
	shift_end=0
	started_at="N"
	busytill=0
	pos="N"
	traveltime=0
	dir="N"
	start_time_org=0
	waittime=[]
	shift_break_start=0
	shift_break_end=0

	trip=[]
	runtimes=[]

	def __init__(self):
		self.start_time=-1
		self.shift_end=0
		self.busytill=-1
		self.pos="N"
		self.dir="N"
		self.start_time_org=0
		self.started_at="N"
		self.traveltime=0
		self.shift_break=0
		self.waittime=[]
		self.trip=[]
		self.runtimes=[]
		self.shift_break_start=0
		self.shift_break_end=0

if __name__ == "__main__":

	allbus=[]
	total=0
	done=[0]*160
	
	while total<len(trips['trips']):

		newbus=bus()
		for i in range(len(trips['trips'])):
			
			if done[i]==1:
				continue

			if newbus.pos!='N' and newbus.pos!=trips['startpos'][i]:
				continue
			if newbus.shift_break_start!=0 and trips['starttime'][i] - newbus.shift_break_start<120:
				continue
			if newbus.pos!='A' and newbus.traveltime + 2*trips['total_time'][i] >=600:
				print("too much",newbus.traveltime + 2*trips['total_time'][i],newbus.busytill)
				newbus.shift_break_start = newbus.busytill
				newbus.traveltime = 0
				continue
			if newbus.shift_break_start!=0 and trips['starttime'][i] - newbus.shift_break_start>=120:

				newbus.shift_break_end = trips['starttime'][i]
				newbus.start_time=trips["starttime"][i]
				newbus.started_at = trips["startpos"][i]
				newbus.busytill = trips["starttime"][i] + trips["total_time"][i]
				print("charge")
				newbus.dir="UP"
				newbus.pos="A"
				newbus.trip.append(trips["trips"][i])
				newbus.runtimes.append(trips["traveltime"][i])
				newbus.traveltime+=trips["total_time"][i]
				done[i]=1
				total+=1
				continue

			if newbus.pos=='N' and trips['startpos'][i]!='A':
				
				newbus.start_time=trips["starttime"][i]
				newbus.start_time_org=trips["starttime"][i]

				newbus.started_at = trips["startpos"][i]
				newbus.busytill = trips["starttime"][i] + trips["total_time"][i]
				
				newbus.dir="UP"
				newbus.pos="A"
				newbus.trip.append(trips["trips"][i])
				newbus.runtimes.append(trips["traveltime"][i])
				newbus.traveltime+=trips["total_time"][i]
				done[i]=1
				total+=1
				continue

			else:
				if newbus.pos == trips['startpos'][i] and newbus.busytill <= trips['starttime'][i]:
					
					newbus.busytill = trips["starttime"][i] + trips["total_time"][i]

					newbus.dir=trips['dir'][i]
					if trips['dir'][i]=="UP":
						newbus.pos="A"
					else:
						newbus.pos=trips['trips'][i][1]
					newbus.trip.append(trips["trips"][i])
					newbus.runtimes.append(trips["traveltime"][i])
					newbus.traveltime+=trips["total_time"][i]

					done[i]=1
					total+=1
					
		if len(newbus.trip)==0:
			break
		allbus.append(newbus)
	print(done)
	for b in allbus:
		print(b.trip)

	print(len(allbus))

	result = {}
	i=0
	num=0
	

		
	for b in allbus:
		i+=1
		print(b.trip,"number",i)
		num+=len(b.trip)
		key = "busno_"+str(i) 
		result[key] = {
			"starting position" : b.started_at,
			"final pos" : b.pos,
			"trips" : b.trip,
			"busytill" : int(b.busytill),
			"traveltime" : int(b.traveltime),
			"waittimes" : [int(x) for x in b.waittime],
			"runtimes"  : [int(x) for x in b.runtimes],
			"breakstart" : int(b.shift_break_start),
			"breakend" : int(b.shift_break_end)
		}
	print(num)
	with open("buswise.json", "w") as outfile: 
		json.dump(result, outfile,indent=4)