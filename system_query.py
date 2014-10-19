import os

BASE_DIRECTORY="/var/lib/collectd/csv/"
CPU_HISTORY=10

class SystemInfo:
	def __init__(self,system_name):
		self.base_folder=BASE_DIRECTORY+system_name

	def read(self,file_name):
		f = open(file_name, 'rU')
		for line in f:
			fields=line.split(",")
			try:
				float(fields[0])
			except ValueError:
				continue
		return fields
	
	def get_total_cpu(self):
		if(os.path.isdir(self.base_folder)):
			folders=os.walk(self.base_folder).next()[1]
		else:
			print "No folder exists "+self.base_folder
			return -1
		cpus=[x for x in folders if x.find('cpu') != -1]
		print "Total no of cpus ",len(cpus)
		return len(cpus)

	def get_load(self):
		folder_name=self.base_folder+"/load/"
		if(os.path.isdir(folder_name)):
                        files=os.walk(folder_name).next()[2]
                else:
                        print "No folder exists "+folder_name
                        return []
		abs_path=[folder_name+x for x in files] 
		latest_file = max(abs_path, key=os.path.getmtime)
		values=self.read(latest_file)
		print "Epoch ",values[0]
		print "Avg in last 1 min ",values[1]
		print "Avg in last 5 min ",values[2]
		print "Avg in last 10 min ",values[3]
		result_set=[]
		for val in values:
			result_set.append(float(val))
		return result_set
       

	def get_latest_file(self,folder_name,filter_name):
		if(os.path.isdir(folder_name)):
                        files=os.walk(folder_name).next()[2]
                else:
                        print "No folder exists "+folder_name
                        return []
		filtered_files= [x for x in files if x.find(filter_name) != -1]
		abs_path=[folder_name+x for x in filtered_files]
		latest_file = max(abs_path, key=os.path.getmtime)
		return latest_file
		 
	def get_osd_latency(self,osd_id):
		folder_name=self.base_folder+"/ceph-ceph-"+str(osd_id)+"/"		
		latest_file_avgcount= self.get_latest_file(folder_name,'op_latency-avgcount')
		latest_file_sum= self.get_latest_file(folder_name,'op_latency-sum')
		latest_file_r_avgcount= self.get_latest_file(folder_name,'op_r_latency-avgcount')
		latest_file_r_sum= self.get_latest_file(folder_name,'op_r_latency-sum')
		latest_file_w_avgcount= self.get_latest_file(folder_name,'op_w_latency-avgcount')
		latest_file_w_sum= self.get_latest_file(folder_name,'op_w_latency-sum')
		result_set=[]
		value_avgcount=float((self.read(latest_file_avgcount))[1])
		value_sum=float((self.read(latest_file_sum))[1])
		print "Overall count value",value_avgcount
		print "Overall sum value",value_sum
		latency = value_sum/value_avgcount
		result_set.append(latency)
		print "latency ",latency
		value_avgcount=float((self.read(latest_file_r_avgcount))[1])
		value_sum=float((self.read(latest_file_r_sum))[1])
		print "Read count value",value_avgcount
		print "Read sum value",value_sum
		latency = value_sum/value_avgcount
		result_set.append(latency)
		print "Read latency ",latency
		value_avgcount=float((self.read(latest_file_w_avgcount))[1])
		value_sum=float((self.read(latest_file_w_sum))[1])
		print "Write count value",value_avgcount
		print "Write sum value",value_sum
		latency = value_sum/value_avgcount
		result_set.append(latency)
		print "Write latency ",latency
                return result_set

if __name__ == "__main__":
	info=SystemInfo("bd-1-3.ubuntu")
	print info.get_total_cpu()
	print info.get_load()
		
