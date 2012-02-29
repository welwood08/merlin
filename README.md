Merlin
========

Merlin is the Copyright &copy; 2012 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.
Please read the included LICENSE.

Installation Requirements
----------------------------

Requirements: 

+ Git 
+ Python 2*
+ PostgreSQL 8*
+ psycopg2 2.2.1
+ SQLAlchemy 0.6.3

Additional Arthur requirements: 

+ Apache 2.2
+ mod_wsgi
+ Django 
+ Jinja2 2.6

Additional Graphing requirements: 

+ numpy 1.1
+ matplotlib 1.0

Additional POSIX environment (e.g. Linux) requirements:
Create and chmod 777 these directories:

+ /var/www/.matplotlib

/merlin/Arthur/graphs
Create and chmod 666 these files:

+ /merlin/dumplog.txt
+ /merlin/errorlog.txt
+ /merlin/scanlog.txt
+ /merlin/arthurlog.txt

>Note that these sort of permissions are potentially insecure and can cause a stale graphing cache. For more information, refer to README.Posix.

Installation Instructions
----------------------------

Use Git to download the code and create a branch to track your changes:

	git clone git://github.com/ellonweb/merlin.git
	cd merlin
	git checkout -b <your_branch_name>
	
After making changes to the code/config, you should store your changes:

	git add <name_of_changed_files>
	git commit -m <short_description_of_changes>
	
To update the code to the latest available source:

	git checkout master
	git pull
    git checkout <your_branch_name>
	git rebase master
	
This will re-apply your changes on top of the latest source. If you made some incompatible changes you might need to modify your change!

If you would like to contribute to merlin see [Setting up git](http://help.github.com/set-up-git-redirect)

Postgres Setup
----------------------------

All of the data your bot uses is stored in a postgresql database, see [Postgres Docs](http://www.postgresql.org/docs/)
or the relevant documentation for your OS/Distro.

For merlin your database needs to be in UTF-8 encoding          
		
	CREATE DATABASE <your_database_name> WITH ENCODING = 'UTF8';

with client encoding LATIN1
		
	ALTER DATABASE <your_database_name> SET client_encoding='LATIN1';
    
Preparing merlin
----------------------------

Inspect and modify merlin.cfg in an editor as required. You should only need to change the Connection, Admin, Alliance, Channel and DB settings. If you're using the SMS features you'll need to add your details in the clickatell and googlevoice section and check the sms setting in Misc.

>Note Graphing can be completely disabled in the config, look for - graphing  : and append "cached", "enabled", or "disabled" depending on which you want!
       
Run createdb.py. This will create all the neccessary tables for you, as well as configuring the bot to join your alliance's main channel and downloading the shipstats from PA. Linux users, there is no shebang line so you will need to run: 
		
	python createdb.py

Inspect and modify /Hooks/\_\_init\_\_.py as needed. This controls which groups of commands will be enabled. The SMS package is disabled by default, if you have a clickatell account to use you will want to remove the # character. Many alliances will want to disable the prop/cookie package, use a # character at the beginning of the line.
       
You may also want to change the access levels for some of the commands, you should do that now. 
   
Merlin Access Settings
----------------------------

All of Merlin's functionality is stored in /Hooks/

Merlin's system hooks use the list of admins defined in merlin.cfg to control access. System hooks can be identified by the system modifier:@system(..)

Merlin's non-system hooks (the majority of the functionality) are split into different routes and utilise a two-level access system. The access requirement of a route is provided in the modifier: @route(.. access = "member")

The hook can also be given a default access level for all of its routes by defining the access variable at class level.
This parameter can be changed to any of the access levels defined in merlin.cfg, or instead of passing a string you can provide an actual number, though this is not recommended!

If a command is executed in a channel Merlin first checks the channel's min and max levels. If the channel's max level is higher than the command's requirement the command is denied. If the user's access level or the channel's min level match or exceed the requirement the command is executed.

If you want to limit a command to use in a specific channel or in PM, you can use this modifier on the execute method of the hook  @channel("home")

This can be changed to any channels defined in merlin.cfg or simply "PM",or you can specify the specific channel.

Running Merlin
----------------------------

Run merlin.py. Again, there is no shebang line.

	python merlin.py
		
Now add yourself to the bot using !adduser:
        
	!adduser <your_pnick> admin

You may also want to !secure the bot. You should do this each round and then 

	!reboot

Any time you make changes to any of Merlin's code, you will need to use 
		
	!reload 

Configuring Excalibur
----------------------------

You need to use a task scheduler to run excalibur.py one minute after every tick. If you're using crontab, you might use a command like this

	1 * * * * /path/to/merlin/excalibur.sh >> /path/to/merlin/dumplog.txt 2>&1

You'd then also need to create the excalibur.sh file with executable permission and insert the following commands
            
	cd /path/to/merlin/
           python excalibur.py

Make sure to sudo your crontab

Configuring Apache and running Arthur
----------------------------

At the bottom of your httpd.conf, add the following lines
            
	WSGIScriptAlias / /path/to/merlin/arthur.wsgi
    <Directory /path/to/merlin/>
        <Files arthur.wsgi>
            Order allow,deny
            Allow from all
        </Files>
    </Directory>
    
    Alias /static/ /path/to/merlin/Arthur/static/
    <Directory /path/to/merlin/Arthur/static/>
        Order allow,deny
        Allow from all
    </Directory>
    
    Alias /graphs/ F:/Code/Git/merlin/Arthur/graphs/
    <Directory F:/Code/Git/merlin/Arthur/graphs/>
        Order allow,deny
        Allow from all
        ErrorDocument 404 /draw
    </Directory>
       
Make sure you edit all the paths!

Open the arthur.wsgi file and edit the two paths in that file.

Arthur Access Settings
----------------------------
    
All of Arthur's functionality is stored in /Arthur/

Arthur's hooks use a similar but simpler access model to Merlin. The hooks all have an access level defined at the class level, similar to Merlin's default route access.

This parameter can be changed to any of the access levels defined in merlin.cfg, or instead of passing a string you can provide an actual number, though this is not recommended!

These access levels not only control the access but also the items in the dynamic menu.

Anyone with an active user account is able to login to the website. This means galmates as well as members, though obviously there is very little for galmates to see! You have the option of making tools open for public use or the opposite, restricting what your members can see.



Updating for a new round
----------------------------

You should disable your task scheduler from running Excalibur when the round is over, it is not guaranteed to function correctly during havoc.
Make sure you have the latest source code! (see #4)
Run createdb.py with the --migrate switch and the old round number. For example, just before the start of round 37:
            
	python createdb.py --migrate 36
       
This will store the old database in an alternate schema for archiving, and copy your user list (among other things) to a new schema.
The migration tool will automatically pull the ship stats from PA. If the stats change before tick start or if you want to load beta stats, you can run shipstats.py manually:
            
	python shipstats.py [optional_url_to_stats]

Avoid running this midround, it will delete stored unit/au scans.
Don't forget to enable your task scheduler again once ticks start!

