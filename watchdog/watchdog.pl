#!c:\perl\bin\perl.exe

use strict;
use warnings;

use Win32::Process;
use IO::Socket;

###############################################################################
# Constants
###############################################################################
my $serverport=50000;
my $serveraddr="127.0.0.1";


###############################################################################
sub ErrorReport
###############################################################################
{
	LOG (Win32::FormatMessage( Win32::GetLastError() ));
}
	

###############################################################################
sub getTimeStamp
###############################################################################
{
	my ($second, $minute, $hour, $dayOfMonth, $month, $yearOffset, $dayOfWeek, $dayOfYear, $daylightSavings) = gmtime();
	my $year = 1900 + $yearOffset;
	$month+=1;
	my $theGMTime = "$year-$month-$dayOfMonth $hour:$minute:$second";
	
	return $theGMTime;
}



	
###############################################################################
sub DEBUG
###############################################################################
{
	my $msg=$_[0];
	print "[".getTimeStamp()."] - $msg\n";
}


###############################################################################
sub LOG
###############################################################################
{
	my $msg=$_[0];
	
	my $log = "[".getTimeStamp()."] - $msg\n";
	
	print $log;
	
	open (MYFILE, '>>log_watchdog.txt');
	print MYFILE $log;
 	close (MYFILE); 
}



	

###############################################################################
sub isPythonRunning
###############################################################################
{
	
	DEBUG ("+++ isPythonRunning +++");
	
	my $isRunning=0;
	my $cmd="";
	my $count=0;
	
	$cmd="tasklist /fi \"imagename eq python.exe\" | wc -l ";
	
	$count = `$cmd`;
	DEBUG ($count);
	
	if ($count==0) {
		$isRunning=0;
	} else {
		$isRunning=1;
	}
	
	DEBUG ("--- isPythonRunning ---");
	return $isRunning;
	
}



###############################################################################
sub isPythonResponding
###############################################################################
{
	
	DEBUG ("+++ isPythonResponding +++");
	
	my $isResponding=0;
	
	my $cmd="";
	my $count=0;
	my $socket;
	my $recv_data;
	
	
	$socket = new IO::Socket::INET (
	    PeerAddr  => $serveraddr,
	    PeerPort  =>  $serverport,
	    Proto => 'tcp',
	    Timeout  => 5
	);
	
	
	if ($socket)
	{
		$socket->send("WATCHDOG");
		
		sleep(3);
		
		my $sel = new IO::Select($socket);

		my @ready;
		my $sock;
		my $request = "e8aa9e somequery 123";
		my $maxread = 1024;
		my $response;
		
		@ready = $sel->can_read(5);
    	if (! scalar(@ready)) 
    	{
    		LOG("    Response Timed out");
    	} 
    	else 
    	{
    		$sock = $ready[0];    
    		if (! sysread($ready[0], $response, $maxread)) 
    		{
        		LOG ("    Failed to receive data:$!");    
    		} 
    		else 
    		{
    		    DEBUG ("    Got response $response");    
    		    if ($response eq "All OK")
    		    {
    		    	DEBUG ("    Response Match OK");
    		    	$isResponding=1;
    		    }
    		}
    	}
	}
	else
	{
		LOG ("    ERROR: Couldn't connect to Server");
	}
	
	
	if ($socket)
	{
		$socket->close();
	}
	
	DEBUG ("--- isPythonResponding ---");
	return $isResponding;
	
}




###############################################################################
sub restartPython
###############################################################################
{
	
	DEBUG ("+++ restartPython +++");
	
	my $cmd="";
	my $error="";
	my $ProcessObj;
	
	
	$cmd="taskkill /f /im python.exe";
	$error = `$cmd`;
	
	$cmd="c:\\NewHomeControl\\Scripts\\go.cmd";
	
	#$error = fork($cmd);
	
	Win32::Process::Create($ProcessObj,
			"c:\\python25\\python.exe",
			"python.exe c:\\NewHomeControl\\Scripts\\control.py",
			0,
			NORMAL_PRIORITY_CLASS | CREATE_NEW_CONSOLE,
		".")|| die ErrorReport();
		
		
	
	DEBUG ("--- restartPython ---");
	
	
}


###############################################################################
#
#							M A I N   F U N C T I O N
#
###############################################################################


LOG ("================================================");
LOG ("= Watchdog                                     =");
LOG ("================================================");



while (1)
{
	if ( isPythonRunning() )
	{
		if ( ! isPythonResponding() )
		{
			LOG ("Python NOT Responding...restart");
			restartPython()
		}
	}
	else
	{
		LOG ("Python NOT Running...restart");
		restartPython()
	}

	sleep(100);
}

