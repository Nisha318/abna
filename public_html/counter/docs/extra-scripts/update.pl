#!/usr/bin/perl

# BS Counter v2.0.0
# Utility to convert the old style data files to the new xml style

@countries = ('US Commercial','US Organization','Network','US Government','US Military','US Educational','International','Afghanistan','Albania','Algeria','American Somoa','Andorra','Angola','Anguilla','Antarctica','Antigua and Barbuda','Argentina','Armenia','Aruba','Australia','Austria','Azerbaijan','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bermuda','Bhutan','Bolivia','Bosnia and Herzegovina','Botswana','Bouvet Island','Brazil','British Indian Ocean Territory','Brunei','Bulgaria','Burkina Faso','Burundi','Cambodia','Cameroon','Canada','Cape Verde','Central African Republic','Chad','Channel Islands - Guernsey','Channel Islands - Jersey','Chile','China','Christmas Island','Cocos (Keeling) Islands','Colombia','Comoros','Congo','Cook Islands','Costa Rica','Coted Ivoire','Croatia','Cuba','Cyprus','Czech Republic','Denmark','Djibouti','Dominica','Dominican Republic','East Timor','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Ethiopia','Falklands Islands','Faroe Islands','Fiji','Finland','France','French Guiana','French Polynesia','French Southern Territories','French Metropolitan','Gabon','Georgia','Germany','Ghana','Gibraltar','Greece','Greenland','Grenada','Guadeloupe','Guam','Guatemala','Guinea','Guyana','Haiti','Heardand McDonald Islands','Honduras','HongKong','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Kiribati','Peoples Republic of Democratic Korea','Republic of Korea','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libyan Arab Jamahiriya','Liechtenstein','Lithuania','Luxembourg','Macao','Macedonia','Malawi','Malaysia','Mali','Malta','Marshall Islands','Martinique','Mauritania','Mauritius','Mayotte','Mexico','Micronesia','Moldova','Monaco','Mongolia','Montserrat','Morocco','Mozambique','Myanmar','Namibia','Nauru','Nepal','Netherlands','Netherlands Antilles','New Caledonia','New Zealand','Nicaragua','Niger','Nigeria','Niue','Norfolk Island','Northern Mariana Islands','Norway','Oman','Pakistan','Palau','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Pitcairn','Poland','Portugal','Puerto Rico','Qatar','Reunion','Romania','Russia','Rwanda','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tomeand Principe','Saudi Arabia','Senegal','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','South Africa','South Georgia and the South Sandwich Islands','Spain','Sri Lanka','St. Helena','St. Pierreand Miquelon','Sudan','Suriname','Svalbardand Jan Mayen Islands','Swaziland','Sweden','Switzerland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','The Bahamas','The Cayman Islands','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Turks and Caicos Islands','Tuvalu','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States','United States Minor Outlying Islands','Urugauy','Uzbekistan','Vanuatu','Vatican City State','Venezuela','Vietnam','Virgin Islands (British)','Virgin Islands (US)','Wallis and Futuna Islands','Western Sahara','Yemen','Yugoslavia','Zaire','Zambia','Zimbabwe','Unknown Location');
@domainext = ('com','org','net','gov','mil','edu','int','af','al','dz','as','ad','ao','ai','aq','ag','ar','am','aw','au','at','az','bh','bd','bb','by','be','bz','bj','bm','bt','bo','ba','bw','bv','br','io','bn','bg','bf','bi','kh','cm','ca','cv','cf','td','gg','je','cl','cn','cx','cc','co','km','cg','ck','cr','ci','hr','cu','cy','cz','dk','dj','dm','do','tp','ec','eg','sv','gq','er','ee','et','fk','fo','fj','fi','fr','gf','pf','tf','fx','ga','ge','de','gh','gi','gr','gl','gd','gp','gu','gt','gn','gy','ht','hm','hn','hk','hu','is','in','id','ir','iq','ie','il','it','jm','jp','jo','kz','ke','ki','kp','kr','kw','kg','la','lv','lb','ls','lr','ly','li','lt','lu','mo','mk','mw','my','ml','mt','mh','mq','mr','mu','yt','mx','fm','md','mc','mn','ms','ma','mz','mm','na','nr','np','nl','an','nc','nz','ni','ne','ng','nu','nf','mp','no','om','pk','pw','pa','pq','py','pe','ph','pn','pl','pt','pr','qa','re','ro','ru','rw','kn','lc','vc','ws','sm','st','sa','sn','sc','sl','sg','sk','si','sb','so','za','gs','es','lk','sh','pm','sd','sr','sj','sz','se','ch','sy','tw','tj','tz','th','bs','ky','to','tt','tn','tr','tm','tc','tv','ug','ua','ae','uk','us','um','uy','uz','vu','va','ve','vn','vg','vi','wf','eh','ye','yu','zr','zm','zw','other');

if (!$ARGV[0]) { print "Usage: $0 [data file(s)]\n"; }

foreach $file (@ARGV)
{
	open (DATA, $file);
	$data = <DATA>;
	close(DATA);

	($hits,$htoday,$location,$v1,$v2,$v3,$v4,$v5,$v6,$v7,$v8,$v9,$v10,$v11,$v12,$v13,$v14,$v15,$v16,$v17,$v18,$v19,$v20,$r1,$r2,$r3,$r4,$r5,$r6,$r7,$r8,$r9,$r10,$r11,$r12,$r13,$r14,$r15,$r16,$r17,$r18,$r19,$r20,$browsers,$platforms) = split(/&&/, $data);
	($today, $hitstoday) = split(/=/, $htoday);

	($CEXT{'com'},$CEXT{'org'},$CEXT{'net'},$CEXT{'gov'},$CEXT{'mil'},$CEXT{'edu'},$CEXT{'int'},$CEXT{'af'},$CEXT{'al'},$CEXT{'dz'},$CEXT{'as'},$CEXT{'ad'},$CEXT{'ao'},$CEXT{'ai'},$CEXT{'aq'},$CEXT{'ag'},$CEXT{'ar'},$CEXT{'am'},$CEXT{'aw'},$CEXT{'au'},$CEXT{'at'},$CEXT{'az'},$CEXT{'bh'},$CEXT{'bd'},$CEXT{'bb'},$CEXT{'by'},$CEXT{'be'},$CEXT{'bz'},$CEXT{'bj'},$CEXT{'bm'},$CEXT{'bt'},$CEXT{'bo'},$CEXT{'ba'},$CEXT{'bw'},$CEXT{'bv'},$CEXT{'br'},$CEXT{'io'},$CEXT{'bn'},$CEXT{'bg'},$CEXT{'bf'},$CEXT{'bi'},$CEXT{'kh'},$CEXT{'cm'},$CEXT{'ca'},$CEXT{'cv'},$CEXT{'cf'},$CEXT{'td'},$CEXT{'gg'},$CEXT{'je'},$CEXT{'cl'},$CEXT{'cn'},$CEXT{'cx'},$CEXT{'cc'},$CEXT{'co'},$CEXT{'km'},$CEXT{'cg'},$CEXT{'ck'},$CEXT{'cr'},$CEXT{'ci'},$CEXT{'hr'},$CEXT{'cu'},$CEXT{'cy'},$CEXT{'cz'},$CEXT{'dk'},$CEXT{'dj'},$CEXT{'dm'},$CEXT{'do'},$CEXT{'tp'},$CEXT{'ec'},$CEXT{'eg'},$CEXT{'sv'},$CEXT{'gq'},$CEXT{'er'},$CEXT{'ee'},$CEXT{'et'},$CEXT{'fk'},$CEXT{'fo'},$CEXT{'fj'},$CEXT{'fi'},$CEXT{'fr'},$CEXT{'gf'},$CEXT{'pf'},$CEXT{'tf'},$CEXT{'fx'},$CEXT{'ga'},$CEXT{'ge'},$CEXT{'de'},$CEXT{'gh'},$CEXT{'gi'},$CEXT{'gr'},$CEXT{'gl'},$CEXT{'gd'},$CEXT{'gp'},$CEXT{'gu'},$CEXT{'gt'},$CEXT{'gn'},$CEXT{'gy'},$CEXT{'ht'},$CEXT{'hm'},$CEXT{'hn'},$CEXT{'hk'},$CEXT{'hu'},$CEXT{'is'},$CEXT{'in'},$CEXT{'id'},$CEXT{'ir'},$CEXT{'iq'},$CEXT{'ie'},$CEXT{'il'},$CEXT{'it'},$CEXT{'jm'},$CEXT{'jp'},$CEXT{'jo'},$CEXT{'kz'},$CEXT{'ke'},$CEXT{'ki'},$CEXT{'kp'},$CEXT{'kr'},$CEXT{'kw'},$CEXT{'kg'},$CEXT{'la'},$CEXT{'lv'},$CEXT{'lb'},$CEXT{'ls'},$CEXT{'lr'},$CEXT{'ly'},$CEXT{'li'},$CEXT{'lt'},$CEXT{'lu'},$CEXT{'mo'},$CEXT{'mk'},$CEXT{'mw'},$CEXT{'my'},$CEXT{'ml'},$CEXT{'mt'},$CEXT{'mh'},$CEXT{'mq'},$CEXT{'mr'},$CEXT{'mu'},$CEXT{'yt'},$CEXT{'mx'},$CEXT{'fm'},$CEXT{'md'},$CEXT{'mc'},$CEXT{'mn'},$CEXT{'ms'},$CEXT{'ma'},$CEXT{'mz'},$CEXT{'mm'},$CEXT{'na'},$CEXT{'nr'},$CEXT{'np'},$CEXT{'nl'},$CEXT{'an'},$CEXT{'nc'},$CEXT{'nz'},$CEXT{'ni'},$CEXT{'ne'},$CEXT{'ng'},$CEXT{'nu'},$CEXT{'nf'},$CEXT{'mp'},$CEXT{'no'},$CEXT{'om'},$CEXT{'pk'},$CEXT{'pw'},$CEXT{'pa'},$CEXT{'pq'},$CEXT{'py'},$CEXT{'pe'},$CEXT{'ph'},$CEXT{'pn'},$CEXT{'pl'},$CEXT{'pt'},$CEXT{'pr'},$CEXT{'qa'},$CEXT{'re'},$CEXT{'ro'},$CEXT{'ru'},$CEXT{'rw'},$CEXT{'kn'},$CEXT{'lc'},$CEXT{'vc'},$CEXT{'ws'},$CEXT{'sm'},$CEXT{'st'},$CEXT{'sa'},$CEXT{'sn'},$CEXT{'sc'},$CEXT{'sl'},$CEXT{'sg'},$CEXT{'sk'},$CEXT{'si'},$CEXT{'sb'},$CEXT{'so'},$CEXT{'za'},$CEXT{'gs'},$CEXT{'es'},$CEXT{'lk'},$CEXT{'sh'},$CEXT{'pm'},$CEXT{'sd'},$CEXT{'sr'},$CEXT{'sj'},$CEXT{'sz'},$CEXT{'se'},$CEXT{'ch'},$CEXT{'sy'},$CEXT{'tw'},$CEXT{'tj'},$CEXT{'tz'},$CEXT{'th'},$CEXT{'bs'},$CEXT{'ky'},$CEXT{'to'},$CEXT{'tt'},$CEXT{'tn'},$CEXT{'tr'},$CEXT{'tm'},$CEXT{'tc'},$CEXT{'tv'},$CEXT{'ug'},$CEXT{'ua'},$CEXT{'ae'},$CEXT{'uk'},$CEXT{'us'},$CEXT{'um'},$CEXT{'uy'},$CEXT{'uz'},$CEXT{'vu'},$CEXT{'va'},$CEXT{'ve'},$CEXT{'vn'},$CEXT{'vg'},$CEXT{'vi'},$CEXT{'wf'},$CEXT{'eh'},$CEXT{'ye'},$CEXT{'yu'},$CEXT{'zr'},$CEXT{'zm'},$CEXT{'zw'},$CEXT{'other'}) = split(/\|/, $location);
	@browsers = split(/\|/, $browsers); @browsers = sort(@browsers);
	@platforms = split(/\|/, $platforms); @platforms = sort(@platforms);

	open(XML, ">$file.xml");
	print XML "<?xml version=\"1.0\"?>\n";
	print XML "<counter>\n";
	print XML "\t<total>$hits</total>\n";
	print XML "\t<today time=\"\" host=\"\">$hitstoday</today>\n";
	print XML "\t<geographic>\n";
	foreach $key (keys %CEXT) {
		if ($CEXT{$key} > 0) {
			$hits = $CEXT{$key};
			if ($key eq "other") { $key = "ip"; }
			print XML "\t\t<country tld=\"$key\" hits=\"$hits\" />\n";
		}
	}
	print XML "\t</geographic>\n";
	print XML "\t<browsers>\n";
	foreach $browser (@browsers) {
		chomp $browser;
		($agent, $hits) = split(/=/, $browser);
		if ($hits > 0) {
			if ($agent =~ /AOL/i) { $brow{'AOL'} += $hits; }
			elsif ($agent =~ /MSIE/i) { $brow{'Internet Explorer'} += $hits; }
			elsif ($agent =~ /Opera/i) { $brow{'Opera'} += $hits; }
			elsif ($agent =~ /Spider/i) { $brow{'Bot'} += $hits; }
			elsif ($agent =~ /Netscape/i) { $brow{'Netscape'} += $hits; }
			elsif ($agent =~ /Lynx/i) { $brow{'Lynx'} += $hits; }
			elsif ($agent =~ /Mosaic/i) { $brow{'Mosaic'} += $hits; }
			elsif ($agent =~ /Unknown/i) { $brow{'Unknown'} += $hits; }
		}
	}
	foreach $key (keys %brow) {
			print XML "\t\t<agent name=\"$key\" hits=\"$brow{$key}\" />\n";
	}
	print XML "\t</browsers>\n";
	print XML "\t<platforms>\n";
	foreach $platform (@platforms) {
		chomp $platform;
		($agent, $hits) = split(/=/, $platform);
		if ($hits > 0) {
			if ($agent =~ /Windows NT/i) { $os{'Windows NT/2000/XP'} += $hits; }
			elsif ($agent =~ /Windows 98|Windows 95/i) { $os{'Windows 9x/ME'} += $hits; }
			elsif ($agent =~ /WebTV/i) { $os{'WebTV'} += $hits; }
			elsif ($agent =~ /Unknown/i) { $os{'Unknown'} += $hits; }
			elsif ($agent =~ /IRIX/i) { $os{'IRIX'} += $hits; }
			elsif ($agent =~ /SUNOS/i) { $os{'SunOS'} += $hits; }
			elsif ($agent =~ /Unix/i) { $os{'UNIX'} += $hits; }
			elsif ($agent =~ /Spider/i) { $os{'Bot'} += $hits; }
			elsif ($agent =~ /OS/i) { $os{'OS/2'} += $hits; }
			elsif ($agent =~ /Mac/i) { $os{'Mac PowerPC'} += $hits; }
			elsif ($agent =~ /Linux/i) { $os{'Linux'} += $hits; }
		}
	}
	foreach $key (keys %os) {
			print XML "\t\t<os name=\"$key\" hits=\"$os{$key}\" />\n";
	}
	print XML "\t</platforms>\n";
	print XML "\t<referrers>\n";
	print XML "\t</referrers>\n";
	print XML "</counter>\n";
	close(XML);

	system("chmod 666 $file.xml");
}
