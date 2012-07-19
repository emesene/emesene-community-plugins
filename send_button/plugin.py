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

from plugin_base import PluginBase
import gtk

class Plugin(PluginBase):
    _description = 'Show the Send button in conversation window'
    _authors = { 'moneycat' : 'moneycat.tw gmail com' }

    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        '''start the plugin'''
        self.session = session
        self.session.signals.conv_started.subscribe(self.open_conv)
        return True

    def stop(self):
        '''stop the plugin'''
        self.session.signals.conv_started.unsubscribe(self.open_conv)
        return False

    def config(self, session):
        '''config the plugin'''
        pass

    def open_conv(self, cid, account):
        '''add the button when open a conversation'''
        conversation = self.session.get_conversation(cid)

        if conversation:
            # find the widget
            frame_input = conversation.panel.get_children()[1]
            input_box = frame_input.get_children()[0]

            # deattach the widget
            input_box.remove(conversation.input)

            # attach the new widget
            button = gtk.Button(_('Send'))
            button.connect('clicked',
                lambda *args: conversation.input._textbox.emit('message-send'))
            button.set_sensitive(False)
            button.show()

            hhbox = gtk.HButtonBox()
            hhbox.add(button)
            hhbox.show()

            hbox = gtk.HBox()
            hbox.pack_start(conversation.input, True, True)
            hbox.pack_start(hhbox, False, False)
            hbox.show()
        
            input_box.pack_start(hbox, True, True)

            # enable or disable the button, depends on input area
            conversation.input._buffer.connect('changed',
                lambda widget: button.set_sensitive(widget.get_char_count()))
