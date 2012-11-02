#!/usr/bin/python
"""
python runner.py "your query here"
"""
import sys

from selenium import webdriver

import config
import image_fetcher
import gx_cookie_extractor
import goat_machine


if __name__ == "__main__":
	try:
		query = sys.argv[1]
		goat_url = image_fetcher.GoatSearcher(query).get_my_goat_image()
	except IndexError:
		goat_url = config.DEFAULT_GOAT_URL
		query = "You got goated sucka!"

	to = config.GOAT_EMAIL_LIST
	su = query

	driver = webdriver.Firefox()

	goater = goat_machine.GoatMachine(driver, to, su, goat_url)

	for cookie in gx_cookie_extractor.GXCookieExtractorMeta.yield_gx_cookies():
		try:
			goater.post_goat_mail(cookie)
			break
		except goat_machine.BadCookieError:
			pass

	driver.quit()
