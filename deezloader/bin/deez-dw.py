#!/usr/bin/python3

from os.path import isfile
from deezloader import Login
from argparse import ArgumentParser
from configparser import ConfigParser
from deezloader.utils import what_kind

logo = """
	d8888b. d88888b d88888b d88888D        d8888b. db   d8b   db 
	88  `8D 88'     88'     YP  d8'        88  `8D 88   I8I   88 
	88   88 88ooooo 88ooooo    d8'         88   88 88   I8I   88 
	88   88 88~~~~~ 88~~~~~   d8'   C8888D 88   88 Y8   I8I   88 
	88  .8D 88.     88.      d8' db        88  .8D `8b d8'8b d8' 
	Y8888D' Y88888P Y88888P d88888P        Y8888D'  `8b8' `8d8'
"""

print(logo)

def download_link(
	link, output,
	quality, recursive_quality,
	recursive_download, not_gui, zips
):
	link = what_kind(link)

	if "track/" in link:
		if "spotify" in link:
			func = downloa.download_trackspo
		elif "deezer" in link:
			func = downloa.download_trackdee
		else:
			return

		func(
			link, output,
			quality, recursive_quality,
			recursive_download, not_gui
		)

	elif "album/" in link:
		if "spotify" in link:
			func = downloa.download_albumspo
		elif "deezer" in link:
			func = downloa.download_albumdee
		else:
			return

		func(
			link, output,
			quality, recursive_quality,
			recursive_download, not_gui, zips
		)

	elif "playlist/" in link:
		if "spotify" in link:
			func = downloa.download_playlistspo
		elif "deezer" in link:
			func = downloa.download_playlistdee
		else:
			return
		
		func(
			link, output,
			quality, recursive_quality,
			recursive_download, not_gui, zips
		)

parser = ArgumentParser(description = "Deezloader downloader")

if not isfile("setting.ini"):
	parser.add_argument(
		"setting",
		help = "Path for the setting file"
	)

parser.add_argument(
	"-l", "--link",
	help = "Deezer or Spotify link for download"
)

parser.add_argument(
	"-s", "--song",
	help = "song name"
)

parser.add_argument(
	"-a", "--artist",
	help = "artist song"
)

parser.add_argument(
	"-o", "--output",
	help = "Output folder"
)

parser.add_argument(
	"-q", "--quality",
	help = "Select download quality between FLAC, 320, 256, 128"
)

parser.add_argument(
	"-rq", "--recursive_quality",
	help = "If choosen quality doesn't exist download with best possible quality (True or False)"
)

parser.add_argument(
	"-rd", "--recursive_download",
	help = "If the song has already downloaded skip (True or False)"
)

parser.add_argument(
	"-g", "--not_gui",
	help = "Show the little not_gui (True or False)"
)

parser.add_argument(
	"-z", "--zip",
	help = "If is an album or playlist link create a zip archive (True or False)"
)

args = parser.parse_args()

try:
	ini_file = args.setting
except AttributeError:
	ini_file = "setting.ini"

config = ConfigParser()
config.read(ini_file)

try:
	token = config['login']['token']
except KeyError:
	print("Something went wrong with configuration file")
	exit()

downloa = Login(token)
link = args.link
output = args.output
quality = args.quality

if quality and quality != "FLAC":
	quality = "MP3_%s" % quality

recursive_quality = bool(args.recursive_quality)
recursive_download = bool(args.recursive_download)
zips = bool(args.zip)
song = args.song
artist = args.artist
not_gui = bool(args.not_gui)

if not output:
	output = "Songs"

if not quality:
	quality = "MP3_320"

if not recursive_quality:
	recursive_quality = False

if not recursive_download:
	recursive_download = False

if not zips:
	zips = False

if not not_gui:
	not_gui = False

if link:
	download_link(
		link, output, 
		quality, recursive_quality,
		recursive_download, not_gui, zips
	)

if song and artist:
	downloa.download_name(
		artist, song,
		output, quality,
		recursive_quality, recursive_download, not_gui
	)