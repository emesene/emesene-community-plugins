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
import gobject #you need to import webkit and gobject, gobject is needed for threads
import webkit

class Browser:

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.window.destroy()

    def __init__(self,default_site,title):
        self.default_site=default_site
        
        gobject.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.resize(350,300)
        self.window.set_resizable(True)
        self.window.set_title(title)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.web_view = webkit.WebView()
        self.web_view.open(self.default_site)

        scroll_window = gtk.ScrolledWindow(None, None)
        scroll_window.add(self.web_view)

        vbox = gtk.VBox(False, 0)
        vbox.add(scroll_window)
        self.window.add(vbox)

    def show_window(self):
        self.window.show_all()