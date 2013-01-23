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
 
from Core import Merlin
from Core.exceptions_ import PNickParseError
from Core.db import session
from Core.maps import User, Tell
from Core.loadable import loadable, route, require_user, system

class tell(loadable):
    """Sends a message to a user when they next join a channel with me."""
    usage = " <nick> <message>"
    access = "member"
    
    @route(r"(\S+)\s+(.+)", access = "member")
    @require_user
    def execute(self, message, user, params):
        text = params.group(2)
        rec = params.group(1)
        receiver=User.load(name=rec,exact=False,access="member") or User.load(name=rec)
        if not receiver:
            message.reply("Who exactly is %s?" % (rec,))
            return

        receiver.tells.append(Tell(sender_id=user.id, message=text))
        session.commit()

        message.reply("Successfully stored message for %s. Message: %s" % (receiver.name, text))

@system('JOIN')
def join(message):
    # Someone is joining a channel
    if message.get_nick() != Merlin.nick:
        # Someone is joining a channel we're in
        try:
            u = User.load(name=message.get_pnick())
            if u is None:
                return
            tells = u.newtells
            for tell in tells:
                message.notice("Message from %s: %s" % (tell.sender.name, tell.message), message.get_nick())
                tell.read = True
            session.commit()
        except PNickParseError:
            return
