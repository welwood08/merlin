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
#
# Module by Martin Stone
 
import socket
from smtplib import SMTP, SMTPException, SMTPSenderRefused, SMTPRecipientsRefused
from ssl import SSLError
from Core.exceptions_ import SMSError
from Core.config import Config
from Core.string import decode, encode
from Core.db import session
from Core.maps import User, SMS
from Core.loadable import loadable, route, require_user

class email(loadable):
    """Sends an email to the specified user. Your username will be included automatically."""
    usage = " <nick> <message>"
    access = 3 # Member
    
    @route(r"(\S+)\s+(\+\+\+)?(.+)", access = "email")
    @require_user
    def execute(self, message, user, params):
        
        rec = params.group(1)
        shortmsg = params.group(2) is not None
        public_text = params.group(3) + (' - %s' % (user.name,) if not shortmsg else '')
        text = encode(public_text)
        receiver=User.load(name=rec,exact=False) or User.load(name=rec)
        if not receiver:
            message.reply("Who exactly is %s?" % (rec,))
            return

        email = receiver.email
        if not email:
            message.reply("That incompetent retard %s hasn't provided an address. Super secret message not sent." % (receiver.name,))
            return

        error = ""
        
        error = self.send_email(user, receiver, public_text, email, text, shortmsg)
        
        if error is None:
            message.reply("Successfully processed To: %s Message: %s" % (receiver.name, decode(text)))
        else:
            message.reply(error or "That wasn't supposed to happen. I don't really know what went wrong. Maybe your mother dropped you.")

    def send_email(self, user, receiver, public_text, email, message, shortmsg=False):
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
                 smtp.sendmail(Config.get("smtp", "frommail"), email, 
                              "To:%s\nFrom:%s\nSubject:%s\n\n%s\n" % (email,
                                                                    Config.get("smtp", "frommail"),
                                                                    Config.get("Alliance", "name") + " (%s)%s" % (user.name, (": "+message) if shortmsg else ""),
                                                                    "" if shortmsg else message,))
            except SMTPSenderRefused as e:
                raise SMSError("sender refused: %s" % (str(e),))
            except SMTPRecipientsRefused as e:
                raise SMSError("unable to send: %s" % (str(e),))
            
            smtp.quit()
            self.log_message(user, receiver, email, public_text, "email")
            
        except (socket.error, SSLError, SMTPException, SMSError) as e:
            return "Error sending message: %s" % (str(e),)
    
    def log_message(self,sender,receiver,email,text,mode):
        session.add(SMS(sender=sender,receiver=receiver,phone=email,sms_text=text,mode=mode))
        session.commit()
