#!/usr/bin/python3

api_link = "https://api.deezer.com/"
api_track = "{}track/%s".format(api_link)
api_album = "{}album/%s".format(api_link)
api_playlist = "{}playlist/%s".format(api_link)
api_search_trk = "{}search/track/?q=%s".format(api_link)
private_api_link = "https://www.deezer.com/ajax/gw-light.php"
songs_server = "https://e-cdns-proxy-{}.dzcdn.net/mobile/1/{}"
cover = "https://e-cdns-images.dzcdn.net/images/cover/%s/1200x1200-000000-80-0-0.jpg"

header = {
	"Accept-Language": "en-US,en;q=0.5"
}

qualities = {
	"FLAC": {
		"n_quality": "9",
		"f_format": ".flac",
		"s_quality": "FLAC"
	},

	"MP3_320": {
		"n_quality": "3",
		"f_format": ".mp3",
		"s_quality": "320"
	},

	"MP3_256": {
		"n_quality": "5",
		"f_format": ".mp3",
		"s_quality": "256"
	},

	"MP3_128": {
		"n_quality": "1",
		"f_format": ".mp3",
		"s_quality": "128"
	}
}