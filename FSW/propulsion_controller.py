# propulsion_controller.py
#
# Desc: Houses subsystem interface to propulsion system
#
# Author: Alex Wong (aw528)
# 
# Date: 9/21/16
#
# Status: Main functionality completed
# 		  Need to add status acquisition and health vars
#         Pins may change

#Includes
import time
import ccsds_header
import RPi.GPIO as GPIO

#Main Class
class prop_control:
    
    GPIO.setmode(GPIO.BCM)
    elecAPin = 26
    elecBPin = 19
    sparkPin = 13
    burnPin = 5
    cgPin = 6
	
	#Setup GPIO Pins
    GPIO.setup(elecAPin, GPIO.OUT) #power board
    GPIO.setup(elecBPin, GPIO.OUT) #power board
    GPIO.setup(sparkPin, GPIO.OUT) #digital pin
    GPIO.setup(cgPin, GPIO.OUT) #power board
    GPIO.setup(burnPin, GPIO.OUT) #power board

    # **may need to initialize outputs to specific values (e.g. 
    # some components like the spark plug need to be pulled 
    # low to activate so it should be initialized to high)
    
    gvPC_myApid = 2 #change later
    gvPC_maxCmdQ = 50 #max commands waiting
    
    gvPC_command = ccsds_header.CCSDSCommand()
    
	#Cold Gas Pulse
    def cgPulse(pulses,duration,spacing,delay): #opcode 0
        if(delay > 0):
            time.sleep(delay)
        # **may need to change pulses -> pulses+1 (if pulses=1, then 
        # the for loop does not iterate at all)
        for x in range(1,pulses):
            GPIO.output(cgPin, True)
            time.sleep(duration)
            GPIO.output(cgPin, False)
            time.sleep(spacing)
    
	#Cold Gas Thrust
    def cgThruster(activate,delay): #opcode 1
	    if(delay > 0):
            time.sleep(delay)
        if(activate == 1):
            print("remove")
            GPIO.output(cgPin, True)
            if(activate == -1):
                print("remove")
                GPIO.output(cgPin, False)
    
	#Electrolyzer Control
    def electrolyzerControl(electrolyzers,delay): #opcode 2
	    if(delay > 0):
            time.sleep(delay)
        if(electrolyzers[0] == 1):
            print("remove")
            GPIO.output(elecAPin, True)
        if(electrolyzers[0] == -1):
            print("remove")
            GPIO.output(elecAPin, False)
        if(electrolyzers[1] == 1):
            print("remove")
            GPIO.output(elecBPin, True)
        if(electrolyzers[1] == -1):
            print("remove")
            GPIO.output(elecBPin, False)
    
	#Spark Pin Fire
    def sparkFire(sparks,duration,spacing,delay): #opcode 3
	    if(delay > 0):
            time.sleep(delay)
        for x in range(1,sparks):
            GPIO.output(sparkPin,True)
            time.sleep(duration)
            GPIO.output(sparkPin,False)
            time.sleep(spacing)
    
	#Spark Plug Activate
    def sparkPlug(activate,delay): #opcode 4
	    if(delay > 0):
            time.sleep(delay)
        # **sparkplug needs to be pulled low to activate
        if(activate == 1):
            print("remove")
            GPIO.output(sparkPin, True)
        if(activate == -1):
            print("remove")
            GPIO.output(sparkPin, False)
    
	#Propulsion I/O Status
    def propStatus():
        print("remove")
        elecAPinStatus = GPIO.input(elecAPin)
        elecBPinStatus = GPIO.input(elecBPin)
        sparkPinStatus = GPIO.input(sparkPin)
        cgPinStatus = GPIO.input(cgPin)
        tankPressure = propTankStatus()
        chamberPressure = propChamberStatus()
        elecACurrent = elecStatus('A')
        elecBCurrent = elecStatus('B')
        propStats = [elecAPinStatus, elecBPinStatus, sparkPinStatus, cgPinStatus]#tankPressure,chamberPressure,elecACurrent,elecBCurrent]
        return propStats
    
	#Helper function for getting status in vector
    def propPinStatus():
        pinStats = [GPIO.input(elecAPin),GPIO.input(elecBPin),GPIO.input(sparkPin),GPIO.input(cgPin)]
        return pinStats

	#Burn Wire 
    def burnWire(duration,delay): #opcode 5
	    if(delay > 0):
            time.sleep(delay)
        GPIO.output(burnPin, True)
        time.sleep(duration)
        GPIO.output(burnPin, False)
        
	#Command Handler Thread
    def PC_process_cmd_thread():
        result = 1 #current status OK
        bytesCopied = 0
        
        while(gvPC_commandQ != None and gvPC_command != None):
            bytesCopied = gvPC_commandQ.get() #Should we have timeout?
            if (bytesCopied != ccsds_packet_size):
                #report error
                print("reported error")
                result = 0
            else:
                PC_execute_cmd()
        return
    
	#Command Execute 
    def PC_execute_cmd():
        result = 1 #current status ok
        
        if(gvPC_commandQ == None):
            #Report false command execution
            result = 0
        if(getattr(gvPC_command, _fields_(3)) == 0):
            printf("cgPulse")
            cgPulse(getattr(gvPC_command, _fields_(5)), getattr(gvPC_command, _fields_(6)), getattr(gvPC_command, _fields_(7)))
        elif(getattr(gvPR_command, _fields_(3)) == 1):
            printf("cgThruster")
            cgThruster(getattr(gvPC_command, _fields_(5)))
        elif(getattr(gvPR_command, _fields_(3)) == 2):
            printf("electrolyzerControl")
            electrolyzerControl(getattr(gvPC_command, _fields_(5)))
        elif(getattr(gvPR_command, _fields_(3)) == 3):
            printf("sparkFire")
            sparkFire(getattr(gvPC_command, _fields_(5)), getattr(gvPC_command, _fields_(6)), getattr(gvPC_command, _fields_(7)))
        elif(getattr(gvPR_command, _fields_(3)) == 4):
            printf("sparkPlug")
            sparkPlug(getattr(gvPC_command, _fields_(5)))
        elif(getattr(gvPR_command, _fields_(3)) == 5):
            printf("burnWire")
            burnWire(getattr(gvPC_command, _fields_(5)))
        else:
            CR_ExecuteCmd(gvPC_commandQ)
            #report true command execution
        return
    
	#External Command Receive
    def PC_receive_cmd(commandPtr):
        result = 1; #current status ok
        result = gvPS_commandQ.put(commandPtr)
        return


#Add specific status 
#def propTankStatus:

#def propChamberStatus:

#def elecStatus:
