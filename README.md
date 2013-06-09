Merlin
========
Merlin is the Copyright &copy; 2012 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.  
This version was modified and added to by Martin Stone 2012-2013.  
Please read the included LICENSE.

Here Be Dragons
----------------------------
This version of merlin breaks database and config compatibility with ellonweb's original branch, and pretty much anything not forked from here. Additionally, it breaks compatibility with itself occasionally (well, actually quite frequently...).

For support, use github or (preferably) try #munin on netgamers IRC.

Installation Requirements
----------------------------
Requirements (tested on):

+ Git 
+ Python 2.7.*
+ PostgreSQL 9.1
+ psycopg2 2.4.5
+ SQLAlchemy 0.7.8

Additional Arthur requirements: 

+ Apache 2.2 + mod_wsgi (also tested with nginx)
+ Django 1.4+
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

	git clone git://github.com/d7415/merlin.git
	cd merlin
	git checkout -b <your_branch_name>
	
After making changes to the code/config, you should store your changes:

	git add <name_of_changed_files>
	git commit -m <short_description_of_changes>
	
To update the code to the latest available source:

	git checkout master
	git pull
	git rebase master <your_branch_name>
	
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
Inspect and modify merlin.cfg in an editor as required.

>Note Graphing can be completely disabled in the config, look for - graphing  : and append "cached", "enabled", or "disabled" depending on which you want!
       
Run createdb.py. This will create all the neccessary tables for you, as well as configuring the bot to join your alliance's main channel and downloading the shipstats from PA. Linux users, there is no shebang line so you will need to run: 
		
	python createdb.py

Inspect and modify /Hooks/\_\_init\_\_.py as needed. This controls which groups of commands will be enabled. Add a # character to the beginning of a line to disable a module. Many alliances will want to disable the prop/cookie package.
       
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
You need to use a task scheduler to run excalibur.py one minute after every tick. If you're using crontab, you might use a command like this, which uses the supplied excalibur.sh

	1 * * * * /path/to/merlin/excalibur.sh >> /path/to/merlin/dumplog.txt 2>&1

excalibur.sh will need updating with the path to your bot, and if you want to use MySQL. The relevant excalibur.*.py will need updating if you want to use the same excalibur for more than one bot.

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

Open the arthur.wsgi file and edit the two paths in that file. Open Arthur/__init__.py and edit the path in that file.

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

See Also
----------------------------
Other useful sources:

+ Installation walkthrough: walkthrough.md
+ Command list: commandlist.md
+ Posix tips: README.Posix
+ Branch explanation on the wiki: <https://github.com/d7415/merlin/wiki/Branches>

Extra Features and Requirements
----------------------------
Some features require extra configuration. Details below.

### IMAP Support
IMAP support allows the bot to parse notification emails from Planetarion. The bot can then announce incoming or recalled fleets, request scans for incoming fleets and forward the messages to the user's email address.

To use this feature, the alliance will need a domain or subdomain to receive the emails. Users must then set their notification email address in-game to pnick-def@alliance.com. ("-def" is the default suffix for notification emails, which is configurable. If this is set, pnick@alliance.com will still forward emails but not trigger defcalls)

To listen for new emails:

    python IMAPPush.py

If this proves unstable, these crontab lines will kill and restart the process every hour

    39 *    * * *   root    kill `ps aux | grep IMAPPush.py | grep -v grep | sed -r 's/merlin[ tab]+([0-9]+).*/\1/g'`
    40 *    * * *   merlin  /merlin/imappush.sh
Where the bot is run as user "merlin" and stored in /merlin/. imappush.sh should contain

    #!/bin/bash
    cd /merlin/
    python IMAPPush.py >> IMAPLog.txt


### Importing "Last 1000 scans"
Planetarion allows alliance members to "List scan ids of last 1000 scans". If this is saved to a file called "1000scans.txt", 1000scans.py will parse them into the bot using user ID #1. By default this loads at one scan every 2 seconds to minimise server RAM usage (~40mb in testing). If your server has lots of RAM, the time.sleep() can be changed to a lower number or removed entirely..


### WhatsApp Support
WhatsApp support allows the use of WhatsApp with the !sms command.  
It requires the yowsup library, by Tarek Galal.
The git repository will already point to the latest known-good version of the library. To install:  

    git submodule init
    git submodule update

The second of these can also be used to update to a newer version when the upstream repository (this one) updates. If you encounter a fatal "reference is not a tree" error, try

    git submodule sync
    git submodule update

##### Config Items
"login" is your full, international phone number, including the country code but without the leading + or 00.  
For accounts set up from a phone, "password" is the IMEI reversed and MD5 hashed (for android) or the MAC address, uppercase, repeated twice and MD5 hashed. This can be achieved using

    python yowsup/src/yowsup-cli --generatepassword your-IMEI-or-MAC-address-here

For accounts set up using yowsup, "password" is the password given by yowsup, base64 decoded. In python:

    "your password".decode("base64")

### FluxBB Integration
Merlin can integrate with FluxBB, creating user accounts and updating passwords when the arthur password is updated in !pref.

Notes:

+ FluxBB must be set up to use the same database as merlin, and the merlin user must have SELECT, UPDATE and INSERT privileges to the FluxBB users table.
+ To avoid conflicts, FluxBB should be set up using the table prefix option. This can then be set in merlin.cfg.
+ Passwords updated from within FluxBB will not be updated on arthur.

### Multiple Bots on One Database
This version of merlin allows multiple bots to share a single ticker, saving bandwidth, disk space and processing power.

Notes:

+ Each bot must have its own prefix set in merlin.cfg
+ The ticker (excalibur.pg.py) called by cron should refer to *all* merlin.cfg paths.
+ Only one ticker should be used. If more than one are called, only the first will work each tick.
+ When migrating data for a new round, do *not* use the "temp" option. This will erase settings for all but the current bot.
+ When migrating data for a new round, migrate the first bot normally. For each other bot, use the "--noschema" option, i.e. `python createdb.py --migrate 36 --noschema`

### Botfile saving
To save the PA botfiles every tick, change `savedumps` to `True` in excalibur.pg.py and make sure that the merlin folder itself, or a subdirectory called "dumps", is writable by the account running excalibur.

To share the dumps with others, add a section to your Apache or nginx config, e.g.

##### Apache

    Alias /dumps/ /path/to/merlin/dumps/
    <Directory /path/to/merlin/dumps/>
        Options +Indexes
        Order allow,deny
        Allow from all
    </Directory>
    
##### nginx

    location /dumps/ {
        alias /path/to/merlin/dumps/
        autoindex on;
    }

Note: If you are using one excalibur for multiple bots, the dump files will only be saved for the "main" bot. To share these, use the "main" merlin path in all dump-related Apache/nginx config.
