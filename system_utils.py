from scipy import stats

TOTAL_TICKS=10
MU = 0
SIGMA = 0.5


class SystemUtil:
	def __init__(self):
		self.norm_dist=NormalDist()
	
	def get_normal_constant(self,arg):
		interval_width= 1.0 / TOTAL_TICKS
		interval_upper_limit=1.0
		current_interval=0
		while(arg < interval_upper_limit):
			current_interval=current_interval + interval_width
			interval_upper_limit= interval_upper_limit-interval_width
		val = ((self.norm_dist.get_norm_value(current_interval) - 0.5)/0.5)
		print arg,current_interval, val
		return val 		


class NormalDist:
	def __init__(self):
		self.norm_cdf= stats.norm(MU,SIGMA)

	def get_norm_value(self,arg):
		return self.norm_cdf.cdf(arg)
