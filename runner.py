import chrome_cookie_extracter
import goat_machine


if __name__ == "__main__":
	to = "goats@gmail.com"
	su = "selenium goat"
	goat_url = "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hausziege_04.jpg/256px-Hausziege_04.jpg"
	cookie = chrome_cookie_extracter.ChromeCookieExtracter().get_gx_cookie()
	firefox_driver = goat_machine.get_firefox_driver_with_cookie(cookie)
	goat_machine.GoatMachine(firefox_driver, to, su, goat_url, dry_run=True).post_goat_mail()
	firefox_driver.quit()
