# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

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
 
# Module by Martin Stone

from Core.config import Config
from Core.db import session
from Core.maps import Planet, User, Request
from Core.loadable import loadable, route, robohci
from Core.string import errorlog
import socket
from smtplib import SMTP, SMTPException, SMTPSenderRefused, SMTPRecipientsRefused
from ssl import SSLError
from Core.exceptions_ import SMSError
from Core.robocop import push

class defcall(loadable):
    """Make a broadcast to the channel requesting defence"""
    usage = " <x:y:z> <eta> <description>"
    access = 3 # Member (was DC)
    
    @route(loadable.planet_coord + r"\W+(\d+)\W+(.+)", access="defcall")
    def execute(self, message, user, params):
        
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.reply("No planet with coords %s:%s:%s found" % params.group(1,3,5))
            return
        
        notice = "DEFCALL: %s wants %s to %s:%s:%s eta %s" % (user.name, params.group(7), params.group(1), params.group(3), 
                                                              params.group(5), params.group(6))
        if Config.getboolean("Misc", "globaldef"):
            push("broadcast", notice="!#!"+notice.replace(" ","!#!"))
        else:
            message.notice(notice, Config.get("Channels", "home"))
    
    @robohci
    def robocop(self, message, etype, uname="Unknown", tick=0, x=0, y=0, z=0, name="", eta=0, size=0, res=0, cons=0):
        notice = ""
        email = ""

        user = User.load(uname)
        if user is None:
            errorlog("Defcall: Invalid user in email. Idiot.")
            uname = "%s (whoever that is??)" % (uname)
            ucoords = "x:x:x"
            addr = Config.get("imap", "bounce")
            email = "Bad username in notifications: %s\n\nOriginal notification:\n\n\n" % (uname)
        else:
            uname = "%s%s" % (user.name, ("(%s)" % (user.alias)) if user.alias else "")
            if user.planet:
                ucoords = "%d:%d:%d" % (user.planet.x, user.planet.y, user.planet.z)
            else:
                ucoords = "idiot"
            addr = user.email

        if etype != "fin":
            p = Planet.load(x,y,z)
            if p is None:
                errorlog("Defcall: Invalid planet in email. Probably an exile.")

        if etype == "new":
            # Message to DC channel / main channel. Request scans.
            if p is None:
                arace = "??"
                aally = "Unknown"
            else:
                arace = p.race
                i = p.intel
                if i and i.alliance:
                    aally = i.alliance.name
                else:
                    aally = "Unknown"
            
            notice = "DEFCALL: %s (%s) has incoming eta %s(%s) from %s:%s:%s (%s, %s) - Fleet: %s Visible Ships: %s" % (uname, ucoords, eta, int(eta)-int(tick),
                                                                                                                        x, y, z, arace, aally, name, size)
            email += "Notification from Planetarion in tick %s\n\n" % (tick) +\
                     "Incoming Fleet %s from %s:%s:%s with %s visible ships expected to land in tick %s." % (name, x, y, z, size, eta) +\
                    "\n\nThis has been reported to the %s DCs." % (Config.get("Alliance", "name"))
        elif etype == "rec":
            # Message to DC channel *and* main channel
            notice = "RECALL: %s (%s) has had a recall: Fleet: %s from %s:%s:%s" % (uname, ucoords, name, x, y, z)
            email += "Notification from Planetarion in tick %s\n\n" % (tick) +\
                     "Incoming Fleet %s from %s:%s:%s has recalled." % (name, x, y, z) +\
                    "\n\nThis has been reported to %s." % (Config.get("Alliance", "name"))
        elif etype == "fin":
            # Nothing to see here. Move along.
            notice = ""
            what = ""
            if int(res):
                what = "research"
                if int(cons):
                    what += " and construction"
            else:
                what = "construction"
            email += "Notification from Planetarion in tick %s\n\nAll %s has finished and none is queued." % (tick, what)
        else:
            return
        # Send email - pref?
        if notice:
            if Config.getboolean("Misc", "globaldef"):
                   push("broadcast", notice="!#!"+notice.replace(" ","!#!"))
            else:
                if etype == "new" and Config.has_option("Channels", "def"):
                    message.notice(notice, Config.get("Channels", "def"))
                else:
                    message.notice(notice, Config.get("Channels", "home"))
        
        if email and addr:
            self.send_email("Relayed PA Notifications from tick %s" % (tick), email, addr)
        
        # Check for scans
	if etype == "new" and p and user:
           scantypes = Config.get("Misc", "autoscans")
           scanage = Config.getint("Misc", "scanage")

           for stype in scantypes:
               scan = p.scan(stype)
               if scan and (int(tick) - scan.tick <= scanage):
                   return
               else:
                   req = Request(target=p, scantype=stype, dists=0)
                   user.requests.append(req)
                   session.commit()
                   push("request", request_id=req.id, mode="request")

    def send_email(self, subject, message, addr):
        try:
            if (Config.get("smtp", "port") == "0"):
                smtp = SMTP("localhost")
            else:
                smtp = SMTP(Config.get("smtp", "host"), Config.get("smtp", "port"))

            if not ((Config.get("smtp", "host") == "localhost") or (Config.get("smtp", "host") == "127.0.0.1")):
                try:
                    smtp.starttls()
                except SMTPException as e:
                    raise SMSError("unable to shift connection into TLS: %s" % (str(e),))

                try:
                    smtp.login(Config.get("smtp", "user"), Config.get("smtp", "pass"))
                except SMTPException as e:
                    raise SMSError("unable to authenticate: %s" % (str(e),))

            try:
                 smtp.sendmail(Config.get("smtp", "frommail"), addr, "To:%s\nFrom:%s\nSubject:%s\n%s\n" % (addr, "\"%s\" <%s>" % (
                                                               Config.get("Alliance", "name"), Config.get("smtp", "frommail")), subject, message))
            except SMTPSenderRefused as e:
                raise SMSError("sender refused: %s" % (str(e),))
            except SMTPRecipientsRefused as e:
                raise SMSError("unable to send: %s" % (str(e),))

            smtp.quit()
#            self.log_message(user, receiver, email, public_text, "email")

        except (socket.error, SSLError, SMTPException, SMSError) as e:
            return "Error sending message: %s" % (str(e),)

