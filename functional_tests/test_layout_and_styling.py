from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
	def test_layout_and_styling(self):
		#Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		inputbox = self.get_item_input_box()
		print(type(inputbox))
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

		# She notices the input box is nicely centered
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.get_item_input_box()
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

if __name__ == '__main__':
	unittest.main(warnings='ignore')

