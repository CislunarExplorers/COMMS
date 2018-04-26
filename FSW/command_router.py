#Command Router CSC
#Recieves Commands from Comms Controller CSC
#Global Command Queue
#Each CSC that has commands then has individual queues
#Which this places on

import Queue
import ccsds_header
import thread_controller
import hs_manager
import comm_controller
import propulsion_controller

MAX_CSC_APID_NUM = 20
gvCR_myApid = 0 #change later
gvCR_maxQ = 50 #max commands waiting
gvCR_entryCount = 0
gvCR_routingTable = []
gvCR_accept = 1
gvCR_reject = 0
gvCR_commandQ = Queue.Queue(gvCR_maxQ) #global command queue
#gvCR_command = ccsds_header.CCSDS_CreateCommand
gvCR_command = ccsds_header.CCSDSCommand() #assume you receive a command here

#Receiving commands
rcv_maxQ = 50
gvCC_receiveQ = Queue.Queue(rcv_maxQ)

#Temporary size "macros"
gvHS_maxCmdQ = 50
gvCC_maxCmdQ = 50
gvPC_maxCmdQ = 50
gvTM_maxCmdQ = 50

#Temporarily move queues to here for Flatsat
gvHS_commandQ = Queue.Queue(gvHS_maxCmdQ) #global command queue
gvCC_commandQ = Queue.Queue(gvCC_maxCmdQ) #global command queue
gvPC_commandQ = Queue.Queue(gvPC_maxCmdQ) #global command queue
gvTM_commandQ = Queue.Queue(gvTM_maxCmdQ)

def CR_ExecuteCmd(gvCR_command):
    #execute given command held in command pointer
    #default fields, noop, statusclear, 
    if getattr(gvCR_command, _fields_(3)) == 0:
        CR_ReportCmdExecution(gvCR_myApid, getattr(gvCR_command, _fields_(3)), gvCR_accept)
    elif getattr(gvCR_command, _fields_(3)) == 1:
        CR_ReportCmdExecution(gvCR_myApid, getattr(gvCR_command, _fields_(3)), gvCR_accept)
    else:
        CR_ReportCmdExecution(gvCR_myApid, getattr(gvCR_command, _fields_(3)), gvCR_reject)
    return

#Should run continuously 
def CR_ReceivePacket():
	#Get FIFO message from queue
	gvCR_command = gvCC_receiveQ.get()
	CR_RoutePacket(gvCR_command)
	return

def CR_RoutePacket(packet):
    #Check if apID registered in table
	
    #macro for STATUS?
	
    routeStatus = 1 #1 means ok
	#Implement this later
    """ #this has some more complex lookup table method of implementing this. For flatsat, lets just use if else statements for checking apid
    if getattr(packet, _fields_(4)) == gvCR_myApid:
        CR_ExecuteCmd(packet)
    else:
        #Check if APID is registered in table
        if (gvCR_routingTable(getattr(gvCR_command, _fields_(4))) != 0):
            routeStatus = gvCR_routingTable(getattr(gvCR_command, _fields_(4)))
            if (routeStatus == 1):
                return #update h&s for csc
            else:
                return #remove this later
                #report error
    return
    """
		
    #simple implementation for flatsat
    #assuming all CSCs initialized correctly
    
    if (getattr(packet, _fields_(4)) == 0):
        print("TM Command")
        TM_receive_cmd(packet)
    elif (getattr(packet, _fields_(4)) == 1):
        print("CR Command")
        #Probably don't need this case
    elif (getattr(packet, _fields_(4)) == 2):
        print("HS Command")
        HS_receive_cmd(packet)
    elif (getattr(packet, _fields_(4)) == 3):
        print("CC Command")
        CC_receive_cmd(packet)
    elif (getattr(packet, _fields_(4)) == 4):
        print("PC Command")
        PC_receive_cmd(packet)
    else:
        print("Null Command")
    return

"""
def CR_RegisterCSC(apid, func):
    result = 0
    routingTableIndex = 0
    
    if (gvCR_entryCount == 0):
        for routingTableIndex in range(0,MAX_CSC_APID_NUM):
            #empty table
            gvCR_routingTable(routingTableIndex) = 0 #but this is a list....
            
    
    #check that there is space left in routing table
    if (gvCR_entryCount < MAX_CSC_APID_NUM):
        if (gvCR_routingTable(apid) == 0):
            gvCR_routingTable(apid) = func
            gvCR_entryCount = gvCR_entryCount + 1
    
    return
"""

def CR_CmdRouterTask():
    return

def CR_ReportCmdExecution(apid, opcode, option):
    return

if __name__ == '__main__':
    from random import randrange
    delays = [randrange(1, 10) for i in range(100)]
    
    from time import sleep
    def wait_delay(d):
        print 'sleeping for (%d)sec' % d
        sleep(d)
    
    # 1) Init a Thread pool with the desired number of threads
    # pool = ThreadPool(20)
    
    for i, d in enumerate(delays):
        # print the percentage of tasks placed in the queue
        print '%.2f%c' % ((float(i)/float(len(delays)))*100.0,'%')
        
        # 2) Add the task to the queue
        #pool.add_task(wait_delay, d)
    
    receivedCommand = ccsds_header.CCSDSCommand()
    CR_RoutePacket(receivedCommand)
    
    # 3) Wait for completion
    #pool.wait_completion()


