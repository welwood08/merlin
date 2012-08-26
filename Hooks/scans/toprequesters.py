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
 
from sqlalchemy.sql import asc, desc
from sqlalchemy.sql.functions import count
from Core.db import session
from Core.maps import Request, User, Updates
from Core.loadable import loadable, route
from Core.config import Config

class toprequesters(loadable):
    """List top scan requesters in the last x ticks."""
    usage = " <age> <number>"
    access = "admin"
    alias = "topreq"
    
    @route(r"([0-9]+) ([0-9]+)")
    def execute(self, message, user, params):
        reply = ""
        tick=Updates.current_tick()
        age = int(params.group(1))
        num = int(params.group(2))
        Q = session.query(Request, count())
        if age > 0:
            Q = Q.filter(Request.tick >= tick-age)
        Q = Q.group_by(Request.requester_id)
        Q = Q.order_by(desc(count()))
        result = Q.all()
        if len(result) < 1:
           message.reply("No scan requests found in the last %d ticks" % (age))
        printable=map(lambda (r, c): "%s%s: %s" % (r.user.name,' ('+r.user.alias+')' if r.user.alias else '', c),result[:num])
        reply += ', '.join(printable)
        reply += '\n'
        message.reply(reply)
