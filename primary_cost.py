from ceph_query import ExecProcess,CephQuery
from system_query import SystemInfo
from system_utils import SystemUtil
import socket

if __name__ == "__main__":
	ceph=CephQuery()
	print ceph.get_cluster_status()
	#check for the folder name for collectd logs
	for osd in ceph.get_osd_list():
		hostname = socket.gethostbyaddr(osd)[0]
		print "Host Name : ",hostname
		info=SystemInfo(hostname)
		no_cpu=info.get_total_cpu()
		load=info.get_load()
		util=SystemUtil()
		load_factor = util.get_normal_constant(load[3]/no_cpu)
		#util.get_normal_constant(0.12)
		#util.get_normal_constant(0.29)
		#util.get_normal_constant(0.43)
		#util.get_normal_constant(0.65)
		#util.get_normal_constant(0.78)
		#util.get_normal_constant(0.92)

