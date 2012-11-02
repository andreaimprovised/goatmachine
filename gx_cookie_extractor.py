#!/usr/bin/python
import os
import sqlite3

default = lambda key, row: (key, row[key])
to_bool = lambda key, row: (key, bool(row[key]))

class GXCookieExtractor(object):

	keys_remap = None
	table_name = None

	def __init__(self, *args, **kwargs):
		self.connection = sqlite3.connect(self.cookies_path)
		self.connection.row_factory = sqlite3.Row


	@property
	def cookies_path(self):
		raise NotImplementedError()

	def get_gx_cookie_dictionary(self, table_name):
		return self.connection.cursor().execute(
			"SELECT * from %s WHERE name = 'GX'" %(table_name,)
		).fetchone()

	def get_gx_cookie_from_row(self, keys_remap, row):
		return dict(
			remap_function(key, row)
			for key, remap_function in keys_remap.iteritems()
		)

	def get_gx_cookie(self):
		return self.get_gx_cookie_from_row(
			self.keys_remap,
			self.get_gx_cookie_dictionary('cookies'),
		)


class ChromeGXCookieExtractor(GXCookieExtractor):

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


if __name__ == '__main__':
	print ChromeGXCookieExtractor().get_gx_cookie()
