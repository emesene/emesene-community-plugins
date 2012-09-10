# -*- coding: utf-8 -*-

#    This file is part of emesene.
#
#    emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
import os
import extension
from plugin_base import PluginBase
import e3
import gui
import subprocess
import urllib2

try:
    import tinyurl  #you need to install tinyurl for using /tiny
except ImportError:
    pass


class Plugin(PluginBase):
    _description = 'Run some commands in conversation'
    _authors = { 'James Axl' : 'axlrose112@gmail.com' , 'Sbte' : '' }

    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        self.session = session
        self.session.signals.conv_started.subscribe(self.open_conv)
        self.soundPlayer = extension.get_and_instantiate('sound', session)
        self.homedir = os.path.expanduser('~/')
        return True

    def stop(self):
        self.session.signals.conv_started.unsubscribe(self.open_conv)
        return False

    def config(self, session):
        pass

    def open_conv(self, cid, account):
        conversation = self.session.get_conversation(cid)
        conversation.input.on_send_message = Fun(self.custom_on_send_message, conversation)
                
    def _gui_message_(self,text,conv):
        cedict = conv.emcache.parse()
        custom_emoticons = gui.base.MarkupParser.get_custom_emotes(text, cedict)
        message = e3.Message(e3.Message.TYPE_INFO, text, None, None) 
        self.session.send_message(conv.cid, text, conv.cstyle, cedict, custom_emoticons)
        message.body="<b><a href = \"%s\">%s</a> was successfully generated and sent :)</b>" % (text, text)
        self.session.gui_message(conv.cid, '', message)
        
    def check_tiny(self,conversation,url,message,group=True):
        if len(url) != 2:
            message.body = "<b>Please type /help for more help</b>"
        else:
            req = urllib2.Request(url[1])
            try:
                urllib2.urlopen(req)
                url = tinyurl.create_one(url[1])
                if group:
                    for conv in self.session.conversations.itervalues():
                        self._gui_message_(url,conv)
                else:
                    self._gui_message_(url,conversation)
                       
            except NameError:
                message.body = "<b>Please install tinyurl e.g: easy_install tinyurl or pip install tiny</b>"
            except ValueError:
                message.body = "<b>Check your URL please</b>"
            except urllib2.URLError:
                message.body = "<b>Check your URL please</b>"
            
    def custom_on_send_message(self, conversation, text):
        cid = conversation.cid
        if text.startswith("/"):
            commands = ["/help", "/clear", "/nudge", "/run", "/tiny", "/all","/tiny-all",
            "/message","/online","/away","/busy","/invisible","/block","/idle"]
            text = text.split()
            command = text[0]
            message = e3.Message(e3.Message.TYPE_INFO, '', None, None)
            if command in commands:
                if command == "/help":
                    help = """<ul><strong><li>/clear for cleaning chat window.</li></strong>
                            <strong><li>/nudge for sending nudge to user.</li></strong>
                            <strong><li>/run for running command e.g /run mplayer <I>fatman.mp3</I>, /run firefox or /run mplayer <I>james axl.flv</I>
                            <span>DEFAULT PATH IS YOUR HOME DIRECTORY</span>.</li></strong>
                            <strong><li>/tiny for sending large URL e.g /tiny large_url.</li></strong>
			    <strong><li>/all for sending message to all conversations.</li></strong>
			    <strong><li>/tiny-all for sending large URL to all conversations.</li></strong>
                <strong><li>Change status, <b>/online "Status"<b/>, <b>/busy "Status"<b/>, <b>/away "Status"<b/>, <b>/idle "Status"<b/>, <b>/invisible<b/>.</li></strong>
                <strong><li>/message to set message of the session.</li></strong>
			    <ul>"""
                    message = e3.Message(e3.Message.TYPE_INFO, help, '', timestamp = None)
                elif command == "/clear":
                    conversation.output.clear()
                elif command == "/nudge":
                    self.session.request_attention(cid)
                    message.body = _('You just sent a nudge!')
                    self.soundPlayer.play(gui.theme.sound_theme.sound_nudge)
                elif command == "/run":
                    if len(text) >= 3 :
                        try:
                            subprocess.Popen([text[1], self.homedir+' '.join(text[2:])])
                        except NameError:
                            message.body = "<b>Command not found</b>"
                    elif len(text) < 3 and len(text)>1:
                        try:
                            subprocess.Popen([text[1]])
                        except OSError:
                            message.body = "<b>Command not found</b>"
                    else:
                            message.body = "<b>Please type /help for more help</b>"
                elif command == "/tiny":
                    self.check_tiny(conversation,text,message,False)        
                elif command == "/all":
                    if len(text) > 1:
                        for conv in self.session.conversations.itervalues():
                            conv._on_send_message(' '.join(text[1:]))
                elif command == "/tiny-all":
                    self.check_tiny(None,text,message)
                elif command == "/online":
                    self.session.set_status(e3.status.ONLINE)
                    if text[1:]: self.session.set_message(' '.join(text[1:]))
                elif command == "/invisible":
                    self.session.set_status(e3.status.OFFLINE)
                    if text[1:]: self.session.set_message(' '.join(text[1:]))
                elif command == "/busy":
                    self.session.set_status(e3.status.BUSY)
                    if text[1:]: self.session.set_message(' '.join(text[1:]))
                elif command == "/away":
                    self.session.set_status(e3.status.AWAY)
                    if text[1:]: self.session.set_message(' '.join(text[1:]))
                elif command == "/idle":
                    self.session.set_status(e3.status.IDLE)
                    if text[1:]: self.session.set_message(' '.join(text[1:]))  
                elif command == "/message":
                    self.session.set_message(' '.join(text[1:]))
            else:
                message.body = "<b>Please type /help for more help</b>"

            if message.body:
                self.session.gui_message(cid, '', message)
        else:
            conversation._on_send_message(text)

class Fun(object):  #Sbte who had the idea for using this class instead of change emesene code.
    def __init__(self, fun, conv):
        self.fun = fun
        self.conv = conv

    def __call__(self, text):
        self.fun(self.conv, text)