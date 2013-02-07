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
from Core.string import decode, encode
from Core.db import session
from Core.maps import User, SMS
from Core.loadable import loadable, route, require_user
from yowsup.src.Examples.EchoClient import WhatsappEchoClient

class whatsapp(loadable):
    """Sends a WhatsApp message to the specified user. Your username will be appended to the end of each sms. The user must have their phone correctly added and you must have access to their number."""
    usage = " <nick> <message>"
    
    @route(r"(\S+)\s+(.+)", access = "member")
    @require_user
    def execute(self, message, user, params):
        
        rec = params.group(1)
        public_text = params.group(2) + ' - %s' % (user.name,)
        text = encode(public_text + '/%s' %(user.phone,))
        receiver=User.load(name=rec,exact=False,access="member") or User.load(name=rec)
        if not receiver:
            message.reply("Who exactly is %s?" % (rec,))
            return
        if receiver.smsmode == "Retard":
            message.reply("I refuse to talk to that incompetent retard. Check %s's mydef comment and use !phone show to try sending it using your own phone." %(receiver.name,))
            return 

        if not (receiver.pubphone or receiver.smsmode =="Email") and user not in receiver.phonefriends and user.access < (Config.getint("Access","SMSer") if "SMSer" in Config.options("Access") else 1000):
            message.reply("%s's phone number is private or they have not chosen to share their number with you. Supersecret message not sent." % (receiver.name,))
            return

        phone = self.prepare_phone_number(receiver.phone)
        if not phone or len(phone) <= 7:
            message.reply("%s has no phone number or their phone number is too short to be valid (under 6 digits). Super secret message not sent." % (receiver.name,))
            return

        if len(text) >= 160:
            message.reply("Max length for a text is 160 characters. Your text was %i characters long. Super secret message not sent." % (len(text),))
            return

        error = ""
        
        ##############################################################################################################
        ##############################################################################################################
    
        wa = WhatsappEchoClient(phone[1:], text, True)
        wa.login(Config.get("WhatsApp", "login"), Config.get("WhatsApp", "password"))
        if wa.gotReceipt:
            message.reply("Successfully processed To: %s Message: %s" % (receiver.name, decode(text)))
        else:
            message.reply(error or "That wasn't supposed to happen. I don't really know what went wrong. Maybe your mother dropped you.")

        ##############################################################################################################
        ##############################################################################################################
    
    def prepare_phone_number(self,text):
        if not text:
            return text
        s = "".join([c for c in text if c.isdigit()])
        return "+"+s.lstrip("00")

    def log_message(self,sender,receiver,phone,text,mode):
        session.add(SMS(sender=sender,receiver=receiver,phone=phone,sms_text=text,mode=mode))
        session.commit()
