# RoBoCoP

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

import os, socket, SocketServer, threading
from .variables import admins, robocop as addr
from .Core.exceptions_ import PNickParseError

def run():
	try:
		os.remove(addr)
	except OSError:
		pass
	message = threading.currentThread().message
	server = SocketServer.UnixStreamServer((addr), handler)
	message.alert("RoBoCoP is now running.")
	while not threading.currentThread().killcop:
		server.handle_request()
	try:
		os.remove(addr)
	except OSError:
		pass
	message = threading.currentThread().message
	message.alert("RoBoCoP has been killed.")

class handler(SocketServer.StreamRequestHandler):
	def handle(self):
		message = threading.currentThread().message
		s = self.request
		f = s.makefile('rb')
		while 1:
			l = f.readline()
			if not l: break
			message._msg = l
			message.callbackmod.robocop(message)

def robocop(message):
	"Start the RoBoCoP server"
	if message.get_msg() == "!robocop":
		try:
			if message.get_pnick() in admins:
				startcop(message)
			else:
				message.alert("You don't have access for that.")
		except PNickParseError:
			message.alert("You don't have access for that.")

def startcop(message):
	if message.get_msg() in ("is now your hidden host", "!robocop"):
		for thread in threading.enumerate():
			if thread.getName() == "RoBoCoP":
				message.alert("RoBoCoP is already running.")
				return
		thread = threading.Thread(name="RoBoCoP", target=run)
		thread.setDaemon(1)
		thread.message = message
		thread.killcop = False
		thread.start()

def killcop(message):
	"Stop the RoBoCoP server"
	if message.get_msg() == "!killcop":
		try:
			if message.get_pnick() in admins:
				for thread in threading.enumerate():
					if thread.getName() == "RoBoCoP":
						thread.message = message
						thread.killcop = True
						copkiller = socket.socket(socket.AF_UNIX)
						try:
							copkiller.connect((addr))
							copkiller.close()
						except socket.error:
							pass
						return
				message.alert("RoBoCoP is already dead.")
			else:
				message.alert("You don't have access for that.")
		except PNickParseError:
			message.alert("You don't have access for that.")

callbacks = [("396", startcop), ("PRIVMSG", robocop), ("PRIVMSG", killcop)]