from ceph_query import ExecProcess,CephQuery
from system_query import SystemInfo
from system_utils import SystemUtil
from time import sleep
import socket
import sys
from collections import defaultdict

def roundUp(numToRound, multiple):
	if multiple == 0:
		return numToRound
	remainder = numToRound % multiple
	if remainder == 0:
		return numToRound
	return numToRound + multiple - remainder

def add_latency_val(val):
	global latency_raw_val
	latency_raw_val.append(val)


def add_load_val(val):
	global load_raw_val
	load_raw_val.append(val)


def get_max_latency_val():
	global latency_raw_val
	sum_val =0.0
	for val in latency_raw_val:
		sum_val =sum_val +val;
	return sum_val


if __name__ == "__main__":
	ceph=CephQuery()
	latency_val=defaultdict(lambda : None)
	global latency_raw_val
	latency_raw_val = []
	global load_raw_val
	load_raw_val = []
	info = defaultdict(lambda : None)
	print "Cluster Health Status ",ceph.get_cluster_status()
	while 1:
		latency_raw_val =[]
		osd_list,osd_id=ceph.get_osd_list()
		no_of_osds=len(osd_list)
		for i in range(no_of_osds):
			print "Osd Addr",osd_list[i]
			print "Osd Id",osd_id[i]
			hostname = socket.gethostbyaddr(osd_list[i])[0]
			print "Host Name : ",hostname
			if info[osd_id[i]] is None:
				info[osd_id[i]]=SystemInfo(hostname)
			no_cpu=info[osd_id[i]].get_total_cpu()
			load=info[osd_id[i]].get_load()
			util=SystemUtil()
			load_factor = util.get_normal_constant(load[3]/no_cpu)
			add_load_val(load_factor)
			print "Load Factor ",load_factor," for load ",load[3]/no_cpu
			latency = info[osd_id[i]].get_osd_latency(osd_id[i])
			print "Overall Latency ",latency[0]
			print "Read Latency ",latency[1]
			print "Write Latency ",latency[2]
			add_latency_val(latency[1])
				
			usage = ceph.get_osd_usage(osd_id[i])
			usage_factor = util.get_normal_constant(usage[0]/usage[1])
			print "Usage Factor ",usage_factor," for usage ",usage[0]/usage[1]
			print "###############################"
		#sys.exit(0)
		max_latency=get_max_latency_val()
		if max_latency == 0:
			print "No latency change. Skipping"
			sleep(30)
			continue	
		for i in range(no_of_osds):
			latency_factor = (1- latency_raw_val[i]/max_latency)*100
			print "Latency Factor ",latency_factor
			latency_factor =roundUp(latency_factor,10)
			print "Load Factor ",load_raw_val[i]
			if latency_factor != latency_val[osd_id[i]]:
				if latency_factor == 0:
					ceph.set_primary_affinity_cost(osd_id[i], 1)
				else:
					ceph.set_primary_affinity_cost(osd_id[i],latency_factor)
				latency_val[osd_id[i]]=latency_factor
			else:
				print "Not setting latency value as it is same", latency_factor
				exit
		sleep(30)

