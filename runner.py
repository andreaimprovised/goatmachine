#!/usr/bin/python
import gx_cookie_extractor
# import image_fetcher
import goat_machine


if __name__ == "__main__":
	to = "goats@gmail.com"
	su = "selenium goat"
	# image_fetcher.GoatSearcher("selenium goat")
	# goat_url = image_fetch.get_my_goat_image()
	goat_url = "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hausziege_04.jpg/256px-Hausziege_04.jpg"
	cookie = gx_cookie_extractor.GXCookieExtractorMeta.get_gx_cookie()
	firefox_driver = goat_machine.get_firefox_driver_with_cookie(cookie)
	goat_machine.GoatMachine(firefox_driver, to, su, goat_url, dry_run=True).post_goat_mail()
	firefox_driver.quit()
