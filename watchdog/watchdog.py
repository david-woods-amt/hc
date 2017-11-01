#!c:\python25\python.exe

from ctypes import *
import time
import socket
import select
import subprocess



###############################################################################
# Constants
###############################################################################
serverAddr="localhost"
serverPort=50000


###############################################################################











#PSAPI.DLL
psapi = windll.psapi
#Kernel32.DLL
kernel = windll.kernel32



###############################################################################
def DEBUG (msg):
###############################################################################
	x=0
	print str(msg)
	
	
	
###############################################################################
def LOG (msg):
###############################################################################
	x=0
	print str(msg)
	
	
	
	

###############################################################################
def isPythonRunning():
###############################################################################
# Need to count TWO python processes
#
###############################################################################
    
	DEBUG ("+++ isPythonRunning +++")
	
	isRunning = False
	processcount = 0
    
	arr = c_ulong * 256
	lpidProcess= arr()
	cb = sizeof(lpidProcess)
	cbNeeded = c_ulong()
	hModule = c_ulong()
	count = c_ulong()
	modname = c_buffer(30)
	PROCESS_QUERY_INFORMATION = 0x0400
	PROCESS_VM_READ = 0x0010
    
	#Call Enumprocesses to get hold of process id's
	psapi.EnumProcesses(byref(lpidProcess), cb, byref(cbNeeded))
    
	#Number of processes returned
	nReturned = cbNeeded.value/sizeof(c_ulong())
    
	pidProcess = [i for i in lpidProcess][:nReturned]
    
    
	for pid in pidProcess:
		#Get handle to the process based on PID
		hProcess = kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
		if hProcess:
			psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
			psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
			process = str("".join([ i for i in modname if i != '\x00']))
			
			if process:
				if process.find("python.exe") > -1:
					processcount = processcount + 1
            	
			#-- Clean up
			for i in range(modname._length_):
				modname[i]='\x00'
            
			kernel.CloseHandle(hProcess)

	if processcount > 1:
		LOG ("    Python IS running")
		isRunning = True
	else:
		LOG ("    Python is NOT running")
		isRunning = False
		
	
	DEBUG ("--- isPythonRunning ---")
	return isRunning



###############################################################################
def isPythonResponding():
###############################################################################
#
#
###############################################################################
    
	DEBUG ("+++ isPythonResponding +++")
    
	isResponding = False
    
	try:
		DEBUG ("    Open Socket")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		DEBUG ("    Connect")
		s.connect((serverAddr, serverPort))
		
		DEBUG ("    Send")
		s.send("WATCHDOG")
		
		DEBUG ("    Wait")
		time.sleep(2)
		
		DEBUG ("    Read")
		if s:
			is_readable = [s]
			is_writable = []
			is_error = []
			r, w, e = select.select(is_readable, is_writable, is_error, 0)
			if r:
				data=s.recv(100)
				if data == "All OK":
					isResponding = True
			DEBUG (str(data))
		
		DEBUG ("    Close")
		s.close()
		
               
		
	except Exception, e:
		LOG ("EXCEPTION: Socket Exception")
		isResponding = False
		
    
    
	if isResponding:
		LOG ("    Python IS responding")
	else:
		LOG ("    Python is NOT responding")

    
	DEBUG ("--- isPythonResponding ---")
	return isResponding

###############################################################################
def restartPython():
###############################################################################
#
#
###############################################################################
    
	DEBUG ("+++ restartPython +++")
    
	status = False
	
	command = "c:\\python25\\python.exe c:\\NewHomeControl\\Scripts\\control.py"
	
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#error = p.wait()
	#output = p.communicate()[0]
				
	#LOG (str(error))
	#LOG (str(output))
				
	
	DEBUG ("--- restartPython ---")
    
	return status








###############################################################################
#
#							M A I N   F U N C T I O N
#
###############################################################################

if __name__ == '__main__':

	
	while 1:
		if isPythonRunning() and isPythonResponding():
			LOG ("All OK")
		else:
			LOG ("All Not OK...need to restart")
			restartPython()

		time.sleep(5)
    