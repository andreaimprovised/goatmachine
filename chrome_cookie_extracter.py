#!/usr/bin/python
import os
import sqlite3

class ChromeCookieExtracter(object):

	def __init__(self, *args, **kwargs):
		sqlite3.connect(self.chrome_cookies_path)
		

	@property
	def chrome_cookies_path(self):
		return os.path.join('~','Library', 'Application Support', 'Google', 'Chrome', 'Default', 'Cookies')

if __name__ == '__main__':
	ChromeCookieExtracter()
