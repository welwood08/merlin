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
 
# The generic objects used to send messages to callbacks and such.

import re, time

from Core import Merlin
from Core.exceptions_ import ParseError, ChanParseError, MsgParseError, PNickParseError
from Core.config import Config
from Core.string import encode

PUBLIC_PREFIX  = ("!",)
QUERY_PREFIX   = ("@",)
NOTICE_PREFIX  = ("~",)
PRIVATE_PREFIX = (".","-",)
PUBLIC_REPLY  = 1
PRIVATE_REPLY = 2
NOTICE_REPLY  = 3

pnickre = re.compile(r":.+!.+@(.+)\.%s" %(re.escape(Config.get("Services","usermask")),), re.I)

class Message(object):
    # The message object will be passed around to callbacks for inspection and ability to write to the server
    
    _chanerror = False # Will be set to True on failure to parse.
    _msgerror = False # Will be set to True on failure to parse.
    
    def parse(self, line):
        # Parse the irc line
        r = parse_raw_irc(line)
        self.line = line
        self._nick = r['source']['name']
        self._hostmask = r['source']['full']
        self._command = r['msg']
        self._channel = r['params'][0]
        if not self._channel:
            self._chanerror = True
        
        # Encoding
        self._nick = encode(self._nick)
        self._hostmask = encode(self._hostmask)
        self._command = encode(self._command)
        self._channel = encode(self._channel)
        
        # Message
        self._msg = r['params'][-1]
        if (not self._msg or self._msg.strip() == "") and self._command != "PRIVMSG":
            # CUT needed this, but merlin gets *very* upset on an empty PRIVMSG.
            self._msgerror = True
    
    def __str__(self):
        # String representation of the Message object (Namely for debugging purposes)
        try:
            return "[%s] <%s> %s" % (self.get_chan(), self.get_nick(), encode(self.get_msg()))
            return "[%s] <%s> %s" % (self.get_chan(), self.get_nick(), self.get_msg())
        except ParseError:
            return ""
    
    def get_nick(self):
        # Return a parsed nick
        return self._nick
    
    def get_hostmask(self):
        # Return a parsed hostmask
        return self._hostmask
    
    def get_command(self):
        # Return the command
        return self._command

    def get_chan(self):
        # Return a channel. Raises ParseError on failure
        if self._chanerror: # Raise a ParseError: Some RAWs do not containt a target
            raise ChanParseError("Could not parse target.")
        return self._channel
    
    def in_chan(self):
        # Return True if the message was in a channel (as opposed to PM)
        return False if self.get_chan().lower() == Merlin.nick.lower() else True
    
    def get_pnick(self):
        #Return the pnick. Raises ParseError on failure
        match = pnickre.match(self.line.split()[0])
        if not match: # Raise a ParseError: User hasn't authed with P
            raise PNickParseError("Could not parse %s nick."%(Config.get("Services", "nick"),))
        return match.group(1)
    
    def get_msg(self):
        # Return the message part of a line. Raises ParseError on failure        
        if self._msgerror: # Raise a ParseError: Some RAWs do not containt a target
            raise MsgParseError("Could not parse line.")
        return self._msg
    
    def get_prefix(self):
        # Return the prefix used for commands
        return self.get_msg()[0] if self.get_msg() and self.get_msg()[0] in PUBLIC_PREFIX+QUERY_PREFIX+NOTICE_PREFIX+PRIVATE_PREFIX else None
    
    def reply_type(self):
        # Return the proper way to respond based on the command prefix used
        # Always reply to a PM with a PM, otherwise only ! replies with privmsg
        # Always reply to an @command with a PM
        p = self.get_prefix()
        
        if p in PUBLIC_PREFIX and self.in_chan():
            return PUBLIC_REPLY
        
        if p in QUERY_PREFIX:
            return PRIVATE_REPLY
        
        if p in NOTICE_PREFIX:
            return NOTICE_REPLY
        
        if p in PRIVATE_PREFIX and self.in_chan():
            return NOTICE_REPLY
        
        if p in PUBLIC_PREFIX+PRIVATE_PREFIX and not self.in_chan():
            return PRIVATE_REPLY

# Parser from jobe1986 (http://pastebin.mdbnet.net/180)
def parse_raw_irc(line):
    ret = {'source': {'full': "", 'name': "", 'ident': "", 'host': ""}, 'msg': "", 'params': []}

    stat = 0

    words = line.split(' ')

    for word in words:
        if ((stat < 3) and (len(word) == 0)):
            continue

        if (stat == 0):
            stat += 1
            if (word[0] == ":"):
                 ret['source']['full'] = word[1:]
            else:
                ret['msg'] = word
                stat += 1
        elif (stat == 1):
            ret['msg'] = word
            stat += 1
        elif (stat == 2):
            if (word[0] == ":"):
                ret['params'].append(word[1:])
                stat += 1
            else:
                ret['params'].append(word)
        else:
            ret['params'][-1] = ret['params'][-1] + " " + word
    #end for

    if (len(ret['source']['full']) > 0):
        src = ret['source']['full']
        if (src.find("@") >= 0):
            ret['source']['host'] = src[src.find("@")+1:]
            src = src[:src.find("@")]
        if (src.find("!") >= 0):
            ret['source']['ident'] = src[src.find("!")+1:]
            src = src[:src.find("!")]
        ret['source']['name'] = src
    #end if

    return ret
