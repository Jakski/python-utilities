#!/usr/bin/python3

from gi.repository import Gtk
from gi.repository import GObject
import webbrowser
import urllib.request
import re

def getNyan():
	USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36"
	r = urllib.request.Request("http://nyanyan.it/", headers={'User-Agent': USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'})
	data = urllib.request.urlopen(r)
	data = data.read()
	found = re.findall( '<div class="tytul">.*<div class="stronicowanieD" style="width:700px;margin-left:20px">', str(data) )
	return found[0]
class nyanIcon:	
	def __init__( self ):
		self.site = getNyan()
		self.trayicon = Gtk.StatusIcon()
		self.trayicon.set_from_file( "normal.png" )
		self.trayicon.set_visible( True )
		self.trayicon.connect( "activate", self.openNyan )
		self.trayicon.connect( "popup-menu", self.options )
		GObject.timeout_add( 5000, self.checkNyan )
		Gtk.main()
	def options( self, icon, button, time ):
		self.menu = Gtk.Menu()
		
		exit = Gtk.MenuItem()
		exit.set_label( "Exit" )
		exit.connect( "activate", Gtk.main_quit )
		
		self.menu.append( exit )
		self.menu.show_all()
		
		def pos( menu, icon):
			return (Gtk.StatusIcon.position_menu(menu, icon))
		self.menu.popup(None, None, pos, self.trayicon, button, time)
	def checkNyan( self, *args ):
		tempsite = getNyan()
		if tempsite != self.site:
			self.site = tempsite
			self.trayicon.set_from_file( "new.png" )
		GObject.timeout_add( 60000*5, self.checkNyan )
	def openNyan( self, *args ):
		self.trayicon.set_from_file( "normal.png" )
		webbrowser.open( "http://nyanyan.it/" )

app = nyanIcon()
