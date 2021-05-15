#!/usr/bin/python3

class TrackNotFound(Exception):
	def __init__(self, message):
		super().__init__(message)

class AlbumNotFound(Exception):
	def __init__(self, message):
		super().__init__(message)

class InvalidLink(Exception):
	def __init__(self, message):
		super().__init__(message)

class QuotaExceeded(Exception):
	def __init__(self, message):
		super().__init__(message)

class QualityNotFound(Exception):
	def __init__(self, message):
		super().__init__(message)

class NoDataApi(Exception):
	def __init__(self, message):
		super().__init__(message)

class BadCredentials(Exception):
	def __init__(self, message):
		super().__init__(message)