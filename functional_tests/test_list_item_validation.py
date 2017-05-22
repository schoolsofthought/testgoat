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
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)


		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# She tries again with some text for the item, which now works
		self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		#Perversely, she now decides to submit a second blank list item
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		
		# She receives a similar warning on the list page
		self.wait_for(lambda:self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# And she can correct it by filling some tect in
		self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
		self.browser.find_element_by_id('id_new_item')/send_keys(Keys.ENTER)
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

