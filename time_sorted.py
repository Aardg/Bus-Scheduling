import pandas as pd
import json

trips = pd.read_csv("traveltime_dir_9am.csv")

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


def HasValid(pos, q ,i):

	global trips
	if len(q[pos])==0 :
		return False
	else :
		flag=0
		for b in q[pos]:
			if b.busytill<=trips["starttime"][i]:
				if b.pos!="A":
					if trips["starttime"][i] + 2*trips["total_time"][i] - b.start_time  < 540:
						flag=1
						break
					else:
						flag=0
				else:
					flag=1
					break

		if flag==1:
			return True
		else:
			return False


def check_charged(q,i):

	if len(q["C"])==0 :
		return -1
	global trips
	q["C"].sort(key = lambda x: (x.shift_break_start))


	for j in range(len(q["C"])):
		print( trips["starttime"][i]-q["C"][j].shift_break_start)
		if trips["starttime"][i]-q["C"][j].shift_break_start >= 105:
			return 0


	return -1

if __name__ == "__main__":


	queue = {
		"J" : [],
		"K" : [],
		"A" : [],
		"C" : [],
		"F" : []
	}
	undoable=[]
	for i in range(len(trips["trips"])):
		

		if not (HasValid(trips["startpos"][i],queue,i)):
			if trips["startpos"][i]=="A":
				undoable.append(i)
			else :
				if check_charged(queue,i)==-1:
					don=0
				else:
					idx = check_charged(queue,i)
					queue["C"].sort(key = lambda x: (x.shift_break_start))
					selected_bus = queue["C"].pop(0)
					print("charged ",selected_bus.shift_break_start,trips["trips"][i])
					selected_bus.busytill=trips["starttime"][i]+trips["total_time"][i]
					selected_bus.start_time=trips["starttime"][i]
					selected_bus.traveltime+=trips["total_time"][i]
					selected_bus.trip.append(trips["trips"][i])
					selected_bus.runtimes.append(trips["traveltime"][i])
					selected_bus.shift_break_end = trips["starttime"][i]
					selected_bus.pos="A"

					queue["A"].append(selected_bus)
					continue
				print("new bus ================= trip",trips["trips"][i])
				newbus = bus()
				newbus.start_time=trips["starttime"][i]
				newbus.start_time_org=trips["starttime"][i]

				newbus.started_at = trips["startpos"][i]
				newbus.busytill = trips["starttime"][i] + trips["total_time"][i]
				
				newbus.dir="UP"
				newbus.pos="A"
				newbus.trip.append(trips["trips"][i])
				newbus.runtimes.append(trips["traveltime"][i])
				newbus.traveltime+=trips["total_time"][i]
				queue["A"].append(newbus)

		else:
		
			don=0
			# b = len(queue[trips["startpos"][i]])
			pos = trips["startpos"][i]
			overworked=[]
			for b in range(len(queue[trips["startpos"][i]])):
				
				# queue[trips["startpos"][i]].sort(key = lambda x: (x.start_time))
				if trips["starttime"][i]>=queue[pos][b].busytill:
					if queue[pos][b].pos=="A":
						don=1
					else:
						if trips["starttime"][i] + 2*trips["total_time"][i] - queue[pos][b].start_time < 540:
							don=1
						else:
							overworked.append(b)
							continue
					don=1
					print("trip",trips["trips"][i])
					selected_bus = queue[pos].pop(b)

					selected_bus.waittime.append((trips["starttime"][i]-selected_bus.busytill))
					selected_bus.busytill=trips["total_time"][i] + trips["starttime"][i]

					if(trips["dir"][i]=="UP"):
						selected_bus.pos="A"
					else :
						selected_bus.pos = trips["trips"][i][1]

					selected_bus.dir = trips["dir"][i]


					selected_bus.traveltime+=trips["total_time"][i]
					selected_bus.trip.append(trips["trips"][i])
					selected_bus.runtimes.append(trips["traveltime"][i])
					queue[selected_bus.pos].append(selected_bus)
					break

			for b in sorted(overworked,reverse = True):
				selected_bus = queue[pos].pop(b)
				if selected_bus.shift_break_start==0:
					selected_bus.shift_end = selected_bus.busytill
					selected_bus.shift_break_start = selected_bus.busytill
					print("sent to charge ",selected_bus.shift_break_start)
					queue["C"].append(selected_bus)

				else:
					queue["F"].append(selected_bus)

	print(undoable)
	print("+==+=++++++=+++=++=++=++==++" )
	tru_undoable=[]
	for x in undoable:
		cpy=trips["starttime"][x]
		cpy+=1440
		don=0
		for b in range(len(queue["A"])):
			if(cpy-queue["A"][b].start_time_org + trips["total_time"][x]>=1440 or cpy>=1620):
				don=0
				continue
			else:
				don=1
				selected_bus = queue["A"].pop(b)

				selected_bus.waittime.append((cpy-selected_bus.busytill))
				selected_bus.busytill=trips["total_time"][x] + cpy

				selected_bus.pos = trips["trips"][i][1]

				selected_bus.traveltime+=trips["total_time"][x]
				selected_bus.trip.append(trips["trips"][x]+"N")
				selected_bus.runtimes.append(trips["traveltime"][x])
				queue[selected_bus.pos].append(selected_bus)
				break

		if don==0:
			tru_undoable.append(x)

	print("+==+=++++++=+++=++=++=++==++" )
	
	result = {}
	i=0
	num=0
	for k in queue.keys():

		print("===================================================== ",k)	
		for b in queue[k]:
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
	with open("All_results/TSR_new/time_sorted_9am.json", "w") as outfile: 
		json.dump(result, outfile,indent=4)	
	# print(result)
	# print(num)
	print("++++++++++++++++++++++",[trips["trips"][x] for x in tru_undoable])
