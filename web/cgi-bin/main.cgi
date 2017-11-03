#!/usr/bin/perl


use POSIX;
#########################################################################
# Main Web Page script
#
# Handles all operations and posts commands to daemon
#
#########################################################################
$|=1;


# The Info passed to the script file
$line = $ENV{'QUERY_STRING'};


# Print HTML Header
# -----------------
print "Content-Type: text/html\n\n";
print"
	<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">
	<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en-US\"  c\ lang=\"en-US\">


	<HEAD>
		<title>Main Menu</title>
		<META HTTP-EQUIV=\"Cache-Control\" CONTENT=\"no-cache\">
		
	</HEAD>
  
 
	<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/style.css\"/>
	<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/font-awesome.min.css\"/>
	
 	
 	<body>
		<div class=\"container\">
			<header>
				<table border=\"0\" width=\"100%\">
					<tr> 
						<td align=\"left\"> 	<img src=\"/images/logo.png\" alt=\"Logo\" style=\"height:55px;\"/> </td>
						<td align=\"right\"> 	<h1>Home Control </h1></td> 
					</tr>
				</table>
			</header>
			
			<nav>
				<ul>
					<li><a href=\"/cgi-bin/main.cgi\"> 								<i class=\"fa fa-home\"></i>			&nbsp; Home </a></li>
					<li><a href=\"/cgi-bin/main.cgi?command=STATUS-HEATING-ALL\"> 	<i class=\"fa fa-fire\"></i>			&nbsp; Heating </a></li>
					<li><a href=\"/cgi-bin/main.cgi?command=STATUS-SOCKET-ALL\"> 	<i class=\"fa fa-plug\"></i> 	&nbsp; Sockets </a></li>
					<li><a href=\"/cgi-bin/main.cgi?command=STATUS-LIGHT-ALL\"> 	<i class=\"fa fa-lightbulb-o\"></i> 	&nbsp; Lights </a></li>
				</ul>
			</nav>
			
			<article>
";



# Extract the line info
# ---------------------
@options = split(/&/, $line);


$done=0;

# Run though the paremeters and get the command
# ---------------------------------------------
$x=0;
$found=0;
while ($options[$x])
{
	($index, $foo)    = split(/=/,$options[$x]);
	#print "Index [".$index."] Foo [".$foo."]<p>";
	if ( $index eq "command" )
	{
		$found=1;
		$command=$foo;
		last;
	}
	$x++;
} 
if ( $found == 0 )
{
	# if ($line =~ m/SETTIMES-HEATING-0/) 
	# {
		# $command="SETTIMES-HEATING-0";
	# }
	# elsif ($line =~ m/SETBOOST-HEATING-0/) 
	# {
		# $command="SETBOOST-HEATING-0";
	# }
	# else
	# {
		$command="STATUS-ALL-1";
	# }
 }

##print "<hr><p>Command is [".$command."]</p><hr>";



#########################################################################################################
# Handle commands
#########################################################################################################

# If getting BOOST Info - Set the Boost length
# ---------------------
#if ($command eq "GETBOOST-HEATING-0" )
if ( index($command, "GETBOOST") == 0 )
{
	$done=1;
	$mins=0;
	
	($function, $type, $node) = split(/-/, $command);
	
	$res= `perl ./post.cgi "$command"`;
	#print $res;
	
	$res =~ s/GETBOOST-$type-$node=//g;
	$mins=$res / 60;

	print "
	<form action=\"main.cgi\">
		Boost Value <input size=\"6\" type=\"text\" name=\"boostvalue\" value=\"$mins\"> Minutes
		<br><br>
		<input type=\"hidden\" name=\"command\" value=\"SETBOOST-$type-$node\">
		<input type=\"submit\" class=\"button\" name=\"Submit\" value=\"Save $type $node Settings\">	
			
	</form>
	";
	
	#<input type=\"submit\" value=\"Submit\" name=\"SETBOOST-$type-$node\"> </form> </p> \n
	
}


# If setting BOOST Info
# ---------------------
#if ($command eq "SETBOOST-HEATING-0" )
if ( index($command, "SETBOOST") == 0 )
{
	#print "SETBOOST-HEATING-0 <br>";
	
	$done=1;
	$secs=0;
	
	($function, $type, $node) = split(/-/, $command);
			
	$line =~ s/boostvalue=//g;
	$line =~ s/&command=SETBOOST-$type-$node&Submit=Save\+$type\+$node\+Settings//g;
	
	if ( ($line > 0) && ($line <= 120) )   
	{
		$secs=$line * 60;	
		$command="$command-$secs";
		#print "$command";
		
		$res= `perl ./post.cgi "$command"`;
		print "$res - [$line] minutes set";
		print "<br>";
	}
	else
	{	
		print "ERROR: Not a valid value...enter 1 to 120";
	}
	print "<br>";
}




# If a set heating command, set the values
# ----------------------------------------
#if ($command eq "SETTIMES-HEATING-0" )
if ( index($command, "SETTIMES") == 0 )
{
	$done=1;
	
	($function, $type, $node) = split(/-/, $command);
	
	##print "Before $line <br>";

	$line =~ s/=1&/,/g;
	$line =~ s/-/&/g;
	$line =~ s/,B1=Submit//g;

	$line="SETTIMES-$type-$node-".$line;

	$res= `perl ./post.cgi "$line"`;

	##print "After $line <br>";
	##print $res;

	# Set the GET command to force a reload of the settings
	# -----------------------------------------------------
	$command = "GETTIMES-$type-$node";

}



# If a get heating command, display the table - Make sure this is always coded after the SET operation
# -------------------------------------------
#elsif ($command eq "GETTIMES-HEATING-0" )
if ( index($command, "GETTIMES") == 0 )
{
	$done=1;
	
	($function, $type, $node) = split(/-/, $command);
	
	print "<h3>Timer for [$type] [$node]</h3>";
	
	$res= `perl ./post.cgi "GETTIMES-$type-$node"`;
	
	
	###print $res;
	
	@options = split(/&/, $res);
	
	print "<form method=\"run\" action=\"main.cgi\">\n";
	
	print "<table id=\"results\" border=\"1\">";
	
	print "<td> Hour </td> <td> Mon </td> <td> Tue </td> <td> Wed </td> <td> Thu </td> <td> Fri </td> <td> Sat </td> <td> Sun </td> \n";
	for ($x=0; $x<48; $x++)
	{
		print "\n<tr>";
		print "<td>";
		if ( $x % 2 )
		{
			printf("%02d", $x*0.5);
			print ":30"
		}
		else
		{
			printf("%02d", $x/2);
			print ":00"
		}
		print "</td>";
				
		
	    for ($y=0; $y<7; $y++)
	    {
	    	if (index($res, "$y&$x,") != -1)
			{
				$checked="checked";
			}
			else
			{
				$checked="";
			}
			print "<td> <input type=\"checkbox\" name=\"$y-$x\" value=\"1\" $checked> </td>";      
	    }
	    print "</tr>\n";
	}
	print "</table><br><br>";
	
	print "<input type=\"hidden\" name=\"command\" value=\"SETTIMES-$type-$node\">";
	print "<input type=\"submit\" class=\"button\" name=\"Submit\" value=\"Save $type $node Settings\">";

	print "</form> </p> \n";

}





# Handle all other commands 
# -------------------------
if ($done == 0 )
{
	$res= `perl ./post.cgi "$command"`;
	print $res;
	##print "Command [$command] not handled"
}







print "	
	</article>
	<footer>
	
		<a href= \"main.cgi\">Main Menu</a></br>
	</footer>
	
	
	</body>
	</html>
";
