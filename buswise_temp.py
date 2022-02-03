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

    done =[0]*160
    