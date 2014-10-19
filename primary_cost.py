from ceph_query import ExecProcess,CephQuery
from system_query import SystemInfo
from system_utils import SystemUtil
import socket

if __name__ == "__main__":
	ceph=CephQuery()
	print ceph.get_cluster_status()
	#check for the folder name for collectd logs
	osd_list,osd_id=ceph.get_osd_list()
	no_of_osds=len(osd_list)
	for i in range(no_of_osds):
		print "osd list",osd_list[i]
		print "osd id",osd_id[i]
		hostname = socket.gethostbyaddr(osd_list[i])[0]
		print "Host Name : ",hostname
		info=SystemInfo(hostname)
		no_cpu=info.get_total_cpu()
		load=info.get_load()
		util=SystemUtil()
		load_factor = util.get_normal_constant(load[3]/no_cpu)
		latency = info.get_osd_latency(osd_id[i])
		#util.get_normal_constant(0.12)
		#util.get_normal_constant(0.29)
		#util.get_normal_constant(0.43)
		#util.get_normal_constant(0.65)
		#util.get_normal_constant(0.78)
		#util.get_normal_constant(0.92)

