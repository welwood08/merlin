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

from Core.maps import UserAccess, GroupAccess, UserGroup, ChanAccess
from Core.db import session

def has_access(user, function):
    return (session.query(UserAccess.access_id, UserAccess.user_id).filter(access_id == function.lower()).filter(UserAccess.user_id == user.id).count() > 0
    or session.query(GroupAccess.access_id, UserGroup.user_id).filter(ChanAccess.access_id == function.lower()).filter(UserGroup.group_id == GroupAccess.group_id).filter(UserGroup.user_id == user.id).count() > 0)

def chan_access(channel, function):
    return (session.query(ChanAccess.access_id, ChanAccess.channel_id).filter(ChanAccess.access_id == function.lower()).filter(ChanAccess.channel_id == channel.id).count() > 0)
