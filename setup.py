from setuptools import setup

setup(
	name = "deezloader",
	version = "2020.11.26",
	description = "Downloads songs, albums or playlists from deezer",
	license = "CC BY-NC-SA 4.0",
	author = "An0nimia",
	author_email = "An0nimia@protonmail.com",
	url = "https://github.com/An0nimia/deezloader",
	packages = ["deezloader"],
	install_requires = ["Flask", "flask-cors", "stagger", "mutagen", "pycryptodome", "requests", "spotipy", "tqdm"],
	scripts = ["deezloader/bin/deez-dw.py", "deezloader/bin/deez-web.py"]
)