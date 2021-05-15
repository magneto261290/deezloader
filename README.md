# deezloader

This project has been created to download songs, albums or playlists with Spotify or Deezer link from Deezer.

# Disclaimer

- I am not responsible for the usage of this program by other people.
- I do not recommend you doing this illegally or against Deezer's terms of service.
- This project is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- The css and the js code haven't been coded by me, all thanks go to Shayan (https://codepen.io/shayanea/pen/yvvjya)

* ### OS Supported ###
	![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg)
	![macOS Support](https://img.shields.io/badge/macOS-Support-brightgreen.svg)
	![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)

* ### Installation ###
	pip3 install deezloader

# CLI interface

Finally **deez-dw** avalaible ;)
```bash
$ deez-dw -h
```
	usage: deez-dw [-h] [-l LINK] [-s SONG] [-a ARTIST] [-o OUTPUT]
                     [-q QUALITY] [-rq RECURSIVE_QUALITY]
                     [-rd RECURSIVE_DOWNLOAD] [-g NOT_GUI] [-z ZIP]
                     setting

## OPTIONS
	-h, --help            show this help message and exit
  	-l LINK, --link LINK  Deezer or Spotify link for download
  	-s SONG, --song SONG  song name
  	-a ARTIST, --artist ARTIST
                       	artist song
  	-o OUTPUT, --output OUTPUT
                        Output folder
  	-q QUALITY, --quality QUALITY
                        Select download quality between FLAC, 320, 256, 128
  	-rq RECURSIVE_QUALITY, --recursive_quality RECURSIVE_QUALITY
                        If choosen quality doesn't exist download with best
                        possible quality (True or False)
  	-rd RECURSIVE_DOWNLOAD, --recursive_download RECURSIVE_DOWNLOAD
                        If the song has already downloaded skip (True or
                        False)
  	-g NOT_GUI, --not_gui NOT_GUI
                        Show the little not_gui (True or False)
  	-z ZIP, --zip ZIP     If is an album or playlist link create a zip archive
                        (True or False)

# WEB interface

Finally **deez-web** avalaible ;)
```bash
$ deez-web
```

## SETTING
	[login]
	token = deezer_arl_token

setting.ini file for use deez-dw and deez-web

# Library

### Initialize

```python
import deezloader

downloa = deezloader.Login("YOUR ARL TOKEN DEEZER")
#how get arl token https://www.youtube.com/watch?v=pWcG9T3WyYQ the video is not mine
```

### Download song

Download track by Spotify link

```python
downloa.download_trackspo(
	"Insert the Spotify link of the track to download",
	output = "SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality = "MP3_320",
	recursive_quality = False,
	recursive_download = False
	not_interface = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality=True if selected quality isn't avalaible download with best quality possible
#recursive_download=True if song has already been downloaded don't ask for download it again
#not_interface=False if you want too see no download progress
```

Download track by Deezer link
```python
downloa.download_trackdee(
	"Insert the Spotify link of the track to download",
	output = "SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality = "MP3_320",
	recursive_quality = False,
	recursive_download = False
	not_interface = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
```

### Download album
Download album by Spotify link
```python
downloa.download_albumspo(
	"Insert the Spotify link of the album to download",
	output = "SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

Download album from Deezer link
```python
downloa.download_albumdee(
	"Insert the Spotify link of the album to download",
	output = "SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

### Download playlist

Download playlist by Spotify link
```python
downloa.download_playlistspo(
	"Insert the Spotify link of the album to download",
	output = "SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

Download playlist from Deezer link
```python
downloa.download_playlistdee(
	"Insert the Spotify link of the album to download",
	output = "SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality = "MP3_320",
	recursive_quality = True,
	recursive_download = True,
	not_interface = False,
	zips = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#zips = True create a zip with all album songs
```

### Download name

Download by name
```python
downloa.download_name(
	artist = "Eminem",
	song = "Berzerk",
	output = "SELECT THE PATH WHERE SAVE YOUR SONGS",
	quality = "MP3_320",
	recursive_quality = False,
	recursive_download = False,
	not_interface = False
)
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
```