#!/usr/bin/perl -w
use strict;
use Fcntl ":flock";
use Fcntl_flock;
use GD;
#####################
# BS Counter (v2.5.3)
# Copyright 1999-2005 Brian Stanback <brian at stanback dot net>
# This software is protected under the GNU General Public License (see LICENSE)

#
# Set config options (see the docs/README for config instructions)
#

# Sites allowed to use the counter.
my @allowed = ("abna1611.com");

# Directory where png digit images are located (include trailing slash)
my $digits_dir = "/home/sites/abna1611.com/public_html/counter/images/digits/";

# Directory that houses the xml/log data files (include trailing slash)
my $data_dir = "/home/sites/abna1611.com/public_html/counter/data/";

#
# Begin script
#

my @time = localtime(time);
my $time = $time[7] . $time[5];
my $total = 0;
my $deny_update = 0;
my @hosts;

my %in;
&prepareInput;
my $file = $in{'page'} || "default";
my $style = $in{'style'} || "default";
my $nbdigits = $in{'nbdigits'} || 1;
my $allow_reloads = $in{'reloads'} || 0;
my $x = $in{'x'};
my $y = $in{'y'};

# Check referer for proper access
my $verified = 0;
if ($ENV{'HTTP_REFERER'}) {
	foreach my $host (@allowed) {
		if ($ENV{'HTTP_REFERER'} =~ /$host/i) { $verified = 1; } 
	}
	if ($verified == 0) { exit(0); }
}

# Resolve hostname if web server hasnt already (for country statistics)
if (!$ENV{'REMOTE_HOST'} && $ENV{'REMOTE_ADDR'}) {
	my @subnet_numbers = split (/\./, $ENV{'REMOTE_ADDR'});
	$ENV{'REMOTE_HOST'} = gethostbyaddr(pack("C4", @subnet_numbers), 2) || $ENV{'REMOTE_ADDR'};
}

# Parse the XML stats file
if (-f "$data_dir$file.xml") {
	&parse_xml("$data_dir$file.xml");
}

# Count hits in interm log file while checking for reloads
if (-f "$data_dir$file.log") {
	$deny_update = count_interm("$data_dir$file.log", $allow_reloads);
}

if ($deny_update != 1 && $allow_reloads != 1) {
	foreach my $host (@hosts) {
		if ($host eq $ENV{'REMOTE_HOST'}) { $deny_update = 1; last; }
	}
}

# Append hit to interm log file
if ($deny_update != 1) {
	if (-d "$data_dir") {
		open(LOG, ">>$data_dir$file.log");
		Fcntl_flock::flock(LOG, LOCK_EX);
		print LOG $time . "\t" . $ENV{'HTTP_USER_AGENT'} . "\t" . $ENV{'HTTP_REFERER'} . "\t" . $ENV{'REMOTE_HOST'} . "\n";
		Fcntl_flock::flock(LOG, LOCK_UN);
		close(LOG);
		$total++;
	} else {
		print "Counter Error: Data directory not found\n";
	}
}

#
# Print out the count
#

$total = '0' x ($nbdigits - length($total)) . $total;
&doimage($total);

#
# GD image creation
#

sub doimage {
	my ($total) = @_;
	if (!$x or !$y) {
		open(DIM, "$digits_dir$style/dim");
		my $dim = <DIM>;
		close(DIM);
		chomp($dim);
		($x, $y) = split(/x/, $dim);
	}
	my $imx = (length($total) * $x);
	my $imy = $y;
	my $image = new GD::Image($imx,$imy);
	my $magenta = $image->colorAllocate(255, 0, 255);
	$image->transparent($magenta);
	my $startx = 0;
	my $endx = $x;
	foreach my $digit (split(//, $total))
	{
 		my $tile = newFromPng GD::Image("$digits_dir$style/$digit.png");
		$image->setTile($tile);
		$image->filledRectangle($startx,0,$endx,$y,gdTiled);
		$startx += $x;
		$endx += $x;
	}
	print "Content-type: image/png\n\n";
	print $image->png;
}


#
# XML Parsing Routines
#

sub parse_xml {
	open(XML, $_[0]);
	Fcntl_flock::flock(XML, LOCK_SH);
	while (my $line = <XML>) {
		if ($line =~ /<total>(\d+)<\/total>/) { $total = $1; }
		elsif ($line =~ /<host value=\"(.*)\" \/>/) { push(@hosts, $1); }
	}
	Fcntl_flock::flock(XML, LOCK_UN);
	close(XML);
}

#
# Interm log processing
#

sub count_interm {
	open(LOG, $_[0]);
	Fcntl_flock::flock(LOG, LOCK_SH);
	while (my $line = <LOG>) {
		$total++;
		if ($_[1] != 1) {
			chomp($line);
			my ($access_time, $user_agent, $referer, $host) = split(/\t/, $line);
			if ($host eq $ENV{'REMOTE_HOST'}) { $deny_update = 1; }
		}
	}
	Fcntl_flock::flock(LOG, LOCK_UN);
	close(LOG);	
	return $deny_update;
}

#
# Get/prepare environment variables (strip invalid characters)
#

sub prepareInput {
	if ($ENV{QUERY_STRING}) {
		for (split(/\&/, $ENV{'QUERY_STRING'})) {
			my($key, $val) = split /=/;
			$val =~ s/%([0-9a-fA-F]{2})/chr(hex($1))/ge;
			$val =~ s/[^[A-Za-z0-9_-]//g;
			$in{$key} = $val;
		}
	}
	if ($ENV{'HTTP_USER_AGENT'}) { $ENV{'HTTP_USER_AGENT'} =~ s/[^A-z0-9-_.+=\&\/\?\: ]//g; }
	if ($ENV{'HTTP_REFERER'}) { $ENV{'HTTP_REFERER'} =~ s/[^A-z0-9-_.+=\&\/\?\: ]//g; }
}
