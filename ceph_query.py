import subprocess
import os
import json
import signal
from time import sleep
PIPE = subprocess.PIPE

class ExecProcess():

	def execute(self,cmd):
		proc = subprocess.Popen(cmd,shell = True,preexec_fn=os.setsid,
			stdout=PIPE, stderr=PIPE)
		return proc

	def fetch_results(self,cmd):
		results = subprocess.check_output(cmd.split())
		return results
	
	def kill_process(self,proc):
		proc.terminate()


class CephQuery():
	def __init__(self):
		self.command=ExecProcess()

	def get_cluster_status(self):
		cmd="ceph health -f json"
		results = self.command.fetch_results(cmd)
		json_output = json.loads(results)
		return json_output["overall_status"] 

	def get_osd_info(self):
		cmd="ceph osd dump -f json"
		results = self.command.fetch_results(cmd)
                json_output = json.loads(results)
                return json_output["osds"]

	def get_osd_list(self):
		osd_data=self.get_osd_info()
		#print osd_data
		osd_id=[]
		osd_list=[]
		for val in osd_data:
			osd_list.append(val["public_addr"].split(":")[0])
			osd_id.append(val["osd"])
		print "id",osd_id
		return (osd_list,osd_id)

       
if __name__ == "__main__":
	ceph=CephQuery()
	print ceph.get_cluster_status()
	proc=ceph.command.execute("stress -c 5")
	print "waiting"
	sleep(5)
	print "killing ",proc.pid
	os.killpg(proc.pid, signal.SIGTERM)	



