import json
import urllib
import urllib2
import random

import config


class GoatSearcher(object):
	def __init__(self, search_term=None):
		self.search_term = search_term or "goat"
		self.random_image_number = random.randint(1, 50)

	def _build_search_url(self):
		params = urllib.urlencode(
			dict(
				key=config.API_KEY,
				cx=config.CX,
				searchType="image",
				start=self.random_image_number/config.RES_PER_REQUEST + 1,
				q=self.search_term,
				alt="json",
			),
		)
		return config.API_BASE_URL + '?' + params

	def _fetch_search_results(self):
		return urllib2.urlopen(self._build_search_url()).read()

	def get_my_goat_image(self):
		all_results = json.loads(self._fetch_search_results())
		my_image = all_results['items'][self.random_image_number % config.RES_PER_REQUEST]
		return my_image['link']
