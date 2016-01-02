BS Counter 2.5.2 (Copyright 1999-2005 Brian Stanback)

Please send feature requests, optimizations/improvements, or bug reports via the 
contact form at http://www.stanback.net/contact

####################################################################################

General Information:

You will notice that there is a PHP and Perl version of the counter; both 
versions can read/write to the same data files and they both generate the same 
statistics.

The PHP version is slightly easier to setup but the Perl version will still be
maintained for anyone who wants to use it.

There are two types of counter:

	count.xxx	- Counter which will generate the number of hits either as
			  a text string or a series of images, uses Server Side 
          	     	  Includes (SSI).

	gd-count.xxx	- Counter which will generate the number of hits by creating 
			  a png image (requries the GD library).

####################################################################################

Basic Instillation:

1) You may need to configure the variables in the setup.xxx, stats.xxx and the 
   count.xxx or gd-count.xxx. To edit the files, open them up in a bsic text 
   editor such as notepad. The variables will be near the top of the file and 
   descriptions for what each variable does are commented inine. In many cases the 
   configuration variables can be left alone.

2) Upload the bscounter-cgi and bscounter-images folders to an appropriate 
   location on your web server. Some web server configurations require the 
   bscounter-cgi directory to be inside a cgi-bin directory.

3) Change the permissions for the bscounter-cgi/data directory so that all 
   groups have write permissions. Most popular FTP clients have an option for
   doing this. You may also do it from an SSH/Telnet session by typing the 
   command "chmod 777 data" from the bscounter-cgi directory.

4) (Perl Only) You will need to make the .cgi files in the bscounter-cgi/perl 
   directory executable. Again, this may be done from an FTP client or from a 
   SSH/Telnet session using the command "chmod 755 *.cgi" from the perl directory.

####################################################################################

Using the counter:

Go to:	http://www.yourdomain.com/bscounter-cgi/php/setup.php  (PHP Version)
	http://www.yourdomain.com/bscounter-cgi/perl/setup.cgi (Perl Version)

This will automatically generate the html code you need to insert into 
your html documents to display the counter.

####################################################################################

Frequently Asked Questions:

Q: How do I manually change the number of hits?
A: Once you have included the counter on your page, a file named
   pagename.xml will be created in the data directory. Simply edit 
   this file with a text editor and change the number located inside 
   the <total> and </total>
   
Q: The counter showing up on my page or i am getting an error?
A: If you are using the SSI version, many hosting providers will 
   requre you to rename the page from name.html or name.htm to
   name.shtml. If you are getting an error, check the virtual path 
   on the <!--#exec vitual= bit.

Q: Why isn't the script working with Microsoft Windows?
A: Unfortunately I don't have a Microsoft server environment to test 
   with. Please be sure you are using double-backslashes, eg. \\ instead of 
   forward slashes. If it is still not working, please contact me.

Q: Why aren't the referrer stats or search terms showing up?
A: Unfortunately, referer stats and search terms will not work correctly if you are 
   using the GD version of the counter. If the PHP GD counter is being loaded from a 
   PHP document you can enable it by adding the following to the end of the image url:
   &referer=<?php echo $_SERVER['HTTP_REFERER']; ?>
   
Q: Why am I getting a broken image with the GD version of the counter?
A: Make sure your domain/domains are listed in the $allowed/@allowed configuration 
   variable near the top of the gd-count.xxx script.