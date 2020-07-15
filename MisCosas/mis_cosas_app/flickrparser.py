from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class FlickrHandler(ContentHandler):
    def __init__ (self):
        """Initialization of variables for the parser
        * inEntry: within <entry>
        * inContent: reading interesting target content (leaf strings)
        * content: target content being readed
        * title: title of the current entry
        * id: id of the current entry
        * link: link of the current entry
        * videos: list of videos (<entry> elements) in the channel,
            each video is a dictionary (title, link, id)
        """
        self.inEntry = False
        self.inContent = False
        # Para las fotos
        self.content = ""
        self.title = ""
        self.id = ""
        self.link = ""
        self.photo = ""
        self.photos = []
        # Para el alimentador
        self.taglink = ""
        self.tagname = ""

    def startElement (self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title': # Título de la foto
                self.inContent = True
            elif name == 'link' and attrs.get('type') == "text/html": # Link de la publicación
                self.link = attrs.get('href')
            elif name == 'id':  # ID de la publicación
                self.inContent = True
            elif name == 'link' and attrs.get('type') == "image/jpeg": # Link de la imagen
                self.photo = attrs.get('href')
        elif not self.inEntry:
            if name == 'link' and attrs.get('type') == "text/html": # Link de la etiqueta
                self.taglink = attrs.get('href')
            elif name == 'id': # Nombre de la etiqueta
                self.inContent = True


    def endElement (self, name):
        global videos

        if name == 'entry':
            self.inEntry = False
            self.photos.append({'link': self.link,
                                'title': self.title,
                                'id': self.id,
                                'photo': self.photo})
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == 'id':
                self.id = self.content.split('photo/')[1]
                self.content = ""
                self.inContent = False
        elif not self.inEntry:
            if name == 'id':
                self.tagname = self.content.split('all/')[1]
                self.content = ""
                self.inContent = False

    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class FlickrParser:
    """Class to get videos in a YouTube channel.
    Extracts video links and titles from the XML document for a YT channel.
    The list of videos found can be retrieved lated by calling videos()
    """

    def __init__(self, stream):
        self.parser = make_parser()
        self.handler = FlickrHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(stream)

    def fotos (self):
        return self.handler.photos

    def nombre_etiqueta(self):
        return self.handler.tagname


    def link_etiqueta(self):
        return self.handler.taglink
