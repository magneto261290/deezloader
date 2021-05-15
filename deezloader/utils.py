#!/usr/bin/python3

import zipfile
from requests import get
from mutagen import File
from spotipy import oauth2
from os.path import isfile
from os import makedirs, remove
from deezloader import exceptions
from collections import OrderedDict
from mutagen.id3._util import ID3NoHeaderError
from mutagen.flac import error as NOTVALIDSONG

from deezloader.deezer_settings import (
	songs_server, api_album
)

from mutagen.id3 import (
	ID3, APIC, USLT
)

from mutagen.flac import (
	FLAC, Picture, FLACNoHeaderError
)

from deezloader.deezer_settings import (
	api_search_trk, cover, header
)

from deezloader.others_settings import (
	spotify_client_id, spotify_client_secret
)

def generate_token():
	return oauth2.SpotifyClientCredentials(
		client_id = spotify_client_id,
		client_secret = spotify_client_secret
	).get_access_token()

def choose_img(image):
	image = request(cover % image).content

	if len(image) == 13:
		image = request(cover % "").content

	return image

def get_ids(URL):
	ids = (
		URL
		.split("?utm")[0]
		.split("/")[-1]
	)

	return ids

def request(url, control = False):
	try:
		thing = get(url, headers = header)
	except:
		thing = get(url, headers = header)

	if control:
		try:
			if thing.json()['error']['message'] == "no data":
				raise exceptions.NoDataApi("No data avalaible :(")
		except KeyError:
			pass

		try:
			if thing.json()['error']['message'] == "Quota limit exceeded":
				raise exceptions.QuotaExceeded("Too much requests limit yourself")
		except KeyError:
			pass

	return thing

def create_zip(zip_name, nams):
	z = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)

	for a in nams:
		b = a.split("/")[-1]

		try:
			z.write(a, b)
		except FileNotFoundError:
			pass

	z.close()

def artist_sort(array):
	if len(array) > 1:
		for a in array:
			for b in array:
				if a in b and a != b:
					array.remove(b)

	artists = ", ".join(
		OrderedDict.fromkeys(array)
	)

	return artists

def check_dir(directory):
	try:
		makedirs(directory)
	except FileExistsError:
		pass

def check_md5_song(infos):
	try:
		song_md5 = infos['FALLBACK']['MD5_ORIGIN']
		version = infos['FALLBACK']['MEDIA_VERSION']
	except KeyError:
		song_md5 = infos['MD5_ORIGIN']
		version = infos['MEDIA_VERSION']

	return song_md5, version

def var_excape(string):
	string = (
		string
		.replace("\\", "")
		.replace("/", "")
		.replace(":", "")
		.replace("*", "")
		.replace("?", "")
		.replace("\"", "")
		.replace("<", "")
		.replace(">", "")
		.replace("|", "")
		.replace("&", "")
	)

	return string

def not_found(song, title):
	url = request(
		api_search_trk % song.replace("#", ""), True
	).json()

	for b in range(url['total'] + 1):
		if url['data'][b]['title'] == title or title in url['data'][b]['title_short']:
			ids = url['data'][b]['link'].split("/")[-1]
			break

	return ids

def song_exist(n, song_hash):
	crypted_audio = request(
		songs_server.format(n, song_hash)
	)

	if len(crypted_audio.content) == 0:
		raise exceptions.TrackNotFound("")

	return crypted_audio

def tracking(URL, album = None):
	datas = {}
	json_track = request(URL, True).json()

	if not album:
		json_album = request(
			api_album % str(json_track['album']['id']), True
		).json()

		datas['genre'] = []

		try:
			for a in json_album['genres']['data']:
				datas['genre'].append(a['name'])
		except KeyError:
			pass

		datas['genre'] = " & ".join(datas['genre'])
		datas['ar_album'] = []

		for a in json_album['contributors']:
			if a['role'] == "Main":
				datas['ar_album'].append(a['name'])

		datas['ar_album'] = " & ".join(datas['ar_album'])
		datas['album'] = json_album['title']
		datas['label'] = json_album['label']
		datas['upc'] = json_album['upc']

	datas['music'] = json_track['title']
	array = []

	for a in json_track['contributors']:
		if a['name'] != "":
			array.append(a['name'])

	array.append(
		json_track['artist']['name']
	)

	datas['artist'] = artist_sort(array)
	datas['tracknum'] = str(json_track['track_position'])
	datas['discnum'] = str(json_track['disk_number'])
	datas['year'] = json_track['release_date']
	datas['bpm'] = str(json_track['bpm'])
	datas['duration'] = str(json_track['duration'])
	datas['isrc'] = json_track['isrc']
	return datas

def write_tags(song, data):
	try:
		tag = FLAC(song)
		tag.delete()
		images = Picture()
		images.type = 3
		images.data = data['image']
		tag.clear_pictures()
		tag.add_picture(images)
		tag['lyrics'] = data['lyric']
	except FLACNoHeaderError:
		try:
			tag = File(song, easy = True)
			tag.delete()
		except:
			if isfile(song):
				remove(song)

			raise exceptions.TrackNotFound("")
	except NOTVALIDSONG:
		raise exceptions.TrackNotFound("")

	tag['artist'] = data['artist']
	tag['title'] = data['music']
	tag['date'] = data['year']
	tag['album'] = data['album']
	tag['tracknumber'] = data['tracknum']
	tag['discnumber'] = data['discnum']
	tag['genre'] = data['genre']
	tag['albumartist'] = data['ar_album']
	tag['author'] = data['author']
	tag['composer'] = data['composer']
	tag['copyright'] = data['copyright']
	tag['bpm'] = data['bpm']
	tag['length'] = data['duration']
	tag['organization'] = data['label']
	tag['isrc'] = data['isrc']
	tag['lyricist'] = data['lyricist']
	tag.save()

	try:
		audio = ID3(song)

		audio.add(
			APIC(
				encoding = 3,
				mime = "image/jpeg",
				type = 3,
				desc = u"Cover",
				data = data['image']
			)
		)

		audio.add(
			USLT(
				encoding = 3,
				lang = u"eng",
				desc = u"desc",
				text = data['lyric']
			)
		)

		audio.save()
	except ID3NoHeaderError:
		pass

def what_kind(link):
	url = request(link).url
	return url