#!/usr/bin/perl

use strict;


my %days;
my %global_service_counter;

while(my $line = <STDIN>)
{

  # 2012-09-12 14:36:43,117 INFO [org.jasig.cas.CentralAuthenticationServiceImpl] - Granted service ticket [ST-720745-dFo5g7d5Bvl1gW5X3FxF-cas] for service [https://my.csumb.edu/] for user [appa9057]

  # $1 - day $2 - time $3 - service $4 - user
	if($line =~ m/(^\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d+ INFO \[org.jasig.cas.CentralAuthenticationServiceImpl\] - Granted service ticket \[[^\]]*] for service \[([^\]]*)] for user \[([^\]]*)]/)
	{

		my $day = $1;
		my $time = $2;
		my $service = $3;
		my $user = $4;


		$service =~ s/^http[s]?:\/\/([^\/]+)\/.*/$1/;
		$service =~s/:\d+$//;


		#print "$day, $service";

		$days{$day}{$service}++;
		$global_service_counter{$service}++;

	}
}


print '{' . "";
print '"cols": [' . "";
my $counter = 0;
print '{"id":"","label":"Date","pattern":"","type":"date"},' . "";
foreach my $service (sort { $global_service_counter{$b} <=> $global_service_counter{$a} } keys %global_service_counter )
{
	$counter++;
	my $total_tickets = $global_service_counter{$service};
	print '{"id":"","label":"' . "$service ($total_tickets)" .'","pattern":"","type":"number"}' . "";
	if ($counter != keys %global_service_counter)
	{
		print ',' . "";
	}

}

print '],' . "";


print '"rows": [' . "";
my $dcount = 0;
my $total_day_count = keys %days;
foreach my $day (sort keys %days)
{
	++$dcount;
	#print "###################### $dcount";


	my ($year, $month, $day_of_month) = split(/-/, $day);
	$month =~ s/^0+//;
	$month -= 1;
	$day_of_month =~ s/^0+//;

	print '{"c":[{"v":"Date(' . "$year, $month, $day_of_month" . ')","f":null},' . "";

	#print "$day,";
	my $i = 0;
 	foreach my $service (sort {$global_service_counter{$b} <=> $global_service_counter{$a}} keys %global_service_counter)
 	{
 		$i++;
 		my $count = $days{$day}{$service};

 		#print "#################### $day - $service -  $count";
 		if($count == 0)
 		{
 			$count = 0;
 		}

 		print '{"v":' . $count . ',"f":null}' . "";
 		if ($i != keys %global_service_counter)
		{
			print ',' . "";
		}


 	}
 	print ']}' . "";
 	if ($dcount != $total_day_count)
 	{
 		print ',' . "";
 	}


}

print ']' . "";
print '}' . "";
