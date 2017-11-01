#!perl

print "Content-Type: text/html\n\n";
print "<title>House Log File</title>\n";
print "<html>\n";
print "<HEAD>\n";
print '<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">';
print "\n";
print "</HEAD>\n";
print "<body>\n";
print  "<p><b><big>House Log File</big></b></p>";

print  '<a href="main.cgi">Return to Main Menu</a></p>';


print '<pre><NOBR><small><font face="Courier New">';


# Read the Log file
###################
$error = open (INFILE, "settings/log.txt");
if (defined $error)
{
	$error="None";
	while ($line = <INFILE>)
	{
		print $line;
		print "</p>";
	}
} 
else 
{
	print "<p>Cannot open [log.txt]</p>";
	$error="Error";
}
close (INFILE);


print "</font></small></NOBR></pre>";
print  '<a href="main.cgi">Return to Main Menu</a></p>';
print "</body></html>\n";



