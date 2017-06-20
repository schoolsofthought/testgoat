from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		#Edith goes to te home page and accidentally tries tos submit 
		#an empty list item. She hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# The browser intercepts the request, and does not load the list page
		self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

		# She starts typing some text for the new item and the error disappears
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))

		#and she can submit it successfully
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		#Perversely, she now decides to submit a second blank list item
		self.get_item_input_box().send_keys(Keys.ENTER)

		#again, the browser will not comply
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

		# And she can correct it by filling some tect in
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def wait_for(self, fn):
		start_time = time.time()
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

if __name__ == '__main__':
	unittest.main(warnings='ignore')

