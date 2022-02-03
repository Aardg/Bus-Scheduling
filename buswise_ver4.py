import pandas as pd
import json

trips = pd.read_csv("traveltime_dir_4pm.csv")
trips=trips.sort_values(by=['starttime'])
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
	onbreak = 0
	traveltime_org=0
	trip=[]
	runtimes=[]
	shift_dur=0

	def __init__(self):
		self.start_time=-1
		self.shift_end=0
		self.busytill=-1
		self.pos="N"
		self.dir="N"
		self.start_time_org=0
		self.started_at="N"
		self.traveltime=0
		self.traveltime_org=0
		self.shift_break=0
		self.waittime=[]
		self.trip=[]
		self.runtimes=[]
		self.shift_break_start=0
		self.shift_break_end=0
		self.onbreak=0
		self.shift_dur=0

if __name__ == "__main__":

	allbus=[]
	total=0
	done=[0]*160
	brk_flg=1
	while(total<160):

		print("=============newbus================")
		newbus=bus()
		selected_up=-1
		selected_dn=-1
		brk=-1
		busdone=-1
		i=0
		for i in range(len(trips['trips']))	:
			print(i)
			if done[i]!=0 or trips['startpos'][i]=='A':
				continue

			if newbus.onbreak!=1 and (newbus.pos!='N') and newbus.pos!=trips['startpos'][i]:
				continue

			if newbus.onbreak==1:
				if (((trips['starttime'][i]-newbus.shift_break_start) >= 120 and (trips['starttime'][i]-newbus.shift_break_start) <= 180) or trips['starttime'][i]-newbus.shift_break_start >= 300):
					newbus.onbreak=0
					newbus.shift_dur=0
					brk=1
					newbus.pos="N"
					newbus.busytill=trips['starttime'][i]-1
					print("ended break")
					i=0
					continue
				else:
					continue
				

			if newbus.pos=='N':
				print("selected upn: ",trips['trips'][i],done[i])
				selected_up=i
			
			elif newbus.pos == trips['startpos'][i] and newbus.busytill <= trips['starttime'][i]:
				print("selected up: ",trips['trips'][i],done[i])
				selected_up=i

			if selected_up!=-1:
				
				selected_dn=-1

				for j in range(len(trips['startpos'])):

					if done[j]!=0 or trips['startpos'][j]!='A':
						continue
					

					if trips['starttime'][selected_up] + trips['total_time'][selected_up] <= trips['starttime'][j]:
						if newbus.shift_dur + ((trips['starttime'][j] + trips['total_time'][j]) - trips['starttime'][selected_up]) <= 540:
							print("selected dn : ",trips['trips'][j],done[j])
							print(newbus.shift_dur + ((trips['starttime'][j] + trips['total_time'][j]) - trips['starttime'][selected_up]))
							selected_dn=j
							break
						else:
							print("shift exceeded")
							if newbus.shift_break_end!=0:
								busdone=1
								break

							if newbus.shift_break_start==0:
								newbus.onbreak=1
								newbus.shift_break_start = newbus.busytill
							i=0
							break
			else :
				print("no up trip")
				continue	

			if busdone==1:
				break	

			if selected_dn==-1:
				print("no dn trip available")
			else:
				if brk==1:
					newbus.shift_break_end = trips["starttime"][selected_up]
					newbus.busytill = newbus.shift_break_end
					brk=-1
				print(trips["trips"][selected_up],trips["trips"][selected_dn],trips['trips'][selected_dn][1],newbus.shift_dur + ((trips['starttime'][selected_dn] + trips['total_time'][selected_dn]) - newbus.busytill))
				newbus.trip.append(trips["trips"][selected_up])
				newbus.trip.append(trips["trips"][selected_dn])
				newbus.shift_dur = newbus.shift_dur + ((trips['starttime'][selected_dn] + trips['total_time'][selected_dn]) - newbus.busytill)
				newbus.busytill = trips['starttime'][selected_dn] + trips['total_time'][selected_dn]
				newbus.runtimes.append(trips["traveltime"][selected_up])
				newbus.runtimes.append(trips["traveltime"][selected_dn])
				newbus.traveltime+=trips["total_time"][selected_dn] + trips["total_time"][selected_up]
				newbus.traveltime_org+=trips["total_time"][selected_dn] + trips["total_time"][selected_up]
				newbus.pos = trips['trips'][selected_dn][1]
				print("===============",selected_up,selected_dn)
				done[selected_dn]=1
				done[selected_up]=1
				print("++++++++++++++++++ bus is busy till",newbus.busytill)
				total+=2
				selected_dn=-1
				selected_up=-1

		if len(newbus.trip)==0:
			break


		allbus.append(newbus)


	tot=0
	for b in allbus:
		tot+=len(b.trip)
		print(b.trip)
	
	print(tot)

	result = {}
	i=0
	num=0
	

	total_trips=0
	for b in allbus:
		i+=1
		total_trips+=len(b.trip)
		print(b.trip,"number",i)

		num+=len(b.trip)
		key = "busno_"+str(i) 
		print(b.traveltime_org)
		result[key] = {
			"starting position" : b.started_at,
			"final pos" : b.pos,
			"trips" : b.trip,
			"busytill" : int(b.busytill),
			"traveltime" : int(b.traveltime_org),
			"waittimes" : [int(x) for x in b.waittime],
			"runtimes"  : [int(x) for x in b.runtimes],
			"breakstart" : int(b.shift_break_start),
			"breakend" : int(b.shift_break_end)
		}
	print(num)
	print([trips['trips'][i] for i in range(len(done)) if done[i]==0])
	with open("All_results/Buswise_v4/buswise_9hrs_4pm.json", "w") as outfile: 
		json.dump(result, outfile,indent=4)
	
	print("toal number of trips ",total_trips)
