from Queue import Queue
from threading import Thread
import threading
#import ss_controller
#import comm_controller
import propulsion_controller
import command_router
import hs_manager
import thread
import time
import ccsds_header


gvTC_newThreadQ = Queue(20)
gvTC_receivedCommand = ccsds_header.CCSDSCommand() 

class tm_manager:
    def thread_manager(self):
		while(1):
			if(gvTC_newThreadQ != None):
				gvTC_receivedCommand = gvTC_newThreadQ.get()
				
				#parse apid, args, delay, etc.
				apid = getattr(gvTC_receivedCommand, _fields_(3))
				opcode = getattr(gvTC_receivedCommand, _fields_(2))
				delay = getattr(gvTC_receivedCommand, _fields_(10))
				arg0 = getattr(gvTC_receivedCommand, _fields_(4))
				arg1 = getattr(gvTC_receivedCommand, _fields_(5))
				arg2 = getattr(gvTC_receivedCommand, _fields_(6))
				arg3 = getattr(gvTC_receivedCommand, _fields_(7))
				arg4 = getattr(gvTC_receivedCommand, _fields_(8))
				arg5 = getattr(gvTC_receivedCommand, _fields_(9))
				if (apid == 2): #Propulsion
					if (opcode == 0): #cgPulse(pulses,duration,spacing,delay)
						try:
							#find args
							thread.start_new_thread(cgPulse,(arg0,arg1,arg2,delay))
						except: 
							print "Error: unable to start thread"
					elif (opcode == 1): #cgThruster(activate,delay): #opcode 1
						try:
							#find args
							thread.start_new_thread(cgThrustere,(arg0,delay))
						except: 
							print "Error: unable to start thread"		
					elif (opcode == 2): #electrolyzerControl(electrolyzers,delay): #opcode 2
						try:
							#find args
							thread.start_new_thread(electrolyzerControl,(arg0,delay))
						except: 
							print "Error: unable to start thread"	
					elif (opcode == 3): #sparkFire(sparks,duration,spacing,delay): #opcode 3
						try:
							#find args
							thread.start_new_thread(sparkFire,(arg0,arg1,arg2,delay))
						except: 
							print "Error: unable to start thread"	
					elif (opcode == 4): #sparkPlug(activate,delay): #opcode 4 burnWire(duration,delay): #opcode 5
						try:
							#find args
							thread.start_new_thread(sparkPlug,(arg0,delay))
						except: 
							print "Error: unable to start thread"	
					elif (opcode == 5): #burnWire(duration,delay): #opcode 5
						try:
							#find args
							thread.start_new_thread(burnWire,(arg0,delay))
						except: 
							print "Error: unable to start thread"								
				if (apid == 1):
					if (opcode == 0): #encode(self,instring): opcode 0
						try:
							#find args
							thread.start_new_thread(encode, (self,instring,delay))
						except:
							print "Error: unable to start thread"
					# elif (opcode == 1) #encode(self,instring): #opcode 0
						# try:
							# #find args
							# thread.start_new_thread(encode, (self,instring,delay))
						# except:
							# print "Error: unable to start thread"
		return

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

if __name__ == '__main__':
    from random import randrange
    delays = [randrange(1, 10) for i in range(100)]
    
    from time import sleep
    def wait_delay(d):
        print 'sleeping for (%d)sec' 
        sleep(d)
    
    # 1) Init a Thread pool with the desired number of threads
    pool = ThreadPool(20)
    
    """
    for i, d in enumerate(delays):
        # print the percentage of tasks placed in the queue
        print '%.2f%c' % ((float(i)/float(len(delays)))*100.0,'%')
        
        # 2) Add the task to the queue
        pool.add_task(wait_delay, d)
    """
    
    #pool.add_task(TM_process_cmd_thread, d)
    
    # 3) Wait for completion
    pool.wait_completion()
    