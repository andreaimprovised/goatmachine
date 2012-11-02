#!/usr/bin/python
import json
import os
import sqlite3

import common

default = lambda key, row: (key, row[key])
to_bool = lambda key, row: (key, bool(row[key]))


class CookieNotFoundError(Exception):
	pass


class GXCookieExtractorMeta(type):

	cookie_extractor_classes = []

	def __init__(
			cls,
			class_name,
			base_classes,
			class_dict
	):
		super(GXCookieExtractorMeta, cls).__init__(
			class_name,
			base_classes,
			class_dict
		)
		if cls.keys_remap is not None:
			cls.cookie_extractor_classes.append(cls)

	@classmethod
	def get_gx_cookie(cls):
		for extractor_class in cls.cookie_extractor_classes:
			try:
				return extractor_class().get_gx_cookie()
			except CookieNotFoundError:
				pass
		raise CookieNotFoundError()


class GXCookieExtractor(object):

	__metaclass__ = GXCookieExtractorMeta

	keys_remap = None
	table_name = None

	def __init__(self, *args, **kwargs):
		self.connection = sqlite3.connect(self.cookies_path)
		self.connection.row_factory = sqlite3.Row


	@property
	def cookies_path(self):
		raise NotImplementedError()

	def get_gx_cookie_dictionary(self, table_name):
		cookie_dictionary = self.connection.cursor().execute(
			"SELECT * from %s WHERE name = 'GX'" % (table_name,)
		).fetchone()
		if cookie_dictionary:
			return cookie_dictionary
		raise CookieNotFoundError()

	def get_gx_cookie_from_row(self, keys_remap, row):
		return dict(
			remap_function(key, row)
			for key, remap_function in keys_remap.iteritems()
		)

	def get_gx_cookie(self):
		return self.get_gx_cookie_from_row(
			self.keys_remap,
			self.get_gx_cookie_dictionary(self.table_name),
		)


class ChromeGXCookieExtractor(GXCookieExtractor):

	table_name = 'cookies'
	keys_remap = {
		'name': default,
		'value': default,
		'path': default,
		'host_key': lambda key, row: ('domain', row[key][1:]),
		'expires_utc': lambda key, row: ('expiry', row[key])
	}

	@property
	def cookies_path(self):
		return os.path.expanduser(
			os.path.join(
				'~',
				'Library',
				'Application Support',
				'Google',
				'Chrome',
				'Default',
				'Cookies'
			)
		)


class FirefoxGXCookieExtractor(GXCookieExtractor):

	table_name = 'moz_cookies'
	keys_remap = {
		'name': default,
		'value': default,
		'path': default,
		'host': lambda key, row: ('domain', row[key][1:]),
		'expiry': default
	}


	@property
	def cookies_path(self):
		return os.path.join(
			common.get_firefox_profile_path(),
			'cookies.sqlite'
		)

	@property
	def session_cookies_path(self):
		return os.path.join(
			common.get_firefox_profile_path(),
			'sessionstore.js'
		)

	def get_gx_cookie_dictionary(self, table_name):
		try:
			return super(
				FirefoxGXCookieExtractor,
				self
			).get_gx_cookie_dictionary(table_name)
		except CookieNotFoundError:
			with open(self.session_cookies_path) as file:
				cookies_dump = json.load(file)
			for window in cookies_dump['windows']:
				for cookie in window['cookies']:
					if cookie['name'] == 'GX':
						return cookie
			raise

if __name__ == '__main__':
	print FirefoxGXCookieExtractor().get_gx_cookie()
