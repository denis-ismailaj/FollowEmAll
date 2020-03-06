from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException
from time import sleep, strftime
import os.path
import pickle


class FollowEmAll(object):
	def __init__(self):
		self.db, self.count = self.load()

	def add_user(self, username):
		if username not in self.db:
			self.db.append(username)

	@staticmethod
	def load():
		if os.path.isfile("database.pickle"):
			try:
				with open('database.pickle', 'rb') as handle:
					a = pickle.load(handle)
				return a, len(a)

			except EOFError:
				return [], 0
		else:
			return [], 0

	def save(self):
		print(self.db)
		with open('database.pickle', 'wb') as handle:
			pickle.dump(self.db, handle)

	def terminate(self, driver):
		self.save()
		driver.close()
		print("Terminated at {} ({} new follows)".format(strftime("%H:%M"), len(self.db) - self.count))

	def start(self):

		print(self.db)

		driver = webdriver.Firefox()
		driver.get("https://www.instagram.com/accounts/login/")

		sleep(1)

		driver.find_element_by_name("username").send_keys("username")
		driver.find_element_by_name("password").send_keys("password")

		driver.find_element_by_xpath(
			'//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button').submit()

		sleep(2)

		driver.get("https://www.instagram.com/instagram/")

		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a').click()

		sleep(2)

		index = 1

		while True:
			try:
				while True:
					username = driver.execute_script("return arguments[0].innerText;", driver.find_element_by_xpath(
						'/html/body/div[2]/div/div[2]/div/div[2]/ul/li[{}]/div/div[1]/div/div[1]/a'.format(index)))
					button = driver.find_element_by_xpath(
						'/html/body/div[2]/div/div[2]/div/div[2]/ul/li[{}]/div/div[2]/span/button'.format(index))
					if driver.execute_script("return arguments[0].innerText;", button) == "Follow" and username not in self.db:
						button.click()
						sleep(0.6)
						if not button.is_enabled() or driver.execute_script("return arguments[0].innerText;", button) != "Follow":
							self.add_user(username)
						else:
							print("case 1")
							print(username)
							self.terminate(driver)
							return
					else:
						self.add_user(username)

					index += 1
					print(index)
					print(self.db[len(self.db) - 1])
			except (StaleElementReferenceException, NoSuchElementException):
				sleep(1.5)
			except (WebDriverException, KeyboardInterrupt) as e:
				print(e)
				print("case 2")
				self.terminate(driver)


instance = FollowEmAll()
instance.start()
sleep(3600)
