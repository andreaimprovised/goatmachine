#!/usr/bin/python
"""
python runner.py "your query here"
"""
import sys

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
	cookie = gx_cookie_extractor.GXCookieExtractorMeta.get_gx_cookie()
	firefox_driver = goat_machine.get_firefox_driver_with_cookie(cookie)
	goat_machine.GoatMachine(firefox_driver, to, su, goat_url, dry_run=True).post_goat_mail()
	firefox_driver.quit()
