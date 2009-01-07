# Merlin Core

# This file is part of Merlin.
 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

import os
from time import asctime
from traceback import format_exc
from variables import *
from Core.connection import Connection as conn
from Core.actions import Action as parse
from Core.exceptions_ import RebootConnection
import Core.callbacks as cb
import Core.modules

# Check the errorlog file exists, if not create it
try:
	open("errorlog.txt", "r")
except IOError:
	open("errorlog.txt", "w").close()

class Bot(object):
	# Main bot container
	
	def __init__(self):
		# Initialize the bot
	
		self.server = server
		self.port = port
		self.details = {"nick":nick, "pass":passw}
		
		self.conn = conn(self.server, self.port)
		self.conn.connect()
		
		self.run()
	
	def run(self):
		# Run the bot
		
		self.conn.write("NICK %s" % self.details["nick"])
		self.conn.write("USER %s 0 * : %s" % (self.details["nick"], self.details["nick"]))
		
		# Initialise the bot with the modules that are supposed to be loaded at startup
		for line in open(os.path.join("Hooks/mods.txt")):
			mod = line.split("#")[0]
			if mod:
				cb.reload_mod(mod.strip())
			
		# The beast begins
		while True:
			# Read the next line
			line = self.conn.read()
			if not line:
				return
			
			# Parse and process the line
			parsed_line = parse(line, self.conn, self.details["nick"], cb)
			try:
				cb.callback(parsed_line)
				self.details["nick"] = parsed_line.botnick
			except SystemExit:
				raise
			except KeyboardInterrupt:
				raise
			except RebootConnection:
				raise
			except:
				open("errorlog.txt", "a").write(asctime()+" Error:\n%s" % format_exc())
				open("errorlog.txt", "a").write("\nArguments that caused error: %s" % parsed_line)
				print "ERROR RIGHT HERE!!"
				print format_exc()
				parsed_line.alert("An exception occured and has been logged.")

if __name__ == "__main__":
	Bot() # Start the bot here, if we're the main module.