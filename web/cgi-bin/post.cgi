#!perl
$command=$ARGV[0];

$res= `curl --connect-timeout 5 -H "Content-Type:" -H "Content-Length:" -H "Accept:" -H "User-Agent:" -H "Host:" -X POST -d '$command' http://127.0.0.1:50000`;
if ($? == 0) 
{
  ##print "Command OK";
  print $res;
}
else
{
  print "ERROR from Daemon";
}


	
