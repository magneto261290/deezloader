#!/usr/bin/python3

from tqdm import tqdm
from os import getcwd
from os.path import isfile
from spotipy import Spotify
from requests import Session
from deezloader.others_settings import answers

from deezloader import(
	utils, methods, exceptions,
	download_utils, deezer_settings
)

stock_output = "%s/Songs" % getcwd()
stock_quality = "MP3_320"
stock_recursive_quality = False
stock_recursive_download = False
stock_not_interface = False
stock_zip = False

class Login:
	def __init__(self, token):
		self.spo = Spotify(
			utils.generate_token()
		)

		self.req = Session()
		self.req.cookies['arl'] = token
		self.get_user_data = methods.method_get_user_data
		self.private_api_link = deezer_settings.private_api_link
		user_id = self.get_api(self.get_user_data)['USER']['USER_ID']

		if user_id == 0:
			raise exceptions.BadCredentials("Wrong token: %s :(" % token)

		self.qualities = deezer_settings.qualities
		self.songs_server = deezer_settings.songs_server
		self.get_song_data = methods.method_get_song_data
		self.get_lyric = methods.method_get_lyric
		self.get_album = methods.method_get_album
		self.get_album_data = methods.method_get_album_data
		self.api_track = deezer_settings.api_track
		self.api_album = deezer_settings.api_album
		self.api_playlist = deezer_settings.api_playlist

	def get_api(self, method, api_token = "null", json_data = None):
		params = {
			"api_version": "1.0",
			"api_token": api_token,
			"input": "3",
			"method": method
		}

		try:
			return self.req.post(
				self.private_api_link,
				params = params,
				json = json_data
			).json()['results']
		except:
			return self.req.post(
				self.private_api_link,
				params = params,
				json = json_data
			).json()['results']

	def download(
		self, link, details,
		recursive_quality = None,
		recursive_download = None,
		not_interface = None,
		zips = False
	):
		if not details['quality'] in self.qualities:
			raise exceptions.QualityNotFound("The qualities have to be FLAC or MP3_320 or MP3_256 or MP3_128")

		self.token = self.get_api(self.get_user_data)['checkForm']
		ids = utils.get_ids(link)
		datas = details['datas']
		quality = details['quality']
		output = details['output']

		def get_infos(method, json_data):
			infos = self.get_api(method, self.token, json_data)
			return infos

		def check_quality_song(infos, datas):
			ids = infos['SNG_ID']
			num_quality = self.qualities[quality]['n_quality']
			file_format = self.qualities[quality]['f_format']
			song_quality = self.qualities[quality]['s_quality']
			song_md5, version = utils.check_md5_song(infos)
			song_hash = download_utils.genurl(song_md5, num_quality, ids, version)

			try:
				crypted_audio = utils.song_exist(song_md5[0], song_hash)
			except (IndexError, exceptions.TrackNotFound):
				if not recursive_quality:
					raise exceptions.QualityNotFound("The quality chosen can't be downloaded")

				for a in self.qualities:
					if details['quality'] == a:
						continue

					num_quality = self.qualities[a]['n_quality']
					file_format = self.qualities[a]['f_format']
					song_quality = self.qualities[a]['s_quality']
					song_hash = download_utils.genurl(song_md5, num_quality, ids, infos['MEDIA_VERSION'])

					try:
						crypted_audio = utils.song_exist(song_md5[0], song_hash)
					except exceptions.TrackNotFound:
						raise exceptions.TrackNotFound("Error with this song %s" % link)

			album = utils.var_excape(datas['album'])

			directory = (
				"%s%s %s/"
				% (
					"%s/" % output,
					album,
					datas['upc']
				)
			)

			name = (
				"%s%s CD %s TRACK %s"
				% (
					directory,
					album,
					datas['discnum'],
					datas['tracknum']
				)
			)

			utils.check_dir(directory)
			name += " ({}){}".format(song_quality, file_format)

			if isfile(name):
				if recursive_download:
					return name

				ans = input("Track %s already exists, do you want to redownload it?(y or n):" % name)

				if not ans in answers:
					return name

			decrypted_audio = open(name, "wb")

			download_utils.decryptfile(
				crypted_audio.iter_content(2048),
				download_utils.calcbfkey(ids),
				decrypted_audio
			)

			utils.write_tags(
				name, 
				add_more_tags(datas, infos, ids)
			)

			return name

		def add_more_tags(datas, infos, ids):
			json_data = {
				"sng_id": ids
			}

			try:
				datas['author'] = " & ".join(
					infos['SNG_CONTRIBUTORS']['author']
				)
			except:
				datas['author'] = ""

			try:
				datas['composer'] = " & ".join(
					infos['SNG_CONTRIBUTORS']['composer']
				)
			except:
				datas['composer'] = ""

			try:
				datas['lyricist'] = " & ".join(
					infos['SNG_CONTRIBUTORS']['lyricist']
				)
			except:
				datas['lyricist'] = ""

			try:
				datas['version'] = infos['VERSION']
			except KeyError:
				datas['version'] = ""

			need = get_infos(self.get_lyric, json_data)

			try:
				datas['lyric'] = need['LYRICS_TEXT']
				datas['copyright'] = need['LYRICS_COPYRIGHTS']
				datas['lyricist'] = need['LYRICS_WRITERS']
			except KeyError:
				datas['lyric'] = ""
				datas['copyright'] = ""
				datas['lyricist'] = ""

			return datas

		def tracking2(infos, datas):
			image = utils.choose_img(infos['ALB_PICTURE'])
			datas['image'] = image
			song = "{} - {}".format(datas['music'], datas['artist'])

			if not not_interface:
				print("Downloading: %s" % song)

			try:
				nams = check_quality_song(infos, datas)
			except exceptions.TrackNotFound:
				try:
					ids = utils.not_found(song, datas['music'])
				except IndexError:
					raise exceptions.TrackNotFound("Track not found: %s" % song)

				json_data = {
					"sng_id": ids
				}

				infos = get_infos(self.get_song_data, json_data)
				nams = check_quality_song(infos, datas)

			return nams

		if "track" in link:
			json_data = {
				"sng_id" : ids
			}

			infos = get_infos(self.get_song_data, json_data)
			nams = tracking2(infos, datas)
			return nams

		zip_name = ""

		if "album" in link:
			nams = []
			detas = {}
			quali = ""

			json_data = {
				"alb_id": ids,
				"nb": -1
			}

			infos = get_infos(self.get_album, json_data)['data']

			image = utils.choose_img(
				infos[0]['ALB_PICTURE']
			)

			detas['image'] = image
			detas['album'] = datas['album']
			detas['year'] = datas['year']
			detas['genre'] = datas['genre']
			detas['ar_album'] = datas['ar_album']
			detas['label'] = datas['label']
			detas['upc'] = datas['upc']

			t = tqdm(
				range(
					len(infos)
				),
				desc = detas['album'],
				disable = not_interface
			)

			for a in t:
				detas['music'] = datas['music'][a]
				detas['artist'] = datas['artist'][a]
				detas['tracknum'] = datas['tracknum'][a]
				detas['discnum'] = datas['discnum'][a]
				detas['bpm'] = datas['bpm'][a]
				detas['duration'] = datas['duration'][a]
				detas['isrc'] = datas['isrc'][a]
				song = "{} - {}".format(detas['music'], detas['artist'])
				t.set_description_str(song)

				try:
					nams.append(
						check_quality_song(infos[a], detas)
					)
				except exceptions.TrackNotFound:
					try:
						ids = utils.not_found(song, detas['music'])

						json = {
							"sng_id": ids
						}

						nams.append(
							check_quality_song(
								get_infos(self.get_song_data, json), 
								detas
							)
						)
					except (exceptions.TrackNotFound, IndexError):
						nams.append(song)
						print("Track not found: %s :(" % song)
						continue

				quali = (
					nams[a]
					.split("(")[-1]
					.split(")")[0]
				)

			if zips:
				album = utils.var_excape(datas['album'])

				directory = (
					"%s%s %s/"
					% (
						"%s/" % output,
						album,
						datas['upc']
					)
				)

				zip_name = (
					"%s%s (%s).zip"
					% (
						directory,
						album,
						quali
					)
				)

				try:
					utils.create_zip(zip_name, nams)
				except FileNotFoundError:
					raise exceptions.QualityNotFound(
						"Can't download album \"{}\" in {} quality".format(album, details['quality'])
					)

		elif "playlist" in link:
			json_data = {
				"playlist_id": ids,
				"nb": -1
			}

			infos = get_infos(methods.method_get_playlist_data, json_data)['data']
			nams = []

			for a in range(
				len(infos)
			):
				try:
					nams.append(
						tracking2(infos[a], datas[a])
					)
				except TypeError:
					c = infos[a]
					song = "{} - {}".format(c['SNG_TITLE'], c['ART_NAME'])
					nams.append("Track not found")

			quali = "ALL"

			if zips:
				zip_name = (
					"%s %s (%s).zip"
					% (
						"%s/playlist" % output,
						ids,
						quali
					)
				)

				utils.create_zip(zip_name, nams)

		return nams, zip_name

	def download_trackdee(
		self, URL,
		output = stock_output,
		quality = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface
	):
		datas = {}
		ids = utils.get_ids(URL)
		URL2 = self.api_track % ids
		datas = utils.tracking(URL2)

		details = {
			"datas": datas,
			"quality": quality,
			"output": output

		}

		name = self.download(
			URL2, details,
			recursive_quality,
			recursive_download,
			not_interface
		)

		return name

	def download_albumdee(
		self, URL,
		output = stock_output,
		quality = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		zips = stock_zip
	):
		datas = {}
		datas['music'] = []
		datas['artist'] = []
		datas['tracknum'] = []
		datas['discnum'] = []
		datas['bpm'] = []
		datas['duration'] = []
		datas['isrc'] = []
		names = []
		ids = utils.get_ids(URL)
		URL2 = self.api_album % ids
		album_json = utils.request(URL2, True).json()
		datas['album'] = album_json['title']
		datas['label'] = album_json['label']
		datas['year'] = album_json['release_date']
		datas['upc'] = album_json['upc']
		datas['genre'] = []

		try:
			for a in album_json['genres']['data']:
				datas['genre'].append(a['name'])
		except KeyError:
			pass

		datas['genre'] = " & ".join(datas['genre'])
		datas['ar_album'] = []

		for a in album_json['contributors']:
			if a['role'] == "Main":
				datas['ar_album'].append(a['name'])

		datas['ar_album'] = " & ".join(datas['ar_album'])

		for a in album_json['tracks']['data']:
			URL3 = self.api_track % str(a['id'])
			detas = utils.tracking(URL3, True)
			datas['music'].append(detas['music'])
			discnum = detas['discnum']
			tracknum = detas['tracknum']
			datas['tracknum'].append(tracknum)
			datas['discnum'].append(discnum)
			datas['bpm'].append(detas['bpm'])
			datas['duration'].append(detas['duration'])
			datas['isrc'].append(detas['isrc'])
			datas['artist'].append(detas['artist'])

		details = {
			"datas": datas,
			"quality": quality,
			"output": output
		}

		names, zip_name = self.download(
			URL2, details,
			recursive_quality,
			recursive_download,
			not_interface, zips
		)

		if zips:
			return names, zip_name

		return names

	def download_playlistdee(
		self, URL,
		output = stock_output,
		quality = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		zips = stock_zip
	):
		datas = []
		ids = utils.get_ids(URL)
		URL2 = self.api_playlist % ids
		playlist_json = utils.request(URL2, True).json()['tracks']['data']

		for a in playlist_json:
			URL3 = self.api_track % str(a['id'])

			try:
				detas = utils.tracking(URL3)
				datas.append(detas)
			except exceptions.NoDataApi:
				datas.append(None)

		details = {
			"datas": datas,
			"quality": quality,
			"output": output
		}

		names, zip_name = self.download(
			URL2, details,
			recursive_quality,
			recursive_download,
			not_interface, zips
		)

		if zips:
			return names, zip_name

		return names

	def download_trackspo(
		self, URL,
		output = stock_output,
		quality = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface
	):
		URL = URL.split("?")[0]

		try:
			url = self.spo.track(URL)
		except Exception as a:
			if not "The access token expired" in str(a):
				raise exceptions.InvalidLink("Invalid link ;)")

			self.spo = Spotify(
				utils.generate_token()
			)

			url = self.spo.track(URL)

		isrc = "isrc:%s" % url['external_ids']['isrc']

		url = utils.request(
				self.api_track % isrc, True
		).json()

		name = self.download_trackdee(
			url['link'], output,
			quality, recursive_quality,
			recursive_download, not_interface
		)

		return name

	def download_albumspo(
		self, URL,
		output = stock_output,
		quality = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		zips = stock_zip
	):
		URL = URL.split("?")[0]

		try:
			tracks = self.spo.album(URL)
		except Exception as a:
			if not "The access token expired" in str(a):
				raise exceptions.InvalidLink("Invalid link ;)")

			self.spo = Spotify(
				utils.generate_token()
			)

			tracks = self.spo.album(URL)

		try:
			upc = "0%s" % tracks['external_ids']['upc']

			while upc[0] == "0":
				upc = upc[1:]

				try:
					upc = "upc:%s" % upc
					url = utils.request(self.api_album % upc, True).json()

					names = self.download_albumdee(
						url['link'], output,
						quality, recursive_quality,
						recursive_download, not_interface, zips
					)

					break
				except exceptions.NoDataApi:
					if upc[0] != "0":
						raise KeyError
		except KeyError:
			tot = tracks['total_tracks']

			for a in tracks['tracks']['items']:
				try:
					isrc = self.spo.track(
						a['external_urls']['spotify']
					)['external_ids']['isrc']
				except:
					self.spo = Spotify(
						utils.generate_token()
					)

					isrc = self.spo.track(
						a['external_urls']['spotify']
					)['external_ids']['isrc']

				try:
					isrc = "isrc:%s" % isrc

					ids = utils.request(
						self.api_track % isrc, True
					).json()['album']['id']

					tracks = utils.request(
						self.api_album % str(ids), True
					).json()

					if tot == tracks['nb_tracks']:
						break
				except exceptions.NoDataApi:
					pass

			try:
				if tot != tracks['nb_tracks']:
					raise KeyError

				names = self.download_albumdee(
					tracks['link'], output,
					quality, recursive_quality,
					recursive_download, not_interface, zips
				)
			except KeyError:
				raise exceptions.AlbumNotFound("Album not found :(")

		return names

	def download_playlistspo(
		self, URL,
		output = stock_output,
		quality = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface,
		zips = stock_zip
	):
		array = []

		URL = (
			URL
			.split("?")[0]
			.split("/")
		)

		try:
			tracks = self.spo.user_playlist_tracks(URL[-3], URL[-1])
		except Exception as a:
			if not "The access token expired" in str(a):
				raise exceptions.InvalidLink("Invalid link ;)")

			self.spo = Spotify(
				utils.generate_token()
			)

			tracks = self.spo.user_playlist_tracks(URL[-3], URL[-1])

		def lazy(tracks):
			for a in tracks['items']:
				try:
					array.append(
						self.download_trackspo(
							a['track']['external_urls']['spotify'],
							output, quality,
							recursive_quality, recursive_download, not_interface
						)
					)
				except:
					print("Track not found :(")
					array.append("None")

		lazy(tracks)
		tot = tracks['total']

		for a in range(tot // 100 - 1):
			try:
				tracks = self.spo.next(tracks)
			except:
				self.spo = Spotify(
					utils.generate_token()
				)

				tracks = self.spo.next(tracks)

			lazy(tracks)

		if zips:
			zip_name = "{}playlist {}.zip".format(output, URL[-1])			
			utils.create_zip(zip_name, array)
			return array, zip_name

		return array

	def download_name(
		self, artist, song,
		output = stock_output,
		quality = stock_quality,
		recursive_quality = stock_recursive_quality,
		recursive_download = stock_recursive_download,
		not_interface = stock_not_interface
	):
		query = "track:{} artist:{}".format(song, artist)

		try:
			search = self.spo.search(query)
		except:
			self.spo = Spotify(
				utils.generate_token()
			)

			search = self.spo.search(query)

		try:
			return self.download_trackspo(
				search['tracks']['items'][0]['external_urls']['spotify'],
				output, quality, recursive_quality,
				recursive_download, not_interface
			)
		except IndexError:
			raise exceptions.TrackNotFound("Track not found: :(")