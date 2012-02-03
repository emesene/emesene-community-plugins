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
import e3
import re
import urlparse
import urllib
try:
    import BeautifulSoup
except ImportError:
    pass

class Plugin(PluginBase):
    _description = "Showing youtube video's thumb in conversation"
    _authors = { 'James Axl' : 'axlrose112@gmail.com' }

    def __init__(self):
        PluginBase.__init__(self)
	
    def start(self, session):
        self.session = session
        self.session.signals.conv_message.subscribe(self._on_message)
        return True

    def stop(self):
         self.session.signals.conv_message.unsubscribe(self._on_message)
         return False


    def configurable(self):
         return False


    def check_url(self,cid, account, msg):
        s = msg
        l=re.findall(r'(http?://www.youtube.com/watch\S+)', s)
        if len(l) >= 1:
                msg_text=l[0]
                url_data = urlparse.urlparse(msg_text)
                query = urlparse.parse_qs(url_data.query)
                video_id = query["v"][0]
                if video_id:
                        try:		
                            src = BeautifulSoup.BeautifulSoup(urllib.urlopen("http://www.youtube.com/watch?v=%s"%video_id))
                            title=src.title.string.split('\n')[1].strip()
                            image="""<a  href="http://www.youtube.com/v/%s">
                                 <img  src="http://img.youtube.com/vi/%s/hqdefault.jpg" width="150" height="150"></a> <h3>%s</h3>"""%(video_id,video_id,title)
                            url=e3.Message(e3.Message.TYPE_INFO, image,account,timestamp=None)                   
                        except NameError:
                            warn="""<P><B>BeautifulSoup</B> is required by youtube plugin please run <B>easy_install BeautifulSoup</B> or <B>pip install BeautifulSoup</B> </P> """
                            url=e3.Message(e3.Message.TYPE_INFO, warn,account,timestamp=None)
                self.session.gui_message(cid, account, url)
                
    def _on_message(self, cid, account, message, cedict=None):	
        user = self.session.contacts.get(account)
        msg_text=message.body
        message=e3.Message(e3.Message.TYPE_INFO, msg_text,account,timestamp=None)
        self.check_url(cid, account, message.body)
