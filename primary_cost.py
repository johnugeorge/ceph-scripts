from ceph_query import ExecProcess,CephQuery
from system_query import SystemInfo
from system_utils import SystemUtil
from time import sleep
import socket
import sys

if __name__ == "__main__":
	ceph=CephQuery()
	print "Cluster Health Status ",ceph.get_cluster_status()
	while 1:
	#check for the folder name for collectd logs
		osd_list,osd_id=ceph.get_osd_list()
		no_of_osds=len(osd_list)
		for i in range(no_of_osds):
			print "Osd Addr",osd_list[i]
			print "Osd Id",osd_id[i]
			hostname = socket.gethostbyaddr(osd_list[i])[0]
			print "Host Name : ",hostname
			info=SystemInfo(hostname)
			no_cpu=info.get_total_cpu()
			load=info.get_load()
			util=SystemUtil()
			load_factor = util.get_normal_constant(load[3]/no_cpu)
			print "Load Factor ",load_factor," for load ",load[3]/no_cpu
			latency = info.get_osd_latency(osd_id[i])
			print "Overall Latency ",latency[0]
			print "Read Latency ",latency[1]
			print "Write Latency ",latency[2]
			#print util.get_normal_constant(0.12)
			#print util.get_normal_constant(0.29)
			#print util.get_normal_constant(0.43)
			#print util.get_normal_constant(0.65)
			#print util.get_normal_constant(0.78)
			#print util.get_normal_constant(0.89)
			#print util.get_normal_constant(0.92)
			#print util.get_normal_constant(0.94)
			#print util.get_normal_constant(0.98)
			#print util.get_normal_constant(1)
			usage = ceph.get_osd_usage(osd_id[i])
			usage_factor = util.get_normal_constant(usage[0]/usage[1])
			print "Usage Factor ",usage_factor," for usage ",usage[0]/usage[1]
			print "###############################"
		sys.exit(0)
		sleep(10)

