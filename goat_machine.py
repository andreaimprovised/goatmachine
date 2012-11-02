import os
import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


OS_X_FF_PROFILE_ROOT = "Library/Application Support/Firefox/Profiles/"
LINUX_FF_PROIFLE_ROOT = ".mozilla/firefox/"


def get_firefox_driver_with_profile(root):
	profiles_path = os.path.join(os.environ.get("HOME"), root)

	uname = os.environ.get("USER")

	profile_path = None

	for path in os.listdir(profiles_path):
		if "default" in path:
			profile_path = path
			break
		elif uname in path:
			profile_path = path
			break

	if profile_path is None:
		raise LookupError("Could not find a profile for firefox!")

	ff_profile = webdriver.FirefoxProfile(os.path.join(profiles_path, profile_path))

	return webdriver.Firefox(firefox_profile=ff_profile)


def get_firefox_driver_with_cookie(cookie):
	firefox_driver = webdriver.Firefox()
	firefox_driver.get("http://mail.google.com/goatingyourightnow")
	firefox_driver.add_cookie(cookie)
	return firefox_driver


class GoatMachine(object):

	def __init__(self, driver, to, su, goat_url, dry_run=False):
		self.driver = driver
		self.to = to
		self.su = su
		self.goat_url = goat_url
		self.dry_run = dry_run

	def wait_until_displayed(self, target, timeout=1):
		try:
			WebDriverWait(self.driver, timeout).until(lambda _: target.is_displayed())
		except TimeoutException:
			import ipdb; ipdb.set_trace()
			self.driver.quit()
			sys.exit(-1)


	def wait_until_enabled(self, target, timeout=1):
		try:
			WebDriverWait(self.driver, timeout).until(lambda _: target.is_enabled())
		except TimeoutException:
			import ipdb; ipdb.set_trace()
			self.driver.quit()
			sys.exit(-1)

	def _is_new_version(self):
		# Look for that weird panel at the bottom of the page
		# if its there then its the new version
		try:
			self.driver.find_element_by_id(":qb")
		except NoSuchElementException:
			return False
		return True

	def post_goat_mail(self):
		# Automatically set the to and subject fields in the URL params"""
		self.driver.get("http://mail.google.com/mail?view=cm&tf=0&to={to}&su={su}".format(to=self.to, su=self.su))

		# This page is so AJAX-y, that at "onload", most things aren't around
		# This polls for 1 second on each "find" operation if it initially fails
		self.driver.implicitly_wait(1)

		self._insert_picture()

		self._click_send_button()

	def _insert_picture(self):
		#####################
		# gmail new compose #
		#####################

		try:
			# The insert pics button is only visible when hovering over the + button.
			# Hover over insert things "+" symbol, then click on the insert pic button
			webdriver.ActionChains(self.driver).move_to_element(self.driver.find_element_by_id(":qb")).perform()
			insert_pic_but = self.driver.find_element_by_id(":nk")
			self.wait_until_displayed(insert_pic_but)
			insert_pic_but.click()
			self._insert_picture_dialog()
			return
		except NoSuchElementException:
			pass

		self.driver.implicitly_wait(0)

		#####################
		# gmail old compose #
		#####################

		# if currently in plain text mode, switch to rich text
		mode_switch_span = self.driver.find_element_by_id(":py")
		if "Rich" in mode_switch_span.text:
			mode_switch_span.click()
			self.driver.implicitly_wait(1)

		# gmail old compose with labs insert inline picture plugin
		try:
			insert_pic_but = self.driver.find_element_by_xpath("//div[@command='image']")
			insert_pic_but.click()
			self._insert_picture_dialog()
			return
		except NoSuchElementException:
			pass

		# no inline picture support

		# Open the dialog box and insert the url
		self.driver.find_element_by_xpath("//div[@command='+link']").click()
		url_box = self.driver.find_element_by_id("linkdialog-onweb-tab-input")
		self.wait_until_displayed(url_box)
		url_box.send_keys(self.goat_url)

		# Wait until okay button is enabled and then click okay
		okay_but = self.driver.find_element_by_name("ok")
		self.wait_until_enabled(okay_but)
		okay_but.click()

		self.driver.implicitly_wait(1)

	def _insert_picture_dialog(self):
		"""Shared logic to going through the insert picture dialog"""
		# Click the user Web URL radio button
		radio_but = self.driver.find_element_by_id("tr_image-dialog-external-image-tab-dialog-radio")
		self.wait_until_displayed(radio_but)
		radio_but.click()

		# Type link for picture
		web_url_bar = self.driver.find_element_by_id("tr_image-dialog-external-image-input")
		self.wait_until_displayed(web_url_bar)
		web_url_bar.send_keys(self.goat_url)

		# Confirm insert picture
		okay_but = self.driver.find_element_by_name("ok")
		self.wait_until_enabled(okay_but)
		okay_but.click()

	def _insert_picture_dialog(self):
		"""Shared logic to going through the insert picture dialog"""
		# Click the user Web URL radio button
		radio_but = self.driver.find_element_by_id("tr_image-dialog-external-image-tab-dialog-radio")
		self.wait_until_displayed(radio_but)
		radio_but.click()

		# Type link for picture
		web_url_bar = self.driver.find_element_by_id("tr_image-dialog-external-image-input")
		self.wait_until_displayed(web_url_bar)
		web_url_bar.send_keys(self.goat_url)

		# Confirm insert picture
		okay_but = self.driver.find_element_by_name("ok")
		self.wait_until_enabled(okay_but)
		okay_but.click()

	def _click_send_button(self):
		if not self.dry_run:
			send_but = self.driver.find_element_by_id(":pl")
			self.wait_until_displayed(send_but)
			self.driver.find_element_by_id(":pl").click()
