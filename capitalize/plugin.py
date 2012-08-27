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

import extension
from plugin_base import PluginBase

class MessageProcessor:
    @classmethod
    def capitalize(self, message):
        # message is e3.base.Message.Message
        # we just process and replace the message.body
        message.body = message.body[0].upper() + message.body[1:]

class Plugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        send_cb_handler = extension.get_instance('send message callback handler')
        # Append our callback to the PriorityList which is processed
        # when an e3.base.Message.Message is fired from the UI
        send_cb_handler.append(MessageProcessor.capitalize, prio=-99)
        return True

    def stop(self):
        send_cb_handler = extension.get_instance('send message callback handler')
        # Remove the callback from the PriorityList so we cleanup resources
        send_cb_handler.remove(MessageProcessor.capitalize)
        return False

    def config(self, session):
        '''method to config the plugin'''
        pass
