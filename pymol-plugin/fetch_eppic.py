'''
Pymol plugin to load EPPIC interface files

DESCRIPTION

EPPIC:
	EPPIC stands fror Evolutionary Protein-Protein Interface Classifier. EPPIC mainly aims at classifying the interfaces present in protein crystal lattices in order to determine whether they are biologically relevant or not. EPPIC can be accessed from www.eppic-web.org

Installation:
copy this file to /modules/pmg_tk/startup/ in the pymol installation path
restart pymol, now you will have additional entry called "Eppic Interface Loader" in Plugin menu


Usage:
Entering 4 digit pdb code will load all interfaces for a given pdbid
Example: 2gs2
Entering pdbid-interfceid will load only specified interface.
Example: 2gs2-2


Command line:
load_eppic is the command line tool for this plugin.



Usage:
	Method 1:
	load_eppic <pdbid> 
	This command will load all the interface files for a given pdbid
	example:
	load_eppic 2gs2

	Method 2:
	load_eppic <pdbid-interfaceid>
	This command will load only specified interface
	example:
	load_eppic 2gs2-2

	The interface ids are listed in EPPIC server


Author : Kumaran Baskaran

Date   : 10.04.2014

'''


from Tkinter import *
from pymol import cmd
from string import atoi
import os
import tkSimpleDialog
import tkMessageBox
import urllib2,StringIO,gzip
import gzip
import os


def __init__(self):
	# Simply add the menu entry and callback
	self.menuBar.addmenuitem('Plugin', 'command', 'EPPIC Interface Loader',
				label = 'EPPIC Interface Loader',
				command = lambda s=self : FetchEPPIC(s))



class FetchEPPIC:
	def __init__(self, app):
		fetchpath=cmd.get('fetch_path')
		pdbCode = tkSimpleDialog.askstring('EPPIC Loader Service',
                                                      'Please enter a 4-digit pdb code:',
                                                      parent=app.root)
		if pdbCode:
			if len(pdbCode)>4:
				pdbid=pdbCode.split("-")[0]
				ifaceid=atoi(pdbCode.split("-")[1])
				filename=os.path.join(fetchpath, "%s-%d.pdb"%(pdbid,ifaceid))
				check_fetch=self.fetch_eppic(pdbid,ifaceid,filename)
				if check_fetch:
					cmd.load(filename,pdbCode)
				else:
					tkMessageBox.showinfo('Loading failed for %s'%(pdbCode),
        	                               'No Interface found\n(or)\nPDB not found')
			else:
				ifaceid=1
				pdbid=pdbCode
				while(1):
					filename=os.path.join(fetchpath, "%s-%d.pdb"%(pdbid,ifaceid))
					check_fetch=self.fetch_eppic(pdbid,ifaceid,filename)
					if check_fetch:
						cmd.load(filename,"%s-%d"%(pdbid,ifaceid))
						ifaceid+=1
					else:
						if ifaceid==1:
							tkMessageBox.showinfo('Loading failed for %s'%(pdbCode),
        	                              			 'No Interface found\n(or)\nPDB not found')
						else:
							tkMessageBox.showinfo('Loading Completed',
        	                               			'%d interfaces loaded'%(ifaceid-1))
						break

	def fetch_eppic(self,pdbid,ifaceid,filename):	
		fetchurl="http://eppic-web.org/ewui/ewui/fileDownload?type=interface&id=%s&interface=%d"%(pdbid,ifaceid)
		request=urllib2.Request(fetchurl)
		request.add_header('Accept-encoding', 'gzip')
		opener=urllib2.build_opener()
		f=opener.open(request)
		compresseddata = f.read()
		if len(compresseddata)>0:
			compressedstream = StringIO.StringIO(compresseddata)
			gzipper = gzip.GzipFile(fileobj=compressedstream)
			data = gzipper.read()
			open(filename,'w').write(data)
			is_done=1
		else:
			is_done=0
		return is_done

def load_eppic(pdbCode):
	'''
	DESCRIPTION

	EPPIC:
		EPPIC stands fro Evolutionary Protein-Protein Interface Classifier. EPPIC mainly aims at classifying the interfaces present in protein crystal lattices in order to determine whether they are biologically relevant or not. EPPIC can be accessed from www.eppic-web.org

	load_eppic is a command line tool to download interface files from EPPIC server to open in pymol

	Usage:
	Method 1:
	load_eppic <pdbid> 
	This command will load all the interface files for a given pdbid
	example:
	load_eppic 2gs2

	Method 2:
	load_eppic <pdbid-interfaceid>
	This command will load only specified interface
	example:
	load_eppic 2gs2-2

	The interface ids are listed in EPPIC server

	Author : Kumaran Baskaran
	Date   : 11.04.2014
	'''
	fetchpath=cmd.get('fetch_path')
	if pdbCode:
		if len(pdbCode)>4:
			pdbid=pdbCode.split("-")[0]
			ifaceid=atoi(pdbCode.split("-")[1])
			filename=os.path.join(fetchpath, "%s-%d.pdb"%(pdbid,ifaceid))
			check_fetch=fetch_eppic(pdbid,ifaceid,filename)
			if check_fetch:
				cmd.load(filename,pdbCode)
			else:
				print "No Interface Found"			

		else:
			ifaceid=1
			pdbid=pdbCode
			while(1):
				filename=os.path.join(fetchpath, "%s-%d.pdb"%(pdbid,ifaceid))
				check_fetch=fetch_eppic(pdbid,ifaceid,filename)
				if check_fetch:
					cmd.load(filename,"%s-%d"%(pdbid,ifaceid))
					ifaceid+=1
				else:
					if ifaceid==1:
						print "No Interface Found"
					else:
						print "%d Interface Loaded"%(ifaceid-1)
					break
def fetch_eppic(pdbid,ifaceid,filename):	
		fetchurl="http://eppic-web.org/ewui/ewui/fileDownload?type=interface&id=%s&interface=%d"%(pdbid,ifaceid)
		request=urllib2.Request(fetchurl)
		request.add_header('Accept-encoding', 'gzip')
		opener=urllib2.build_opener()
		f=opener.open(request)
		compresseddata = f.read()
		if len(compresseddata)>0:
			compressedstream = StringIO.StringIO(compresseddata)
			gzipper = gzip.GzipFile(fileobj=compressedstream)
			data = gzipper.read()
			open(filename,'w').write(data)
			is_done=1
		else:
			is_done=0
		return is_done

cmd.extend("load_eppic",load_eppic)
