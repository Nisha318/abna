#!/usr/bin/perl -w
use strict;
use Fcntl ':flock';
#####################
# BS Counter (v2.5.3)
# Copyright 1999-2005 Brian Stanback <brian at stanback dot net>
# This software is protected under the GNU General Public License (see LICENSE)

#
# Set config options (see the docs/README for config instructions)
#

# Directory that houses the xml data files (include trailing slash)
my $data_dir = "./data/";

# Stats page header html
my $header = "./templates/header.html";

# Stats page footer html
my $footer = "./templates/footer.html";

# WWW path to the image directory (include trailing slash)
my $image_dir = "./images/";

#
# First check for redirect
#

if ($ENV{'QUERY_STRING'} =~ /redirect=(.*)/) {
	print "Location: $1\n\n";
	exit(0);
}

#
# Begin script
#

my @time = localtime(time);
my $time = $time[7] . $time[5];
my $total;
my @today;
my %geographic; my $geographic_total = 0;
my %agents; my $agents_total = 0;
my %platforms; my $platforms_total = 0;
my %spiders; my $spiders_total = 0;
my %terms; my $terms_total = 0;
my %referrers; my $referrers_total = 0;
my @hosts;

my %in;
&getvars;
my $file = $in{'page'};

# List of agents (Name => Regex)
my @agents_match = (
		"Mozilla Firefox 1.x => Firefox",
		"Internet Explorer 7 => MSIE 7",
		"Internet Explorer 6 => MSIE 6",
		"Internet Explorer 5 => MSIE 5",
		"Internet Explorer &le;4 => MSIE",
		"Safari => Safari",
		"Pocket Internet Explorer => Windows CE|Pocket Internet Explorer",
		"AvantGo => AvantGo",
		"Netscape 8 => Netscape/8|NS8",
		"Netscape 7 => Netscape/7",
		"Netscape 6 => Netscape6",
		"Opera 9 => Opera/9|Opera 9",
		"Opera 8 => Opera/8|Opera 8",
		"Opera 7 => Opera/7|Opera 7",
		"Konqueror => Konqueror",
		"Flock => Flock",
		"PlayStation Portable => PlayStation",
		"WebTV => WebTV",
		"Java => Java|Sun",
		"Opera &le;6 => Opera",
		"Download Agents => File|file|Fetch|fetch|Download|download|Wget|Get|get|Zilla",
		"Mozilla/Gecko => Gecko",
		"Netscape Navigator => Mozilla/[3-4]",
	);
	
# List of spiders/robots (Name => Regex)
my @spiders_match = (
		"Google => Google",
		"AltaVista => Scooter",
		"Overture => MMCrawler|WebCrawler",
		"Yahoo => Yahoo",
		"MSN => msnbot",
		"FAST => FAST",
		"Ask Jeeves/Teoma => Teoma",
		"Alexa => alexa|ia_archiver",
		"Infoseek => Infoseek|Ultraseek",
		"Lycos => Lycos",
		"Inktomi/HotBot => Slurp",
		"Gigablast => Gigabot",
		"Baidu => Baiduspider",
		"Entireweb => Speedy Spider",
	);

# List of Platforms
my @os_match = (
		"Windows XP => Windows NT 5.1|Windows XP",
		"Windows 2000 => Windows NT 5.0|Windows 2000",
		"Windows NT => Windows NT|WinNT",
		"Windows 9x/ME => Windows|Win98|Win95",
		"Mac OSX => Mac OS X",
		"Mac PowerPC => Mac|PPC",
		"Linux => Linux",
		"HP-UX => HP-UX",
		"SunOS => SunOS",
		"BeOS => BeOS",
		"BSD => BSD",
		"UNIX => UNIX",
		"IRIX => IRIX",
		"QNX => QNX",
		"OS/2 => OS/2",
		"WebTV => WebTV",
	);

# Descriptions for all the crazy top-level domains out there
my %domains = (
		com => "Int/Commercial",
		org => "Int/Organization",
		net => "Int/Network",
		gov => "US Government",
		mil => "US Military",
		edu => "US Educational",
		int => "International",
		aero => "Air-transport industry",
		biz => "Int/Business",
		coop => "Int/Cooperatives",
		info => "Int/Informative",
		museum => "Int/Museum",
		pro => "Int. Professional",
		af => "Afghanistan",
		al => "Albania",
		dz => "Algeria",
		as => "American Somoa",
		ad => "Andorra",
		ao => "Angola",
		ai => "Anguilla",
		aq => "Antarctica",
		ag => "Antigua and Barbuda",
		ar => "Argentina",
		am => "Armenia",
		aw => "Aruba",
		ac => "Ascension Island", 
		au => "Australia",
		at => "Austria",
		az => "Azerbaijan",
		bh => "Bahrain",
		bd => "Bangladesh",
		bb => "Barbados",
		by => "Belarus",
		be => "Belgium",
		bz => "Belize",
		bj => "Benin",
		bm => "Bermuda",
		bt => "Bhutan",
		bo => "Bolivia",
		ba => "Bosnia and Herzegovina",
		bw => "Botswana",
		bv => "Bouvet Island",
		br => "Brazil",
		io => "British Indian Ocean Territory",
		bn => "Brunei",
		bg => "Bulgaria",
		bf => "Burkina Faso",
		bi => "Burundi",
		kh => "Cambodia",
		cm => "Cameroon",
		ca => "Canada",
		cv => "Cape Verde",
		cf => "Central African Republic",
		td => "Chad",
		gg => "Channel Islands - Guernsey",
		je => "Channel Islands - Jersey",
		cl => "Chile",
		cn => "China",
		cx => "Christmas Island",
		cc => "Cocos (Keeling) Islands",
		co => "Colombia",
		km => "Comoros",
		cg => "Congo",
		ck => "Cook Islands",
		cr => "Costa Rica",
		ci => "Coted Ivoire",
		hr => "Croatia",
		cu => "Cuba",
		cy => "Cyprus",
		cz => "Czech Republic",
		dk => "Denmark",
		dj => "Djibouti",
		dm => "Dominica",
		do => "Dominican Republic",
		tp => "East Timor",
		ec => "Ecuador",
		eg => "Egypt",
		sv => "El Salvador",
		gq => "Equatorial Guinea",
		er => "Eritrea",
		ee => "Estonia",
		et => "Ethiopia",
		fk => "Falklands Islands",
		fo => "Faroe Islands",
		fj => "Fiji",
		fi => "Finland",
		fr => "France",
		gf => "French Guiana",
		pf => "French Polynesia",
		tf => "French Southern Territories",
		fx => "French Metropolitan",
		ga => "Gabon",
		ge => "Georgia",
		de => "Germany",
		gh => "Ghana",
		gi => "Gibraltar",
		gr => "Greece",
		gl => "Greenland",
		gd => "Grenada",
		gp => "Guadeloupe",
		gu => "Guam",
		gt => "Guatemala",
		gn => "Guinea",
		gy => "Guyana",
		ht => "Haiti",
		hm => "Heardand McDonald Islands",
		hn => "Honduras",
		hk => "HongKong",
		hu => "Hungary",
		is => "Iceland",
		in => "India",
		id => "Indonesia",
		ir => "Iran",
		iq => "Iraq",
		ie => "Ireland",
		il => "Israel",
		it => "Italy",
		jm => "Jamaica",
		jp => "Japan",
		jo => "Jordan",
		kz => "Kazakhstan",
		ke => "Kenya",
		ki => "Kiribati",
		kp => "Peoples Republic of Democratic Korea",
		kr => "Republic of Korea",
		kw => "Kuwait",
		kg => "Kyrgyzstan",
		la => "Laos",
		lv => "Latvia",
		lb => "Lebanon",
		ls => "Lesotho",
		lr => "Liberia",
		ly => "Libyan Arab Jamahiriya",
		li => "Liechtenstein",
		lt => "Lithuania",
		lu => "Luxembourg",
		mo => "Macao",
		mk => "Macedonia",
		mw => "Malawi",
		my => "Malaysia",
		ml => "Mali",
		mt => "Malta",
		mh => "Marshall Islands",
		mq => "Martinique",
		mr => "Mauritania",
		mu => "Mauritius",
		yt => "Mayotte",
		mx => "Mexico",
		fm => "Micronesia",
		md => "Moldova",
		mc => "Monaco",
		mn => "Mongolia",
		ms => "Montserrat",
		ma => "Morocco",
		mz => "Mozambique",
		mm => "Myanmar",
		na => "Namibia",
		nr => "Nauru",
		np => "Nepal",
		nl => "Netherlands",
		an => "Netherlands Antilles",
		nc => "New Caledonia",
		nz => "New Zealand",
		ni => "Nicaragua",
		ne => "Niger",
		ng => "Nigeria",
		nu => "Niue",
		nf => "Norfolk Island",
		mp => "Northern Mariana Islands",
		no => "Norway",
		om => "Oman",
		pk => "Pakistan",
		pw => "Palau",
		pa => "Panama",
		pq => "Papua New Guinea",
		py => "Paraguay",
		pe => "Peru",
		ph => "Philippines",
		pn => "Pitcairn",
		pl => "Poland",
		pt => "Portugal",
		pr => "Puerto Rico",
		qa => "Qatar",
		re => "Reunion",
		ro => "Romania",
		ru => "Russia",
		rw => "Rwanda",
		kn => "Saint Kitts and Nevis",
		lc => "Saint Lucia",
		vc => "Saint Vincent and the Grenadines",
		ws => "Samoa",
		sm => "San Marino",
		st => "Sao Tomeand Prin cipe",
		sa => "Saudi Arabia",
		sn => "Senegal",
		sc => "Seychelles",
		sl => "Sierra Leone",
		sg => "Singapore",
		sk => "Slovakia",
		si => "Slovenia",
		sb => "Solomon Islands",
		so => "Somalia",
		za => "South Africa",
		gs => "South Georgia and the South Sandwich Islands",
		es => "Spain",
		lk => "Sri Lanka",
		sh => "St. Helena",
		pm => "St. Pierreand Miquelon",
		sd => "Sudan",
		sr => "Suriname",
		sj => "Svalbardand Jan Mayen Islands",
		sz => "Swaziland",
		se => "Sweden",
		ch => "Switzerland",
		sy => "Syria",
		tw => "Taiwan",
		tj => "Tajikistan",
		tz => "Tanzania",
		th => "Thailand",
		bs => "The Bahamas",
		ky => "The Cayman Islands",
		to => "Tonga",
		tt => "Trinidad and Tobago",
		tn => "Tunisia",
		tk => "Tokelau",
		tr => "Turkey",
		tm => "Turkmenistan",
		tc => "Turks and Caicos Islands",
		tv => "Tuvalu",
		ug => "Uganda",
		ua => "Ukraine",
		ae => "United Arab Emirates",
		uk => "United Kingdom",
		us => "United States",
		um => "United States Minor Outlying Islands",
		uy => "Urugauy",
		uz => "Uzbekistan",
		vu => "Vanuatu",
		va => "Vatican City State",
		ve => "Venezuela",
		vn => "Vietnam",
		vg => "Virgin Islands (British)",
		vi => "Virgin Islands (US)",
		wf => "Wallis and Futuna Islands",
		eh => "Western Sahara",
		ye => "Yemen",
		yu => "Yugoslavia",
		zr => "Zaire",
		zm => "Zambia",
		zw => "Zimbabwe",
		ip => "Int/IP Address"
	);

# Print the header
print "Content-type: text/html\n\n";
if (-f "$header") {
	open(FILE, $header);
	if ($file) {
		while(<FILE>) { $_ =~ s/<!--page-->/Counter Stats for <span class=\"g\">$file<\/span>/gi; print; }
	} else {
		while(<FILE>) { $_ =~ s/<!--page-->/Counter Stats/gi; print; }
	}
	close(FILE);
}

if ($file and (-f "$data_dir$file.xml" or -f "$data_dir$file.log")) {
	# Parse the XML stats file
	if (-f "$data_dir$file.xml") {
		parse_xml("$data_dir$file.xml");
	}
	
	# Parse intermediate log file and update stats/xml data file
	if (-s "$data_dir$file.log") {
		parse_log($data_dir, $file);
	}

	# Grab the totals so we can generate percentages
	foreach my $agent (keys %agents) {
		$agents_total += $agents{$agent};
	}
	foreach my $os (keys %platforms) {
		$platforms_total += $platforms{$os};
	}
	foreach my $spider (keys %spiders) {
		$spiders_total += $spiders{$spider};
	}
	foreach my $tld (keys %geographic) {
		if ($domains{$tld}) {
			$geographic_total += $geographic{$tld};
		}
	}
	foreach my $term (keys %terms) {
		$terms_total += $terms{$term};
	}

	#
	# Print the html
	#

	while ($total =~ s/(.*\d)(\d\d\d)/$1,$2/) {}
	while ($today[1] =~ s/(.*\d)(\d\d\d)/$1,$2/) {}

	print "<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\n";
	print "<tr><td>Total Hits:</td><td>$total</td></tr>\n";
	print "<tr><td>Hits Today:</td><td>$today[1]</td></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	print "<tr><th colspan=\"2\">Browsers</th></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	foreach my $agent (sort {$agents{$b} <=> $agents{$a}} keys %agents) {
		print "<tr><td>$agent</td><td>".mkbar($agents{$agent}, $agents_total, "red", 1)."</td></tr>\n";
	}
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	print "<tr><th colspan=\"2\">Platforms</th></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	foreach my $os (sort {$platforms{$b} <=> $platforms{$a}} keys %platforms) {
		print "<tr><td>$os</td><td>".mkbar($platforms{$os}, $platforms_total, "blue", 1)."</td></tr>\n";
	}
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	if (scalar keys(%spiders) > 0) {
		print "<tr><th colspan=\"2\">Spiders &amp; Robots</th></tr>\n";
		print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
		foreach my $spider (sort {$spiders{$b} <=> $spiders{$a}} keys %spiders) {
			print "<tr><td>$spider</td><td>".mkbar($spiders{$spider}, $spiders_total, "green", 1)."</td></tr>\n";
		}
		print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	}
	print "<tr><th colspan=\"2\">Top Countries</th></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	my $i = 0;
	foreach my $tld (sort {$geographic{$b} <=> $geographic{$a}} keys %geographic) {
		if ($domains{$tld}) {
			if ($i == 20) { last; }
			if (!$domains{$tld}) { $domains{$tld} = $tld; }
			print "<tr><td>$domains{$tld}</td><td>".mkbar($geographic{$tld}, $geographic_total, "purple", 1)."</td></tr>\n";
			$i++;
		}
	}
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	if (scalar keys(%terms) > 0) {
		my $i = 0;
		my ($term2, $term3);
		print "<tr><th colspan=\"2\">Top Search Words</th></tr>\n";
		print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
		foreach my $term (sort {$terms{$b} <=> $terms{$a}} keys %terms) {
			if ($i == 20) { last; }
			print "<tr><td>$term</td><td>".mkbar($terms{$term}, $terms_total, "orange", 2)."</td></tr>\n";
			$i++;
		}
		print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	}
	if (scalar keys(%referrers) > 0) {
		my $i = 0;
		my ($term2, $term3);
		print "<tr><th colspan=\"2\">Top Referrers</th></tr>\n";
		print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
		foreach my $ref (sort {$referrers{$b} <=> $referrers{$a}} keys %referrers) {
			if ($i == 20) { last; }
			my $trunc_ref = substr($ref, 0, 90);
			if ($trunc_ref ne $ref) { $trunc_ref .= '...'; }
			print "<tr><td colspan=\"2\"><a href=\"" . $ENV{'SCRIPT_NAME'} . "?redirect=$ref\">$trunc_ref ($referrers{$ref})</a></td></tr>\n";
			$i++;
		}
		print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	}
	print "<tr><th colspan=\"2\">Last 20 Accesses</th></tr>\n";
	print "<tr><td colspan=\"2\">&nbsp;</td></tr>\n";
	foreach my $host (@hosts) {
		print "<tr><td colspan=\"2\">$host</td></tr>\n";
	}
	print "</table>\n";
} else {
	if (-d $data_dir and !$file) {
		print "<table width=\"100%\" cellspacing=\"0\" cellpadding=\"0\">\n";
		print "<tr><th>Available Pages</th></tr>\n";
		print "<tr><td>&nbsp;</td></tr>\n";
		opendir(DATA, $data_dir);
		while (my $file = readdir(DATA)) {
			if ($file =~ s/\.log$//g) {
				print "<tr><td>&#183; <a href=\"$ENV{'SCRIPT_URI'}?page=$file\">$file</a></td></tr>\n";
			}
		}
		closedir(DATA);
		print "</table>\n";
	} else {
		print "Error: Cannot open the specified counter. This may be because you have not yet placed the counter on your webpage, once the counter receives the first hit, the stats will become available.";
	}
}

# Print the footer
if (-f "$footer") {
	open(FILE, $footer);
	while(<FILE>) { print; }
	close(FILE);
}

#
# XML Parsing Routines
#

sub parse_xml {
	open(XML, $_[0]);
	flock(XML, LOCK_EX);
	while (my $line = <XML>) {
		if ($line =~ /<ref url=\"(.*)\" hits=\"(\d+)\" \/>/) { $referrers{$1} = $2; }
		elsif ($line =~ /<host value=\"(.*)\" \/>/) { push(@hosts, $1); }
		elsif ($line =~ /<term value=\"(.*)\" hits=\"(\d+)\" \/>/) { $terms{$1} = $2; }
		elsif ($line =~ /<spider name=\"(.*)\" hits=\"(\d+)\" \/>/) { $spiders{$1} = $2; }
		elsif ($line =~ /<country tld=\"(.*)\" hits=\"(\d+)\" \/>/) { $geographic{$1} = $2; }
		elsif ($line =~ /<agent name=\"(.*)\" hits=\"(\d+)\" \/>/) { $agents{$1} = $2; }
		elsif ($line =~ /<os name=\"(.*)\" hits=\"(\d+)\" \/>/) { $platforms{$1} = $2; }
		elsif ($line =~ /<today time=\"(\d+)\">(\d+)<\/today>/) { $today[0] = $1; $today[1] = $2; }
		elsif ($line =~ /<total>(\d+)<\/total>/) { $total = $1; }
	}
	close(XML);
}

#
# Parse intermediate log file, update XML file, and clear log
#

sub parse_log {
	if ($today[0] != $time) { $today[1] = 0; }
	open(LOG, $_[0] . $_[1] . ".log");
	flock(LOG, LOCK_SH);
	while (my $line = <LOG>) {
		chomp($line);
		my ($access_time, $user_agent, $referer, $host) = split(/\t/, $line);
		if ($user_agent) {
			$total++;

			if ($time == $access_time) { $today[1]++; }

			my @hostname = split(/\./, $host);
			if (int($hostname[$#hostname]) eq $hostname[$#hostname]) {
				$geographic{'ip'}++;
			} else {
				$geographic{lc($hostname[$#hostname])}++;
			}

			foreach my $agent (@agents_match) {
				my ($name, $regex) = split(' => ', $agent);
				if ($user_agent =~ m!$regex!) { $agents{$name}++; last; }
			}
			foreach my $platform (@os_match) {
				my ($name, $regex) = split(' => ', $platform);
				if ($user_agent =~ m!$regex!) { $platforms{$name}++; last; }
			}
			foreach my $spider (@spiders_match) {
				my ($name, $regex) = split(' => ', $spider);
				if ($user_agent =~ m!$regex!) { $spiders{$name}++; last; }
			}

			if ($referer and $referer =~ m!^(https?://)([-a-z0-9\.]{4,})((?::\d+)?)(/[^#?]+(?:#\S+)?)\?([^#?]+(?:#\S+)?)$!i) {
				if ($5) {
					my(@ref_terms, $referer) = get_terms($5, $referer);
					foreach my $term (@ref_terms) {
						$term =~ s/^[\-\+\?]|[\-\+\?]$//;
						if ($term =~ /^[A-Za-z0-9\+\-\?]{2,30}$/) {
							$terms{$term}++;
						}
					}
				}	
				$referrers{$referer}++;
			}

			unshift(@hosts, $host);
		}
	}
	flock(LOG, LOCK_UN);
	close(LOG);

	@hosts = @hosts[0..19];

	my $xml = "<?xml version=\"1.0\"?>\n";
	$xml .= "<counter>\n";
	$xml .= "\t<total>$total</total>\n";
	$xml .= "\t<today time=\"$time\">$today[1]</today>\n";
	$xml .= "\t<geographic>\n";
	foreach my $tld (keys %geographic) {
		$xml .= "\t\t<country tld=\"$tld\" hits=\"$geographic{$tld}\" />\n";
	}
	$xml .= "\t</geographic>\n";
	$xml .= "\t<agents>\n";
	foreach my $agent (keys %agents) {
		$xml .= "\t\t<agent name=\"$agent\" hits=\"$agents{$agent}\" />\n";
	}
	$xml .= "\t</agents>\n";
	$xml .= "\t<platforms>\n";
	foreach my $os (keys %platforms) {
		$xml .= "\t\t<os name=\"$os\" hits=\"$platforms{$os}\" />\n";
	}
	$xml .= "\t</platforms>\n";
	$xml .= "\t<spiders>\n";
	foreach my $spider (keys %spiders) {
		$xml .= "\t\t<spider name=\"$spider\" hits=\"$spiders{$spider}\" />\n";
	}
	$xml .= "\t</spiders>\n";
	$xml .= "\t<terms>\n";
	foreach my $term (keys %terms) {
		$xml .= "\t\t<term value=\"$term\" hits=\"$terms{$term}\" />\n";
	}
	$xml .= "\t</terms>\n";
	$xml .= "\t<referrers>\n";
	foreach my $ref (keys %referrers) {
		$xml .= "\t\t<ref url=\"$ref\" hits=\"$referrers{$ref}\" />\n";
	}
	$xml .= "\t</referrers>\n";
	$xml .= "\t<hosts>\n";
	foreach my $host (@hosts) {
		$xml .= "\t\t<host value=\"$host\" />\n";
	}
	$xml .= "\t</hosts>\n";
	$xml .= "</counter>";

	# Update XML data file
	open(XML, ">" . $_[0] . $_[1] . ".xml");
	flock(XML, LOCK_EX);
	print XML $xml;
	flock(XML, LOCK_UN);
	close(XML);

	# Clear log file
	open(LOG, ">" . $_[0] . $_[1] . ".log");
	flock(LOG, LOCK_EX);
	print LOG "";
	flock(LOG, LOCK_UN);
	close(LOG);
}

#
# Get search engine terms
#

sub get_terms {
	my $ref_temp = $_[1];
	for (split /\&/, $_[0]) {
		my($key, $val) = split /=/;
		if ($key and $key =~ /^(q|p|query)$/) {
			$val =~ tr/+/ /;
			$val =~ s/%([0-9a-fA-F]{2})/chr(hex($1))/ge;
			$ref_temp =~ s/$_[0]/$key\=$val/g;
			return (split(' ', validate_input(lc($val))), $ref_temp);
		}
	}
}

#
# Print the progress bar
#

sub mkbar {
	my ($hits, $total, $color, $type) = @_;
	my $percent = (($hits / $total) * 1000);
	$percent = (int($percent + .5 * ($percent <=> 0)) / 10);
	my $width = int(4.5 * $percent) + 1;
	if ($type == 1) {
		if ($percent == 0) { $percent = "&lt;0.1"; }
		return "<img src=\"$image_dir$color-lcap.gif\" height=\"12\" width=\"6\" /><img src=\"$image_dir$color-bar.gif\" height=\"12\" width=\"$width\" /><img src=\"$image_dir$color-rcap.gif\" height=\"12\" width=\"6\" /> $percent%";
	} else {
		return "<img src=\"$image_dir$color-lcap.gif\" height=\"12\" width=\"6\" /><img src=\"$image_dir$color-bar.gif\" height=\"12\" width=\"$width\" /><img src=\"$image_dir$color-rcap.gif\" height=\"12\" width=\"6\" /> $hits";
	}
}

#
# Get query string configuration variables (strip everything that isn't a number or letter)
#

sub getvars {
	if ($ENV{QUERY_STRING}) {
		for (split /\&/, $ENV{'QUERY_STRING'}) {
			my($key, $val) = split /=/;
			$val =~ s/%([0-9a-fA-F]{2})/chr(hex($1))/ge;
			$val =~ s/[^\w_-]//g;
			$in{$key} = $val;
		}
	}
}

#
# Remove any 'innapropriate' characters
#

sub validate_input {
	my $string = $_[0];
	$string =~ s/[^A-z0-9-_.+=\&\/\?\: ]//g;
	return $string;
}
