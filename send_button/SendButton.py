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

import gtk
from gui.gtkui import Conversation

class SendButton(Conversation.Conversation):
    '''Show the Send button in conversation window'''
    NAME = 'Send Button'
    DESCRIPTION = 'Show the Send button in conversation window'
    AUTHOR = 'moneycat'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session, cid, update_win, tab_label, members=None):
        '''constructor'''
        Conversation.Conversation.__init__(self, session, cid, 
                                           update_win, tab_label, members)

        # find out the parent of widget
        frame_input = self.panel.get_children()[1]
        input_box = frame_input.get_children()[0]

        # deattach the widget
        input_box.remove(self.input)

        # attach the new widget
        button = gtk.Button(_('Send'))
        button.connect('clicked',
                       lambda *args: self.input._textbox.emit('message-send'))
        button.show()

        hhbox = gtk.HButtonBox()
        hhbox.add(button)
        hhbox.show()

        hbox = gtk.HBox()
        hbox.pack_start(self.input, True, True)
        hbox.pack_start(hhbox, False, False)
        hbox.show()
        
        input_box.pack_start(hbox, True, True)
