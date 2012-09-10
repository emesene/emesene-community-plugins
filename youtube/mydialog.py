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
import webkit
import gobject #gobject is needed for threads
import pango
import subprocess
import os
import tempfile
from E_youtube import Browser

class WatchVideo():
        
    def init_info(self):
        self.images=[]
        self.videos=[]
        self.titles=[]
        self.users=[]

    def __init__(self):
        self._tmp=tempfile.gettempdir()
        self.bl=0
        self.pointer=0
        self.init_info()
        gobject.threads_init()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.resize(425,150)
        self.window.set_resizable(True)
        self.window.set_title("Emesene Youtube")
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.move(30, 30)
        self.window.connect("delete_event", self.win_hide)
        self.vbox = gtk.VBox()
       
        self.hbox = gtk.HBox()
        self.hbox.set_spacing(4)
        self.hbox.set_border_width(4)
      
        self.image = gtk.Image()
       
        self.imagebox = gtk.HBox()
        self.imagebox.set_border_width(4)
        self.image.set_alignment(0.0, 0.5)

        self.vboxtext = gtk.VBox()
        self.pages = self._buildpages()
        self.text = gtk.Label()
        self.text.set_selectable(True)
        self.text.set_ellipsize(3) #pango.ELLIPSIZE_END
        self.text.set_alignment(0.0, 0.0) # top left
        self.text.set_width_chars(60)

        # hboxbuttons + button box
        self.hboxbuttons = gtk.HBox()
        self.hboxbuttons.set_spacing(4)
        self.hboxbuttons.set_border_width(4)
        self.buttonbox = gtk.HButtonBox()
        self.buttonbox.set_layout(gtk.BUTTONBOX_END)

        # the contents of the buttonbox
        self.watchvideo = gtk.Button()
        self.watchvideo.add(gtk.Label('Watch Video'))
        self.watchvideo.connect('clicked', self.watch_video)
        self.removevideo = gtk.Button(stock=gtk.STOCK_REMOVE)
        self.removevideo.connect('clicked', self.remove)

        self.window.add(self.vbox)
        self.vbox.pack_start(self.hbox, True, True)
        self.vbox.pack_start(self.hboxbuttons, False, False)

        self.imagebox.pack_start(self.image)
        self.hbox.pack_start(self.imagebox, False, False)
        self.hbox.pack_start(self.vboxtext, True, True)
        self.vboxtext.pack_start(self.pages, False, False)
        self.vboxtext.pack_start(self.text, True, True)

        self.hboxbuttons.pack_start(self.watchvideo, False, False)
        self.hboxbuttons.pack_start(self.removevideo, False, False)
        self.hboxbuttons.pack_start(self.buttonbox)

        if not self.pointer:
            self.update()
            
    def _buildpages(self):
        '''Builds hboxpages, that is a bit complex to include in __init__'''
        hboxpages = gtk.HBox()
        arrowleft = TinyArrow(gtk.ARROW_LEFT)
        self.buttonleft = gtk.Button()
        self.buttonleft.set_relief(gtk.RELIEF_NONE)
        self.buttonleft.add(arrowleft)
        self.buttonleft.connect('clicked', self.switchvideo, -1)

        arrowright = TinyArrow(gtk.ARROW_RIGHT)
        self.buttonright = gtk.Button()
        self.buttonright.set_relief(gtk.RELIEF_NONE)
        self.buttonright.add(arrowright)
        self.buttonright.connect('clicked', self.switchvideo, 1)

        self.currentpage = gtk.Label()

        hboxpages.pack_start(gtk.Label(), True, True) # align to right
        hboxpages.pack_start(self.buttonleft, False, False)
        hboxpages.pack_start(self.currentpage, False, False)
        hboxpages.pack_start(self.buttonright, False, False)

        return hboxpages
    def switchvideo(self, button, order):
        '''Moves the video info pointer +1 or -1'''
        if (self.pointer + order) >= 0:
            if (self.pointer + order) < len(self.titles):
                self.pointer += order
            else:
                self.pointer = 0         
        else:
            self.pointer = len(self.titles) - 1
        self.update()
        
    def update(self):
        '''Update the GUI, including labels, arrow buttons, images, etc'''
        try:
            #mail, nick = self.mails[self.pointer]
            title=self.titles[self.pointer]
            user=self.users[self.pointer]
            image=self.images[self.pointer]
          
        except IndexError:
            self.win_hide(self)            
            return
    
        titlestring = '<b>%s</b>' % title
        userstring= '<b>%s</b>' % user
        self.text.set_markup(userstring + (' sent you ')+titlestring+('\nDo you want to watch this video? '))
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(image)
        scaled_buf = pixbuf.scale_simple(150,150,gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(scaled_buf)
        
        self.buttonleft.set_sensitive(True)
        self.buttonright.set_sensitive(True)
       
        if self.pointer == 0:
            self.buttonleft.set_sensitive(False)
        if self.pointer == len(self.titles) - 1:
            self.buttonright.set_sensitive(False)

        self.currentpage.set_markup('<b>(%s/%s)</b>' % \
            (self.pointer + 1, len(self.titles)))        


    def set_video(self,title,video,image,user):
        self.images.append(image)
        self.videos.append(video)
        self.titles.append(title)
        self.users.append(user)
        self.update()
          
    def watch_video(self,button):
        watch = Browser(self.videos[self.pointer], self.titles[self.pointer])
        watch.show_window()                                           
        self.remove(None)
                
    def remove(self,button):
        self.titles.pop(self.pointer)
        self.videos.pop(self.pointer)
        self.users.pop(self.pointer)
        self.images.pop(self.pointer)
        self.switchvideo(None, 1)
                
    def win_hide(self,*args):
        self.window.hide() 
        self.bl=0
        self.init_info()
        return gtk.TRUE
        
    def win_show(self):
        self.window.show_all()
        self.bl=1
    
    def main(self):
        gtk.main()
                
class TinyArrow(gtk.DrawingArea):
    LENGTH = 8
    WIDTH = 5

    def __init__(self, arrow_type, shadow=gtk.SHADOW_NONE):
        gtk.DrawingArea.__init__(self)
        self.arrow_type = arrow_type
        self.shadow = shadow
        self.margin = 0

        self.set_size_request(*self.get_size())
        self.connect("expose_event", self.expose)

    def get_size(self):
        if self.arrow_type in (gtk.ARROW_LEFT, gtk.ARROW_RIGHT):
            return (TinyArrow.WIDTH + self.margin*2, \
                    TinyArrow.LENGTH + self.margin*2)
        else:
            return (TinyArrow.LENGTH + self.margin*2, \
                    TinyArrow.WIDTH + self.margin*2)

    def expose(self, widget=None, event=None):
        if self.window is None:
            return
        self.window.clear()
        width, height = self.get_size()
        self.get_style().paint_arrow(self.window, self.state, \
            self.shadow, None, self, '', self.arrow_type, True, \
            0, 0, width, height)

        return False

    def set(self, arrow_type, shadow=gtk.SHADOW_NONE, margin=None):
        self.arrow_type = arrow_type
        self.shadow = shadow
        if margin is not None:
            self.margin = margin
        self.set_size_request(*self.get_size())
        self.expose()                