#!/usr/bin/perl -w
use strict;
#####################
# BS Counter (v2.5.3)
# Copyright 1999-2005 Brian Stanback <brian at stanback dot net>
# This software is protected under the GNU General Public License (see LICENSE)

#
# Set config options (see the docs/README for config instructions)
#

# WWW path to digit images (include trailing slash)
my $digits_url = "/counter//images/digits/";

# Directory where digit images are located (include trailing slash)
my $digits_dir = "/home/sites/abna1611.com/public_html/counter/images/digits/";

# Stats page header html
my $header = "/home/sites/abna1611.com/public_html/counter/templates/header.html";

# Stats page footer html
my $footer = "/home/sites/abna1611.com/public_html/counter/templates/footer.html";

#
# Begin script
#

my $total; my $found_total = 0;
my @today; my $found_today = 0;
my %geographic; my $geographic_total = 0;
my %browsers; my $browsers_total = 0;
my %platforms; my $platforms_total = 0;
my @referrers;

my %in;
&getvars;
my $file = $in{'page'};

# Print the header
print "Content-type: text/html\n\n";
open(FILE, $header);
while (<FILE>) { $_ =~ s/<!--page-->/Perl Counter Setup/gi; print; }
close(FILE);


my $digits;
opendir(DIGITS, $digits_dir);
while (my $digit = readdir(DIGITS)) {
	if ($digit ne '.' and $digit ne '..') { $digits .= "<option>$digit</option>"; }
}
closedir(DIGITS);

if ($in{'step'}) {
	if (!$in{'name'}) {
		print "Please go back and ensure you have filled in the name of your counter.";
	} else {
		print "<p>The counter is ready to be placed on your page.\n";
		if ($in{'type'} eq "text") {
			if ($ENV{'SCRIPT_NAME'}) { $ENV{'SCRIPT_NAME'} =~ s/setup.cgi/count.cgi/i; }
			else {$ENV{'SCRIPT_NAME'} = "count.cgi"; }
			print "To add the counter to your web page, make sure you have server side includes (SSI) enabled (you may have to name your document page.shtml rather than .htm or .html). Then add the following into your html source:<br /><br />\n";
			print "<code>&lt;!--#include virtual=\"$ENV{'SCRIPT_NAME'}?page=$in{'name'}&amp;type=" . $in{'type'};
			if ($in{'reloads'}) { print "&amp;reloads=1"; }
			print "\"--&gt;</code><br /><br />\n";
		} elsif ($in{'type'} eq "image") {
			if ($ENV{'SCRIPT_NAME'}) { $ENV{'SCRIPT_NAME'} =~ s/setup.cgi/count.cgi/i; }
			else {$ENV{'SCRIPT_NAME'} = "count.cgi"; }
			my $imgtype;
			opendir(DIGITS, "$digits_dir$in{'style'}");
			while (my $digit = readdir(DIGITS)) {
				if ($digit ne '..' and $digit ne '.' and $digit =~ /\.(.*)$/) { $imgtype = $1; last; }
			}
			closedir(DIGITS);
			print "Your counter digits will look like this...<br /><br /><img src=\"$digits_url$in{'style'}/0.$imgtype\"><img src=\"$digits_url$in{'style'}/1.$imgtype\"><img src=\"$digits_url$in{'style'}/2.$imgtype\"><img src=\"$digits_url$in{'style'}/3.$imgtype\"><img src=\"$digits_url$in{'style'}/4.$imgtype\"><img src=\"$digits_url$in{'style'}/5.$imgtype\"><img src=\"$digits_url$in{'style'}/6.$imgtype\"><img src=\"$digits_url$in{'style'}/7.$imgtype\"><img src=\"$digits_url$in{'style'}/8.$imgtype\"><img src=\"$digits_url$in{'style'}/9.$imgtype\"><br /><br />\n";
			print "To add the counter to your web page, make sure you have server side includes (SSI) enabled (you may have to name your document page.shtml rather than .htm or .html). Then add the following into your html source:<br /><br />\n";
			print "<code>&lt;!--#include virtual=\"$ENV{'SCRIPT_NAME'}?page=$in{'name'}&amp;type=image&amp;style=$in{'style'}&amp;imgtype=$imgtype&amp;nbdigits=$in{'nbdigits'}";
			if ($in{'reloads'}) { print "&amp;reloads=1"; }
			print "\"--&gt;</code><br /><br />\n";
		} else {
			if ($ENV{'SCRIPT_NAME'}) { $ENV{'SCRIPT_NAME'} =~ s/setup.cgi/gd-count.cgi/i; }
			else {$ENV{'SCRIPT_NAME'} = "gd-count.cgi"; }
			my $imgtype;
			opendir(DIGITS, "$digits_dir$in{'style'}");
			while (my $digit = readdir(DIGITS)) {
				if ($digit ne '..' and $digit ne '.' and $digit =~ /\.(.*)$/) { $imgtype = $1; last; }
			}
			closedir(DIGITS);
			if ($imgtype eq "png") {
				open(DIM, "$digits_dir$in{'style'}/dim");
				my $dim = <DIM>;
				close(DIM);
				chomp($dim);
				my($x, $y) = split(/x/, $dim);
				print "Your counter digits will look like this...<br /><br /><img src=\"$digits_url$in{'style'}/0.$imgtype\"><img src=\"$digits_url$in{'style'}/1.$imgtype\"><img src=\"$digits_url$in{'style'}/2.$imgtype\"><img src=\"$digits_url$in{'style'}/3.$imgtype\"><img src=\"$digits_url$in{'style'}/4.$imgtype\"><img src=\"$digits_url$in{'style'}/5.$imgtype\"><img src=\"$digits_url$in{'style'}/6.$imgtype\"><img src=\"$digits_url$in{'style'}/7.$imgtype\"><img src=\"$digits_url$in{'style'}/8.$imgtype\"><img src=\"$digits_url$in{'style'}/9.$imgtype\"><br /><br />\n";
				print "To add the counter to your web page, add the following into your html source, also note that you need to edit the gd-count.cgi script and add your domain/site to the \@allowed.<br /><br />\n";
				print "<code>&lt;img src=\"$ENV{'SCRIPT_NAME'}?page=$in{'name'}&amp;style=$in{'style'}&amp;x=$x&amp;y=$y&amp;nbdigits=$in{'nbdigits'}";
				if ($in{'reloads'}) { print "&amp;reloads=1"; }
				print "\"&gt;</code><br /><br />\n";
			}
			else {
				print "Error: The images for the selected digit style are not in png format, please go back and select a different style.\n";
			}
		}
		print "Note: To make the counter hidden, add <code>&lt;div style=\"display: none; visibility: hidden;\"&gt;</code> before the code and <code>&lt;/div&gt;</code> after the code.<br><br>\n";
		print "Once you have installed the counter, you can view your site statictics by linking to or visiting the following URL:<br /><br />\n";
		print "<a href=\"stats.cgi?page=$in{'name'}\">http://www.abna1611.com/counter/stats.cgi?page=$in{'name'}</a></p>\n";
	}
} else {
	print "<p>Please select a counter type, name, and style. The GD image counter will allow you to insert an img tag on your page rather than having to use SSI.</p>\n";
	print "<form action=\"$ENV{'SCRIPT_NAME'}\" method=\"get\">\n";
	print "<input type=\"hidden\" name=\"step\" value=\"1\" />\n";
	print "<table cellspacing=\"0\" cellpadding=\"2\">\n";
	print "<tr><td>Counter Type:</td><td><select name=\"type\" class=\"input\"><option value=\"hidden\">Hidden Counter</option><option selected value=\"text\">Text Counter</option><option value=\"image\">Image Counter</option><option value=\"gdimage\">Image Counter (GD)</option></select></td></tr>\n";
	print "<tr><td>Counter Name (numbers and letters only):&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td><input type=\"text\" class=\"input\" name=\"name\" size=\"20\" /></td></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	print "<tr><td>Digit Style (for image counter):</td><td><select class=\"input\" name=\"style\">$digits</select></td></tr>\n";
	print "<tr><td>Number of digits (adds leading zeros):</td><td><select name=\"nbdigits\" class=\"input\"><option value=\"1\">1</option><option value=\"2\">2</option><option value=\"3\">3</option><option value=\"4\">4</option><option value=\"5\">5</option><option value=\"6\">6</option><option value=\"7\">7</option><option value=\"8\">8</option><option value=\"9\">9</option></select></td></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	print "<tr><td>Count if user reloads/refreshes page:</td><td><input type=\"checkbox\" name=\"reloads\" value=\"1\" /></td></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	print "<tr><td>&nbsp;</td><td><input type=\"submit\" class=\"submit\" value=\"Generate HTML\" /></td></tr>\n";
	print "</table>\n";
	print "</form>\n";
}

# Print the footer
open(FILE, $footer);
while(<FILE>) { print; }
close(FILE);

#
# Get query string configuration variables (strip everything that isn't a number or letter)
#

sub getvars {
	if ($ENV{QUERY_STRING}) {
		for (split /\&/, $ENV{QUERY_STRING}) {
			my($key, $val) = split /=/;
			$val =~ s/%([0-9a-fA-F]{2})/chr(hex($1))/ge;
			$val =~ s/[^\w_-]//g;
			$in{$key} = $val;
		}
	}
}
