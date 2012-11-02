#!/usr/bin/python
"""
python runner.py "your query here"
"""
import sys

from selenium import webdriver

import image_fetcher
import gx_cookie_extractor
import goat_machine


if __name__ == "__main__":
	try:
		query = sys.argv[1]
		goat_url = image_fetcher.GoatSearcher(query).get_my_goat_image()
	except IndexError:
		goat_url = "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hausziege_04.jpg/256px-Hausziege_04.jpg"

	to = "goats@gmail.com"
	su = "selenium goat"

	firefox_driver = webdriver.Firefox()
	goater = goat_machine.GoatMachine(firefox_driver, to, su, goat_url, dry_run=True)

	firefox_driver.get("http://mail.google.com/goatingyourightnow")

	for cookie in gx_cookie_extractor.GXCookieExtractorMeta.yield_gx_cookies():
		firefox_driver.add_cookie(cookie)
		try:
			goater.post_goat_mail()
			break
		except goat_machine.WrongDomainError:
			firefox_driver.delete_all_cookies()

	firefox_driver.quit()
