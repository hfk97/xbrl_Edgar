#Big chunks of this code were written by Altova Gmbh see: https://github.com/hfk97/xbrl_Edgar/blob/master/loadSECfilings.py (Copyright 2014 Altova GmbH)

import pip

try:
	import sys

except ImportError:
	pip.main(['install', "sys"])
	import sys


import subprocess
import importlib



# function that imports a library if it is installed, else installs it and then imports it
def getpack(package):
    try:
        return (importlib.import_module(package))
        # import package
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
        return (importlib.import_module(package))
        # import package


import os.path
import getopt
import time
import socket
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET
import zipfile
zlib=getpack("zlib")
feedparser=getpack("feedparser")



def downloadfile( sourceurl, targetfname ):
	mem_file = ""
	good_read = False
	xbrlfile = None
	if os.path.isfile( targetfname ):
		print( "Local copy already exists" )
		return True
	else:
		print( "Downloading:", sourceurl )
		try:
			xbrlfile = urlopen( sourceurl )
			try:
				mem_file = xbrlfile.read()
				good_read = True
			finally:
				xbrlfile.close()
		except HTTPError as e:
			print( "HTTP Error:", e.code )
		except URLError as e:
			print( "URL Error:", e.reason )
		except TimeoutError as e:
			print( "Timeout Error:", e.reason )
		except socket.timeout:
			print( "Socket Timeout Error" )
		if good_read:
			output = open( targetfname, 'wb' )
			output.write( mem_file )
			output.close()
		return good_read

def SECdownload(year, month):
	root = None
	feedFile = None
	feedData = None
	good_read = False
	itemIndex = 0
	edgarFilingsFeed = 'http://www.sec.gov/Archives/edgar/monthly/xbrlrss-' + str(year) + '-' + str(month).zfill(2) + '.xml'
	print( edgarFilingsFeed )
	if not os.path.exists( "sec/" + str(year) ):
		os.makedirs( "sec/" + str(year) )
	if not os.path.exists( "sec/" + str(year) + '/' + str(month).zfill(2) ):
		os.makedirs( "sec/" + str(year) + '/' + str(month).zfill(2) )
	target_dir = "sec/" + str(year) + '/' + str(month).zfill(2) + '/'
	try:
		feedFile = urlopen( edgarFilingsFeed )
		try:
			feedData = feedFile.read()
			good_read = True
		finally:
			feedFile.close()
	except HTTPError as e:
		print( "HTTP Error:", e.code )
	except URLError as e:
		print( "URL Error:", e.reason )
	except TimeoutError as e:
		print( "Timeout Error:", e.reason )
	except socket.timeout:
		print( "Socket Timeout Error" )
	if not good_read:
		print( "Unable to download RSS feed document for the month:", year, month )
		return
	# we have to unfortunately use both feedparser (for normal cases) and ET for old-style RSS feeds,
	# because feedparser cannot handle the case where multiple xbrlFiles are referenced without enclosure
	try:
		root = ET.fromstring(feedData)
	except ET.ParseError as perr:
		print( "XML Parser Error:", perr )
	feed = feedparser.parse( feedData )
	try:
		print( feed[ "channel" ][ "title" ] )
	except KeyError as e:
		print( "Key Error:", e )
	# Process RSS feed and walk through all items contained
	for item in feed.entries:
		print( item[ "summary" ], item[ "title" ], item[ "published" ] )
		try:
			# Identify ZIP file enclosure, if available
			enclosures = [ l for l in item[ "links" ] if l[ "rel" ] == "enclosure" ]
			if ( len( enclosures ) > 0 ):
				# ZIP file enclosure exists, so we can just download the ZIP file
				enclosure = enclosures[0]
				sourceurl = enclosure[ "href" ]
				cik = item[ "edgar_ciknumber" ]
				targetfname = target_dir+cik+'-'+sourceurl.split('/')[-1]
				retry_counter = 3
				while retry_counter > 0:
					good_read = downloadfile( sourceurl, targetfname )
					if good_read:
						break
					else:
						print( "Retrying:", retry_counter )
						retry_counter -= 1
			else:
				# We need to manually download all XBRL files here and ZIP them ourselves...
				linkname = item[ "link" ].split('/')[-1]
				linkbase = os.path.splitext(linkname)[0]
				cik = item[ "edgar_ciknumber" ]
				zipfname = target_dir+cik+'-'+linkbase+"-xbrl.zip"
				if os.path.isfile( zipfname ):
					print( "Local copy already exists" )
				else:
					edgarNamespace = {'edgar': 'http://www.sec.gov/Archives/edgar'}
					currentItem = list(root.iter( "item" ))[itemIndex]
					xbrlFiling = currentItem.find( "edgar:xbrlFiling", edgarNamespace )
					xbrlFilesItem = xbrlFiling.find( "edgar:xbrlFiles", edgarNamespace )
					xbrlFiles = xbrlFilesItem.findall( "edgar:xbrlFile", edgarNamespace )
					if not os.path.exists(  target_dir+"temp" ):
						os.makedirs( target_dir+"temp" )
					zf = zipfile.ZipFile( zipfname, "w" )
					try:
						for xf in xbrlFiles:
							xfurl = xf.get( "{http://www.sec.gov/Archives/edgar}url" )
							if xfurl.endswith( (".xml",".xsd") ):
								targetfname = target_dir+"temp/"+xfurl.split('/')[-1]
								retry_counter = 3
								while retry_counter > 0:
									good_read = downloadfile( xfurl, targetfname )
									if good_read:
										break
									else:
										print( "Retrying:", retry_counter )
										retry_counter -= 1
								zf.write( targetfname, xfurl.split('/')[-1], zipfile.ZIP_DEFLATED )
								os.remove( targetfname )
					finally:
						zf.close()
						os.rmdir( target_dir+"temp" )
		except KeyError as e:
			print( "Key Error:", e )
		finally:
			print( "----------" )
		itemIndex += 1

def main(argv):
	year = 2013
	month = 1
	from_year = 1999
	to_year = 1999
	year_range = False
	if not os.path.exists( "sec" ):
		os.makedirs( "sec" )
	socket.setdefaulttimeout(10)
	start_time  = time.time()
	try:
		opts, args = getopt.getopt(argv,"hy:m:f:t:",["year=","month=","from=","to="])
	except getopt.GetoptError:
		print( 'loadSECfilings -y <year> -m <month> | -f <from_year> -t <to_year>' )
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print( 'loadSECfilings -y <year> -m <month> | -f <from_year> -t <to_year>' )
			sys.exit()
		elif opt in ("-y", "--year"):
			year = int(arg)
		elif opt in ("-m", "--month"):
			month = int(arg)
		elif opt in ("-f", "--from"):
			from_year = int(arg)
			year_range = True
		elif opt in ("-t", "--to"):
			to_year = int(arg)
			year_range = True
	if year_range:
		if from_year == 1999:
			from_year = to_year
		if to_year == 1999:
			to_year = from_year
		for year in range( from_year, to_year+1 ):
			for month in range( 1, 12+1 ):
				SECdownload( year, month )
	else:
		SECdownload( year, month )
	end_time = time.time()
	print( "Elapsed time:", end_time - start_time, "seconds" )

if __name__ == "__main__":
	main(sys.argv[1:])
