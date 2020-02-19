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
from functions import *

class testingcup(unittest.TestCase):

	scr=0
	folder = strftime("%Y-%m-%d %H.%M.%S", gmtime()) 
	path = r"C:\Users\Justyna\Desktop\Python" + "\\" + folder
	Path(path).mkdir(parents=True, exist_ok=True)

	def setUp(self):
    	#self.driver = webdriver.Firefox()
    	#self.driver = webdriver.Ie(r'C:\Users\Justyna\Desktop\Python\Drivers\MicrosoftWebDriver.exe')
		self.driver = webdriver.Chrome(r'C:\Users\Justyna\Desktop\Python\chromedriver.exe')
		#self.driver = webdriver.Remote(command_executor='http://localhost:4444/',desired_capabilities=DesiredCapabilities.CHROME) 
		self.driver.implicitly_wait(10)
		self.driver.delete_all_cookies()
		self.driver.maximize_window() 

	def tearDown(self): 
		self.driver.close()

	def test(self):
		driver = self.driver
		driver.get("https://testingcup.pgs-soft.com/task_1")
		tekst = "test"
		ilosc = 0
		suma = 0.00
		Basket = []
		quantityAll = check_element(driver, By.CLASS_NAME, 'summary-quantity', "Lack of quantity in basket", tekst)
		assertion(driver, quantityAll, str(ilosc), "Incorrect quantity in basket", tekst)
		priceAll = check_element(driver, By.CLASS_NAME, 'summary-price', "Lack of price in basket", tekst)
		assertion(driver, priceAll, str("{0:.2f}".format(suma)) + ' zł', "Incorrect price in basket", tekst)
		for y in range(1,4):
			for x in range(1,5):
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/h4"
				Item = check_element(driver, By.XPATH, pathX, "Lack of name for item", tekst)
				Basket.append(Item)
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/p[1]"
				Item = check_element(driver, By.XPATH, pathX, "Lack of price in basket", tekst).text
				price = Item.split(' ')
				price = float(price[1])
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/div/input"
				Item = check_element(driver, By.XPATH, pathX, "Lack of option to add item", tekst)
				Item.clear()
				Item.send_keys('1') 
				pathX = "//form/div[" + str(y) + "]/div[" + str(x) + "]/div/div/div/span/button"
				Item = check_element(driver, By.XPATH, pathX, "Lack of option to add item", tekst)
				Item.click() 
				ilosc =  ilosc + 1
				suma = suma + price 
				assertion(driver, quantityAll, str(ilosc), "Incorrect quantity in basket", tekst) 
				assertion(driver, priceAll, str("{0:.2f}".format(suma)) + ' zł', "Incorrect price in basket", tekst)
				pathX = "//div[2]/div/div[2]/div[1]/div["+ str(ilosc) +"]/div[1]" 
				Item = check_element(driver, By.XPATH, pathX, "Lack of item in basket", tekst).text 
				name = Item.split(' ')
				assertion(driver, Basket[ilosc-1], name[0], "Incorrect item in basket", tekst)
				pass
			pass

def suite():
	suite = unittest.TestSuite()

	suite.addTest(testingcup("test")) 

	return suite

if __name__== "__main__":
	runner = unittest.TextTestRunner()
	test_suite = suite()
	runner.run (test_suite) 