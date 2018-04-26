import datetime
import os

def datalogger(tag, dataArray, logIsOn):
#logIsOn is a boolean that turns the datalogger on and off, in case the user 
#wants to manually turn it off. tag is a string label that the user wants to be 
#able to find the data organized under eventually. dataArray is the calculation
#to be saved

	while logIsOn:
		if os.system("[ ! -d "/Desktop/Data" ]"): 
			os.system("mkdir /Desktop/Data/" + tag)
			os.system("cd /Desktop/Data/" + tag)

		timestr = datetime.strftime("%d_%b_%Y_%H:%M:%S", datetime.localtime())
		filename = tag + "Data" + '-' + timestr 

		
		#maybe saves all saved variables from script datalogger is run inside of
		#found this command off internet, am unsure if valid
		os.system("(set -o posix ; set ) > " + filename + ".txt") 
		os.system("echo " + "'TAG: " tag + "'" + filename + ".txt")  #unsure about the above 2 lines
		#save errors printed to terminal 
		os.system("type error.log >> " + filename + ".txt")
		os.system("echo 'TAG: ERRORS' >> " + filename + ".txt")
		#saves given dataArray, if other code works probably could remove this 
		file = open(filename,'a')
		save = "{: f}".format(dataArray)
		save += '\n' + "TAG: " + tag + '\n'
		file.write(save)
		file.close()
		
		
		#removing old files 
		os.system("ls > filelist.txt")
		filelist.txt > filelist 
		os.system("rm filelist.txt")
		for x in filelist: 
			fileDateStr = x[len(tag)+5: len(x)]
			fileDate = datetime.strptime(fileDateStr, "%Y-%m-%d %H:%M:%S.%f")
			currentime =datetime.strftime("%d_%b_%Y_%H:%M:%S", datetime.localtime())

			fileAge = currentime - fileDate
			if fileAge.minute > 40: 
				os.system("rm " + filename)
	