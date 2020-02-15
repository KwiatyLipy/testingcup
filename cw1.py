#! python3

import unittest, time, sys, traceback
from time import gmtime, strftime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

class PythonOrgSearch(unittest.TestCase):

	scr=0
	folder = strftime("%Y-%m-%d %H.%M.%S", gmtime()) 
	path = r"C:\Users\Justyna\Desktop\Python" + "\\" + folder
	Path(path).mkdir(parents=True, exist_ok=True)

	def setUp(self):
    	#driver = webdriver.Firefox()
    	#driver = webdriver.Ie(r'C:\Users\Justyna\Desktop\Python\Drivers\MicrosoftWebDriver.exe')
		#driver = webdriver.Chrome(r'C:\Users\Justyna\Desktop\Python\chromedriver.exe')
		#driver = webdriver.Chrome()
		self.driver = webdriver.Remote(command_executor='http://185.238.75.153:22/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)

	def tearDown(self):
		self.screenshot("end")
		self.driver.close()

	def test_search_in_python_org(self):
		driver = self.driver
		driver.get("https://testingcup.pgs-soft.com/task_1")
		tekst = "test"
		ilosc = 0
		suma = 0.00
		Basket = []
		quantityAll = self.check_element(By.CLASS_NAME, 'summary-quantity', "Lack of quantity in basket", tekst)
		self.assertion(quantityAll, str(ilosc), "Incorrect quantity in basket", tekst)
		priceAll = self.check_element(By.CLASS_NAME, 'summary-price', "Lack of price in basket", tekst)
		self.assertion(priceAll, str("{0:.2f}".format(suma)) + ' zł', "Incorrect price in basket", tekst)
		for y in range(1,4):
			for x in range(1,5):
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/h4"
				Item = self.check_element(By.XPATH, pathX, "Lack of name for item", tekst)
				Basket.append(Item)
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/p[1]"
				Item = self.check_element(By.XPATH, pathX, "Lack of price in basket", tekst).text
				price = Item.split(' ')
				price = float(price[1])
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/div/input"
				Item = self.check_element(By.XPATH, pathX, "Lack of option to add item", tekst)
				Item.clear()
				Item.send_keys('1') 
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/div/span/button"
				Item = self.check_element(By.XPATH, pathX, "Lack of option to add item", tekst)
				Item.click() 
				ilosc =  ilosc + 1
				suma = suma + price 
				self.assertion(quantityAll, str(ilosc), "Incorrect quantity in basket", tekst) 
				self.assertion(priceAll, str("{0:.2f}".format(suma)) + ' zł', "Incorrect price in basket", tekst)
				pathX = "//div[2]/div/div[2]/div[1]/div["+ str(ilosc) +"]/div[1]" 
				Item = self.check_element(By.XPATH, pathX, "Lack of item in basket", tekst).text 
				name = Item.split(' ')
				self.assertion(Basket[ilosc-1], name[0], "Incorrect item in basket", tekst)
				pass
			pass


	def check_element(self, how, what, error_exp_text, tekst):
		driver = self.driver
		try:
			element = driver.find_element(how, what)
		except NoSuchElementException as error:
			self.screenshot(tekst)
			print(error_exp_text + " \r\n %s" % error)
		return element

	def assertion(self, what, withwhat, error_text, tekst):
		driver = self.driver
		try:
			assert what.text == withwhat
		except AssertionError as error:
			self.screenshot(tekst)
			_, _, tb = sys.exc_info()
			traceback.print_tb(tb) # Fixed format
			tb_info = traceback.extract_tb(tb)
			filename, line, func, text = tb_info[-1]
			print(error_text + "\r\n")
			print('An error occurred on line {} in statement {}'.format(line, text))
		return

	def screenshot(self, tekst):
		screen = self.path + "\\" + tekst + str(self.scr) + '.png'
		self.scr = self.scr + 1
		self.driver.save_screenshot(screen)
		return


def suite():
	suite = unittest.TestSuite()

	suite.addTest(PythonOrgSearch("test_search_in_python_org")) 

	return suite

if __name__== "__main__":
	runner = unittest.TextTestRunner()
	test_suite = suite()
	runner.run (test_suite)
	#unittest.main()