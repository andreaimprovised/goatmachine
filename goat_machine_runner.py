import os
import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


def get_os_x_firefox_driver():
	profiles_path = os.path.join(os.environ.get("HOME"), "Library/Application Support/Firefox/Profiles/")

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


class GoatMachineRunner(object):

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

		self._access_picture_dialog()

		self._insert_picture_dialog()

		self._click_send_button()

	def _access_picture_dialog(self):
		if self._is_new_version():
			# The insert pics button is only visible when hovering over the + button.
			# Hover over insert things "+" symbol, then click on the insert pic button
			webdriver.ActionChains(self.driver).move_to_element(self.driver.find_element_by_id(":qb")).perform()
			insert_pic_but = self.driver.find_element_by_id(":nk")
			self.wait_until_displayed(insert_pic_but)
			insert_pic_but.click()
		else:
			try:
				insert_pic_but = self.driver.find_element_by_xpath("//div[@command=\"image\"]")
				insert_pic_but.click()
			except NoSuchElementException:
				# Doesn't have image inline plugin
				# Put the url inline
				self.driver.find_element_by_id(":q0").send_keys(self.goat_url)

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


if __name__ == "__main__":

	to = "phyrexian000@gmail.com"

	su = "goats galore from selenium"

	goat_url = "http://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hausziege_04.jpg/256px-Hausziege_04.jpg"

	ff = get_os_x_firefox_driver()

	GoatMachineRunner(ff, to, su, goat_url, dry_run=True).post_goat_mail()

	ff.quit()
