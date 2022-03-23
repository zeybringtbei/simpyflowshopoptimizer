import simpy
from collections import namedtuple

class MonitoredResource(simpy.Resource):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataPoint = namedtuple("Datapoint", "time queue_length nr_in_process")
        self.data = [self.dataPoint(time=0, queue_length=0, nr_in_process=0)]

    def request(self, *args, **kwargs):
        """ Requests the ressource and appends the time, queue length and entities in process

        Returns:
            _request_: SimPyRequest
        """
        r = super().request(*args, **kwargs)
        # store data
        self.data.append(self.dataPoint(time=self._env.now, queue_length=len(self.queue), nr_in_process=self.count))
        return r

    def release(self, *args, **kwargs):
        
        busy = 0
        q_length = 0

        if len(self.queue) > 0:
            q_length = len(self.queue) -1
            busy = self.count
        
        self.data.append(self.dataPoint(time=self._env.now, queue_length=q_length, nr_in_process=busy))

        return super().release(*args, **kwargs)
     
    def avg_util(self):
        # Determines the duration of each possible nr in process
        if len(self.data)==1:
            return 0
        
        utilization = [0]*(self.capacity+1)
        for i in range(1,len(self.data)):
            # i.e. the durationfor which x-entities were served
            utilization[self.data[i-1].nr_in_process] += (self.data[i].time - self.data[i-1].time) 
        termination = self.data[-1].time
        return [ut/termination for ut in utilization]
