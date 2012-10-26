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
 
from sqlalchemy.sql import asc, desc
from Core.db import session
from Core.maps import User
from Core.loadable import loadable, route
from Core.config import Config

class paranoidcunts(loadable):
    """List members who are have not set their phone number properly. Optionally sanity-checks phone numbers."""
    usage = " [galmates] [check]"
    
    @route(r"(.*)", access = "admin")
    def execute(self, message, user, params):
        reply = ""
        opts = params.group(1).split()

        Q = session.query(User.name, User.alias)
        if ("galmates" not in opts):
            Q = Q.filter(User.access > 0)
        Q = Q.filter(User.pubphone == False)
        Q = Q.order_by(asc(User.name))
        result = Q.all()
        if len(result) > 0:
            printable=map(lambda (u, a): "%s%s" % (u,' ('+a+')' if a else ''),result)
        reply += "pubphone=F:    "
        reply += ', '.join(printable)
        reply += '\n'

        Q = session.query(User.name, User.alias)
        if ("galmates" not in opts):
            Q = Q.filter(User.access > 0)
        Q = Q.filter(User.phone == '')
        Q = Q.order_by(asc(User.name))
        result = Q.all()

        if len(result) > 0:
            printable=map(lambda (u, a): "%s%s" % (u,' ('+a+')' if a else ''),result)
        reply += "No phone set:  "
        reply += ', '.join(printable)
        reply += '\n'

        if ("check" in opts):
            Q = session.query(User.name, User.alias, User.phone)
            if ("galmates" not in opts):
                Q = Q.filter(User.access > 0)
            Q = Q.order_by(asc(User.name))
            result = Q.all()
            
            res = []
            for [u, a, n] in result:
                if n and (len(n) <= 7) and (n[1:].isdigit()) and (n[0].isdigit() or n[0] == '+'):
                    res.append([u,a,n])
            if len(res) > 0:
                printable=map(lambda (u, a, n): "%s%s: %s" % (u,' ('+a+')' if a else '',n),res)
            reply += "Bad number:    %s\n" % (', '.join(printable))

        message.reply(reply)
