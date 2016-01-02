#!/usr/bin/perl
use Fcntl ':flock';
use XML::Parser;

# BS Counter v2.0.0
# Utility to weed out entries in the data file

if (!$ARGV[0]) { print "Usage: $0 [data file(s)]\n"; }

foreach $file (@ARGV)
{
	&parse_xml($file);

	$i = 0;
	foreach my $tld (sort {$geographic{$b} <=> $geographic{$a}} keys %geographic) {
		$i++;
		if ($i == 20) {
			$geographic_min = int($geographic{$tld}/2); last;
		}
	}

	$i = 0;
	foreach my $term (sort {$terms{$b} <=> $terms{$a}} keys %terms) {
		$i++;
		if ($i == 20) {
			$terms_min = int($terms{$term}/2); last;
		}
	}

	$i = 0;
	foreach my $ref (sort {$referrers{$b} <=> $referrers{$a}} keys %referrers) {
		$i++;
		if ($i == 20) {
			$referrers_min = int($referrers{$ref}/2); last;
		}
	}

	open(XML, ">$file");
	flock(XML, LOCK_EX);
	seek(XML, 0, 0);
	truncate(XML, 0);
	print XML "<?xml version=\"1.0\"?>\n";
	print XML "<counter>\n";
	print XML "\t<total>$total</total>\n";
	print XML "\t<today time=\"$today[0]\" host=\"$today[1]\">$today[2]</today>\n";
	print XML "\t<geographic>\n";
	foreach my $tld (keys %geographic) {
		if ($geographic{$tld} >= $geographic_min) {
			print XML "\t\t<country tld=\"$tld\" hits=\"$geographic{$tld}\" />\n";
		}
	}
	print XML "\t</geographic>\n";
	print XML "\t<browsers>\n";
	foreach my $agent (keys %browsers) {
		print XML "\t\t<agent name=\"$agent\" hits=\"$browsers{$agent}\" />\n";
	}
	print XML "\t</browsers>\n";
	print XML "\t<platforms>\n";
	foreach my $os (keys %platforms) {
		print XML "\t\t<os name=\"$os\" hits=\"$platforms{$os}\" />\n";
	}
	print XML "\t</platforms>\n";
	print XML "\t<terms>\n";
	foreach my $term (keys %terms) {
		if ($terms{$term} >= $terms_min) {
			print XML "\t\t<term value=\"$term\" hits=\"$terms{$term}\" />\n";
		}
	}
	print XML "\t</terms>\n";
	print XML "\t<referrers>\n";
	foreach my $ref (keys %referrers) {
		if ($referrers{$ref} >= $referrers_min) {
			print XML "\t\t<ref url=\"$ref\" hits=\"$referrers{$ref}\" />\n";
		}
	}
	print XML "\t</referrers>\n";
	print XML "\t<hosts>\n";
	foreach my $host (@hosts) {
		print XML "\t\t<host value=\"$host\" />\n";
	}
	print XML "\t</hosts>\n";
	print XML "</counter>";
	close(XML);
}

#
# XML Parsing Routines
#

sub parse_xml {
	open(XML, $_[0]);
	flock(XML, LOCK_SH);
	while (my $line = <XML>) {
		if ($line =~ /<ref url=\"(.*)\" hits=\"(\d+)\" \/>/) { $referrers{$1} = $2; }
		elsif ($line =~ /<host value=\"(.*)\" \/>/) { push(@hosts, $1); }
		elsif ($line =~ /<term value=\"(.*)\" hits=\"(\d+)\" \/>/) { $terms{$1} = $2; }
		elsif ($line =~ /<country tld=\"(.*)\" hits=\"(\d+)\" \/>/) { $geographic{$1} = $2; }
		elsif ($line =~ /<agent name=\"(.*)\" hits=\"(\d+)\" \/>/) { $browsers{$1} = $2; }
		elsif ($line =~ /<os name=\"(.*)\" hits=\"(\d+)\" \/>/) { $platforms{$1} = $2; }
		elsif ($line =~ /<today time=\"(\d+)\" host=\"(.*)\">(\d+)<\/today>/) { $today[0] = $1; $today[1] = $2; $today[2] = $3; }
		elsif ($line =~ /<total>(\d+)<\/total>/) { $total = $1; }
	}
	close(XML);
}
