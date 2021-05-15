#!/usr/bin/python3

import os
import stagger
from shutil import rmtree
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from flask_cors import cross_origin
from configparser import ConfigParser
from base64 import b64encode, b64decode
from deezloader import Login, deezweb_utils
from deezloader.deezer_settings import qualities
from deezloader.exceptions import QualityNotFound

from flask import (
	Flask, request,
	send_file, render_template
)

config = ConfigParser()
config.read("setting.ini")

try:
	deezer_token = config['login']['token']
except KeyError:
	print("Something went wrong with configuration file")
	exit()

app = Flask(__name__)
downloa = Login(deezer_token)
qualities = qualities.keys()
output = "%s/Songs/" % os.getcwd()
ip = "127.0.0.1"
port = 8000
download_api = "http://{}:{}/download?path=%s".format(ip, port)
player_api = "http://{}:{}/play?path=%s".format(ip, port)
want_api = "http://{}:{}/want?link=%s&quality=%s".format(ip, port)

def check_all():
	dirs = "/".join(
		os.path.realpath(__file__).split("/")[:-1]
	)

	folder1 = "%s/templates/" % dirs
	folder2 = "%s/static/" % dirs

	if not os.path.exists(folder1):
		os.makedirs(folder1)
		folder1 += "%s"	
		os.makedirs(folder2)
		js = "%s/js/" % folder2
		css = "%s/css/" % folder2
		imgs = "%s/imgs/" % folder2
		os.makedirs(js)
		os.makedirs(css)
		os.makedirs(imgs)
		js += "%s"
		css += "%s"
		imgs += "%s"

		files = [
			("404.html", deezweb_utils.html404, folder1, "w"),
			("artist_albums.html", deezweb_utils.artist_albums_html, folder1, "w"),
			("deez-web.html", deezweb_utils.deezweb_html, folder1, "w"),
			("player.html", deezweb_utils.player_html, folder1, "w"),
			("playlist.html", deezweb_utils.playlist_html, folder1, "w"),
			("search.html", deezweb_utils.search_html, folder1, "w"),
			("404.css", deezweb_utils.css404, css, "w"),
			("index.css", deezweb_utils.index_css, css, "w"),
			("player.css", deezweb_utils.player_css, css, "w"),
			("playlist.css", deezweb_utils.playlist_css, css, "w"),
			("download.js", deezweb_utils.download_js, js, "w"),
			("player.js", deezweb_utils.player_js, js, "w"),
			("playlist.js", deezweb_utils.playlist_js, js, "w"),
			("search.js", deezweb_utils.search_js, js, "w"),
			("show_album.js", deezweb_utils.show_album_js, js, "w"),
			("slave.js", deezweb_utils.slave_js, js, "w"),
			("utils.js", deezweb_utils.utils_js, js, "w"),
			("deez.ico", b64decode(deezweb_utils.d_ico), imgs, "wb"),
			("deez.jpg", b64decode(deezweb_utils.d_jpg), imgs, "wb")
		]

		for filee, what, where, mode in files:
			fil = open(where % filee, mode)
			fil.write(what)
			fil.close()

def download_link(link, quality):
	if "track/" in link:
		if "spotify" in link:
			method = downloa.download_trackspo

		elif "deezer" in link:
			method = downloa.download_trackdee

		return method(
			link, output, quality,
			True, True
		)

	elif "album/" in link:
		if "spotify" in link:
			method = downloa.download_albumspo

		elif "deezer" in link:
			method = downloa.download_albumdee

		return method(
			link, output, quality,
			True, True,
			zips = True
		)

	elif "playlist/" in link:
		if "spotify" in link:
			method = downloa.download_playlistspo

		elif "deezer" in link:
			method = downloa.download_playlistdee

		return method(
			link, output, quality,
			True, True,
			zips = True
		)

	elif "artist" in link:
		if "spotify" in link:
			return "spotify/artist"

		elif "deezer" in link:
			return "deezer/artist"

@app.route("/")
def index():
	return render_template("deez-web.html")

@app.route("/want")
@cross_origin()
def want():
	params = request.args
	quality = params['quality']

	if not quality in qualities:
		raise QualityNotFound("Invalid quality :(")

	link = params['link']
	datas = download_link(link, quality)

	if type(datas) is tuple:
		streams = [
			player_api % datas[0][a]
			for a in range(
				len(datas[0])
			)
		]

		downloads = [
			download_api % datas[0][a]
			for a in range(
				len(datas[0])
			)
		]

		zips = download_api % datas[1]

		return {
			"paths": datas[0],
			"downloads": downloads,
			"streams": streams,
			"zip_path": datas[1],
			"zip_down": zips
		}

	elif "artist" in datas:
		return {
			"redirect": True
		}

	else:
		download = download_api % datas
		stream = player_api % datas

		return {
			"download": download,
			"stream": stream,
			"path": datas
		}

@app.route("/playlist")
def slist():
	params = request.args
	quality = params['quality']
	link = params['link']
	url = want_api % (link, quality)
	return render_template("playlist.html", url = url)

@app.route("/artist")
def sartist():
	params = request.args
	link = params['link']
	return render_template("artist_albums.html", link = link)

@app.route("/search")
def search():
	return render_template("search.html")

@app.route("/play")
def play():
	path = request.args['path']

	try:
		mp3 = stagger.read_tag(path)
		data = mp3[stagger.id3.APIC][0].data
		song = EasyID3(path)
	except stagger.errors.NoTagError:
		song = FLAC(path)
		data = song.pictures[0].data

	i_encoded = "data:image/jpeg;base64, %s" % b64encode(data).decode()
	title = song['title'][0]
	artist = song['artist'][0]
	album = song['album'][0]
	path = download_api % path

	return render_template(
		"player.html",
		title = title,
		artist = artist,
		album = album,
		image = i_encoded,
		path = path
	)

@app.route("/download")
def download():
	try:
		path = request.args['path']
		return send_file(path)
	except FileNotFoundError:
		return "Wrong path specified"

@app.route("/del")
def delete():
	try:
		path = request.args['path']
		os.remove(path)
		return "DONE"
	except FileNotFoundError:
		return "Wrong path specified"

@app.route("/delall")
def delall():
	for a in os.listdir(output):
		try:
			rmtree(output + a)
		except NotADirectoryError:
			os.remove(output + a)
		except OSError:
			pass

	return "DONE"

@app.route("/js/slave.js")
def slave_js():
	return app.send_static_file("js/slave.js")

@app.route("/js/utils.js")
def utils_js():
	return app.send_static_file("js/utils.js")

@app.route("/js/download.js")
def download_js():
	return app.send_static_file("js/download.js")

@app.route("/js/search.js")
def search_js():
	return app.send_static_file("js/search.js")

@app.route("/js/show_album.js")
def show_album_js():
	return app.send_static_file("js/show_album.js")

@app.route("/js/player.js")
def player_js():
	return app.send_static_file("js/player.js")

@app.route("/js/playlist.js")
def playlist_js():
	return app.send_static_file("js/playlist.js")

@app.route("/css/index.css")
def index_css():
	return app.send_static_file("css/index.css")

@app.route("/css/404.css")
def four04_css():
	return app.send_static_file("css/404.css")

@app.route("/css/player.css")
def player_css():
	return app.send_static_file("css/player.css")

@app.route("/css/playlist.css")
def playlist_css():
	return app.send_static_file("css/playlist.css")

@app.route("/imgs/deez.jpg")
def deez_jpg():
	return app.send_static_file("imgs/deez.jpg")

@app.route("/imgs/deez.ico")
def deez_ico():
	return app.send_static_file("imgs/deez.ico")

@app.errorhandler(404)
def error_404(e):
	return render_template("404.html")

check_all()
app.run("0.0.0.0", port)