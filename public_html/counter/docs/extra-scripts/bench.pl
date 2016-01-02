#!/usr/bin/perl
use Benchmark qw(:all);

# On my k6-400 the average execution time averaged 0.093 seconds

# Quick benchmark

timethis(1000, \&exec_count);
sub exec_count {
	$hits = `../../count.cgi`;
}
