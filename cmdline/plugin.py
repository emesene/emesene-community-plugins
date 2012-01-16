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
    _description = 'Run some commands from window chat'
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

    def custom_on_send_message(self, conversation, text):
        cid = conversation.cid
        if text.startswith("/"):
            commands = ["/help", "/clear", "/nudge", "/run", "/tiny", "/all"]
            chck = text.split('[')
            text = text.split(' ')
            command = text[0]
            message = e3.Message(e3.Message.TYPE_INFO, '', None, None)
            if command in commands:
                if command == "/help":
                    help = """<ul><strong><li>/clear for cleaning chat window.</li></strong>
                            <strong><li>/nudge for sending nudge to user.</li></strong>
                            <strong><li>/run for running command e.g /run mplayer [fatman.mp3], /run firefox or /run mplayer [james axl.flv]
                            <span>DEFAULT PATH IS YOUR HOME DIRECTORY</span>.</li></strong>
                            <strong><li>/tiny for sending large URL e.g /tiny large_url.</li></strong<ul>"""
                    message = e3.Message(e3.Message.TYPE_INFO, help, '', timestamp = None)
                elif command == "/clear":
                    conversation.output.clear()
                elif command == "/nudge":
                    self.session.request_attention(cid)
                    message.body = _('You just sent a nudge!')
                    self.soundPlayer.play(gui.theme.sound_theme.sound_nudge)
                elif command == "/run":
                    if len(chck) == 2:
                        try:
                            c = ' '.join(text[1:])
                            text = c.split('[')
                            subprocess.Popen([command[:-1], self.homedir+text[1][:-1]])
                        except NameError:
                            message.body = "<b>Command not found</b>"
                        except OSError:
                            message.body = "<b>File not found</b>"
                    elif len(text) == 2:
                        try:
                            subprocess.Popen([text[1]])
                        except OSError:
                            message.body = "<b>Command not found</b>"
                    elif len(text) == 1:
                             message.body = "<b>Please type /help for more help</b>"
                elif command == "/tiny":
                    if len(text) != 2:
                        message.body = "<b>Please type /help for more help</b>"
                    else:
                        req = urllib2.Request(text[1])
                        try:
                            urllib2.urlopen(req)
                            url = tinyurl.create_one(text[1])
                            message = e3.Message(e3.Message.TYPE_MESSAGE, url, None, None) #It is look ilogical but i need it :).
                            self.session.gui_message(cid, '', message)
                            message.type = e3.Message.TYPE_INFO
                            message.body = "<b><a href = \"%s\">%s</a> was successfully generated and sent :)</b>" % (url, url)
                        except NameError:
                            message.body = "<b>Please install tinyurl</b>"
                        except ValueError:
                            message.body = "<b>Check your URL please</b>"
                        except urllib2.URLError:
                            message.body = "<b>Check your URL please</b>"
                elif command == "/all":
                    if len(text) > 1:
                        for conv in self.session.conversations.itervalues():
                            conv._on_send_message(' '.join(text[1:]))

            else:
                message.body = "<b>Please type /help for more help</b>"

            if message.body:
                self.session.gui_message(cid, '', message)
        else:
            conversation._on_send_message(text)

class Fun(object):                  #Sbte who has the idea for using this class instead of change emesene code.
    def __init__(self, fun, conv):
        self.fun = fun
        self.conv = conv

    def __call__(self, text):
        self.fun(self.conv, text)
