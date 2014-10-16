import os

BASE_DIRECTORY="/var/lib/collectd/csv/"

class SystemInfo:
	
	def get_total_cpu(self,system_name):
		folder_name=BASE_DIRECTORY+system_name+".ubuntu/"
		print folder_name
		if(os.path.isdir(folder_name)):
			folders=os.walk(folder_name).next()[1]
			return folders
		else:
			print "No folder exists "+folder_name
		

if __name__ == "__main__":
        info=SystemInfo()
        print info.get_total_cpu("bd-1-3")
		
