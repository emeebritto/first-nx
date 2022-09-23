from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Binomo:
	def __init__(self):
		super(Binomo, self).__init__()


	def _detect_noRobot_box(self):
		pass


	def _createLog(self, msg):
		logger.fullog(msg)


	def openChart(self):
		self._createLog("Browser -> getting aplication web.")
		self.instance.get('https://binomo.com/trading')
		sleep(8)
		self.send_screen_to_author()

		self._createLog("Browser -> insering account login.")
		mail_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-text")
		mail_input = mail_input_wrapper.find_element(By.TAG_NAME, "input")
		password_input_wrapper = self.instance.find_element(By.TAG_NAME, "vui-input-password")
		password_input = password_input_wrapper.find_element(By.TAG_NAME, "input")
		mail_input.send_keys("emersonbritto987@gmail.com")
		password_input.send_keys(r"y1q8uw2a")
		password_input.send_keys(Keys.ENTER)

		self._createLog("Browser -> sleeping.")
		sleep(5)

		self.send_screen_to_author()
		bot_was_detected = self._detect_noRobot_box()
		if bot_was_detected: self.passCaptcha(targetNode=bot_was_detected)
		else: logger.fullog("bot wasn't detected")

		sleep(60)
		self._createLog("Browser -> selecting assets box.")

		assets_tab_wrapper = self.instance.find_element(By.TAG_NAME, "vui-asset-tab")
		assets_tab = assets_tab_wrapper.find_element(By.TAG_NAME, "button")
		assets_tab.click()

		self._createLog("Browser -> sleeping.")
		sleep(4)

		self._createLog("Browser -> selecting asset (EUR/USD).")

		assets_block = self.instance.find_element(By.TAG_NAME, "assets-block")
		asset_search_wrapper = assets_block.find_element(By.TAG_NAME, "asset-search")
		asset_search = asset_search_wrapper.find_element(By.TAG_NAME, "input")
		asset_search.send_keys("EUR/USD")

		self._createLog("Browser -> sleeping.")
		sleep(4)

		assets_result_wrapper = assets_block.find_element(By.TAG_NAME, "lib-platform-scroll")
		asset_body = assets_result_wrapper.find_element(By.CLASS_NAME, "asset-body")
		target_asset = asset_body.find_element(By.CLASS_NAME, "asset-row")
		target_asset.click()

		self._createLog("Browser -> sleeping.")
		sleep(4)

		self._createLog("Browser -> selecting chart time.")

		chart_settings = self.instance.find_element(By.TAG_NAME, "chart-settings")
		chart_Time_Button = chart_settings.find_element(By.ID, "qa_chartTimeButton")
		chart_Time_Button.click()

		sleep(4)

		time_period = self.instance.find_element(By.TAG_NAME, "time-period")
		fiveMChartTime = time_period.find_element(By.ID, "qa_5mChartTime")
		fiveMChartTime.click()

		self._createLog("Browser -> chart ready.")
		sleep(2)


	def purchase(self):
		dealUpButton = self.instance.find_element(By.ID, "qa_trading_dealUpButton")
		dealUpButton.click()
		self.send_msg_to_author("deal up button was clicked")
		self.send_screen_to_author()


	def sell(self):
		dealDownButton = self.instance.find_element(By.ID, "qa_trading_dealDownButton")
		dealDownButton.click()
		self.send_msg_to_author("deal down button was clicked")
		self.send_screen_to_author()


	def chart_price_screenshot(self):
		try:
			app_chart = self.instance.find_element(By.TAG_NAME, "app-chart")
		except Exception as e:
			print("chart not found")
			sleep(1)
			return None

		app_chart.screenshot('app_chart.png')
		img = Image.open('app_chart.png')
		w, h = img.size
		# (left, upper, right, lower)
		cropped_img = img.crop((int(w / 1.275), 0, w, h))
		return cropped_img


	def send_screen_to_author(self):
		pass


	def take_screenshot(self):
		pass


	def send_msg_to_author(self, msg):
		pass
