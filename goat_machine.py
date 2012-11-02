import itertools

from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import config


class WrongDomainError(Exception):
	pass


class GoatMachine(object):

	def __init__(self, driver, to, su, goat_url):
		self.driver = driver
		self.to = to
		self.su = su
		self.goat_url = goat_url

	def wait_until_displayed(self, target, timeout=1):
		WebDriverWait(self.driver, timeout).until(lambda _: target.is_displayed())

	def wait_until_enabled(self, target, timeout=1):
		WebDriverWait(self.driver, timeout).until(lambda _: target.is_enabled())

	def post_goat_mail(self):
		# This page is so AJAX-y, that at "onload", most things aren't around
		# This polls for 1 second on each "find" operation if it initially fails
		self.driver.implicitly_wait(1)

		self._open_compose_page()

		self._insert_picture()

		self._click_send_button()

	def _open_compose_page(self):
	# Iterate through their potential open email accounts
		for i in itertools.count():
			self.driver.get("https://mail.google.com/mail/u/{i}/?view=cm&tf=0&to={to}&su={su}".format(
					i=i, # account number (0 is default)
					to=self.to, # destination email address
					su=self.su, # subject of message
				)
			)

			try:
				app_name_element = self.driver.find_element_by_name("application-name")
			except NoSuchElementException as e:
				raise WrongDomainError
			else:
				if config.DOMAIN.lower() in app_name_element.get_attribute("content").lower():
					return

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

	def _click_send_button(self):
		if not config.DRY_RUN:
			send_but = self.driver.find_element_by_id(":pl")
			self.wait_until_displayed(send_but)
			self.driver.find_element_by_id(":pl").click()
