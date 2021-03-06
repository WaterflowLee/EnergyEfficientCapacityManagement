import numpy as np
import matplotlib.pyplot as plt

class Monitor():

	def __init__(self, consumption_per_boot, run_power):
		self.consumption_per_boot = consumption_per_boot
		self.run_power = run_power
		self.queue_times = []
		self.process_times = []
		self.request_count = 0
		self.boot_consumption = 0
		self.run_consumption = 0

		# Forensic Monitoring
		self.idle_vals = []
		self.busy_vals = []
		self.plot_bins = []
		self.booting_vals = []
		self.queue_vals = []

	def resource_init(self):
		self.boot_consumption += self.consumption_per_boot

	def resource_shut(self, resource):
		self.run_consumption += (resource.simulator.now - resource.start_time) * self.run_power

	def observe_request(self, request):
		self.queue_times.append(request.arrival_time - request.generation_time)
		self.process_times.append(request.departure_time - request.arrival_time)
		self.request_count += 1

	def finalize(self, simulator):
		for resource in simulator.resources:
			self.resource_shut(resource)

		print("-----------------------------------------")
		print("Consumption While Booting: " + str(self.boot_consumption))
		print("Consumption While Serving: " + str(self.run_consumption))
		print("Overall Consumption: " + str(self.boot_consumption + self.run_consumption))
		print("-----------------------------------------")
		print("Average Queueing Delay: " + str(np.mean(self.queue_times)))
		print("Std. Deviation of Queueing Delay: " + str(np.std(self.queue_times)))
		print("-----------------------------------------")
		print("Average Processing Time: " + str(np.mean(self.process_times)))
		print("Std. Deviation of Processing Time: " + str(np.std(self.process_times)))
		print("-----------------------------------------")

		"""
		plt.figure(0)
		plt.hist(self.queue_times, bins=20, histtype='stepfilled', normed=True, color='b', label='Queueing Delay')
		plt.title("Queueing Delay Histogram")
		plt.xlabel("Delay Duration")
		plt.ylabel("Frequency")

		plt.figure(1)
		plt.hist(self.process_times, bins=20, histtype='stepfilled', normed=True, color='r', label='Process Time')
		plt.title("Process Time Histogram")
		plt.xlabel("Process Time")
		plt.ylabel("Frequency")
		plt.show()
		"""

		lambd = np.loadtxt('./extras/traces/stock_trend.txt')
		lambd_bins = lambd[:,0]
		lambd_vals = lambd[:,1]

		plt.figure(2)
		plt.plot(self.plot_bins, self.busy_vals, 'b')
		plt.plot(self.plot_bins, self.booting_vals, 'g')
		#plt.plot(self.plot_bins, self.busy_vals, 'b')
		plt.plot(lambd_bins[:len(self.plot_bins)], lambd_vals[:len(self.plot_bins)], 'r')
		#plt.plot(self.plot_bins, self.queue_vals, 'g')
		plt.show()

