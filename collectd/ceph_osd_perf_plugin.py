import collectd
import json
import traceback
import subprocess
import os
import base
import re
class CephOsdPerfPlugin(base.Base):

    def __init__(self):
        base.Base.__init__(self)
        self.prefix = 'ceph'

    def get_stats(self):
	"""Retrieves stats from ceph osd admin socket"""
	
	ceph_cluster = "%s-%s" % (self.prefix, self.cluster)

	data = { ceph_cluster: { } }
	admin_folder="/var/run/ceph/"
	if(os.path.isdir(admin_folder)):
		files=os.walk(admin_folder).next()[2]
        else:
		print "No folder exists "+admin_folder
		return -1
	abs_path=[admin_folder+x for x in files]
	admin_socket = max(abs_path, key=os.path.getmtime)
	cmd = "ceph --admin-daemon "+admin_socket +" perf dump -f json"
	try:
		output = subprocess.check_output(cmd, shell=True)
	except Exception as exc:
		collectd.error("ceph-osd: failed to ceph osd perf dump :: %s :: %s" % (exc, traceback.format_exc()))
		return

	if output is None:
		collectd.error('ceph-osd: failed to ceph osd perf dump :: output was None')

	json_data = json.loads(output)
	match=(re.search(r'([\w.-]+)(\d)([\w.-]+)',admin_socket))
	if match:
		osd_id=match.group(2)
	else:
		return
	data[ceph_cluster][osd_id]={}
	data[ceph_cluster][osd_id]['op_latency']={}
	data[ceph_cluster][osd_id]['op_w_latency']={}
	data[ceph_cluster][osd_id]['op_r_latency']={}
	data[ceph_cluster][osd_id]['op_latency']['sum']=json_data['osd']['op_latency']['sum']
	data[ceph_cluster][osd_id]['op_latency']['avgcount']=json_data['osd']['op_latency']['avgcount']
	data[ceph_cluster][osd_id]['op_w_latency']['sum']=json_data['osd']['op_w_latency']['sum']
	data[ceph_cluster][osd_id]['op_w_latency']['avgcount']=json_data['osd']['op_w_latency']['avgcount']
	data[ceph_cluster][osd_id]['op_r_latency']['sum']=json_data['osd']['op_r_latency']['sum']
	data[ceph_cluster][osd_id]['op_r_latency']['avgcount']=json_data['osd']['op_r_latency']['avgcount']

	#print data	
	return data

try:
	plugin = CephOsdPerfPlugin()
except Exception as exc:
	collectd.error("ceph-pg: failed to initialize ceph osd perf plugin :: %s :: %s"
            % (exc, traceback.format_exc()))

def configure_callback(conf):
	"""Received configuration information"""
	plugin.config_callback(conf)

def read_callback():
	"""Callback triggerred by collectd on read"""
	plugin.read_callback()

collectd.register_config(configure_callback)
collectd.register_read(read_callback, plugin.interval)


