#!/usr/bin/python
import json
import os
import sqlite3

import common

default = lambda key, row: (key, row[key])
to_bool = lambda key, row: (key, bool(row[key]))


class CookieNotFoundError(Exception):
	pass

class NoMoreCookiesError(Exception):
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
	def yield_gx_cookies(cls):
		for extractor_class in cls.cookie_extractor_classes:
			try:
				for cookie in extractor_class().get_gx_cookie():
					yield cookie
			except (CookieNotFoundError, sqlite3.OperationalError):
				pass


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

	def get_gx_cookie_dictionaries(self, table_name):
		cookie_dictionaries = self.connection.cursor().execute(
			"SELECT * from %s WHERE name = 'GX'" % (table_name,)
		)
		for cookie in cookie_dictionaries:
			yield cookie

	def get_gx_cookie_from_row(self, keys_remap, row):
		return dict(
			remap_function(key, row)
			for key, remap_function in keys_remap.iteritems()
		)

	def get_gx_cookie(self):
		for cookie in self.get_gx_cookie_dictionaries(self.table_name):
			yield self.get_gx_cookie_from_row(
				self.keys_remap,
				cookie
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

	def get_gx_cookie_dictionaries(self, table_name):
		for cookie in super(
			FirefoxGXCookieExtractor,
			self
		).get_gx_cookie_dictionaries(table_name):
			yield cookie
		with open(self.session_cookies_path) as file:
			cookies_dump = json.load(file)
		for window in cookies_dump['windows']:
			for cookie in window['cookies']:
				if cookie['name'] == 'GX':
					yield cookie

if __name__ == '__main__':
	for cookie in GXCookieExtractorMeta.yield_gx_cookies():
		print cookie
