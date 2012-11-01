#!/usr/bin/python
import os
import sqlite3

default = lambda key, row: (key, row[key])
to_bool = lambda key, row: (key, bool(row[key]))

class ChromeCookieExtracter(object):

	keys_remap = {
		'name': default,
		'value': default,
		'path': default,
		'host_key': lambda key, row: ('domain', row[key][1:]),
		'secure': to_bool,
		'expires_utc': lambda key, row: ('expiry', row[key])
	}

	def __init__(self, *args, **kwargs):
		self.connection = sqlite3.connect(self.chrome_cookies_path)
		self.connection.row_factory = sqlite3.Row


	@property
	def chrome_cookies_path(self):
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

	def get_gx_cookie_dictionary(self):
		return self.connection.cursor().execute(
			"SELECT * from cookies WHERE name = 'GX'"
		).fetchone()

	def get_gx_cookie(self):
		gx_cookie_row = self.get_gx_cookie_dictionary()
		return dict(
			remap_function(key, gx_cookie_row)
			for key, remap_function in self.keys_remap.iteritems()
		)

if __name__ == '__main__':
	print ChromeCookieExtracter().get_gx_cookie()
