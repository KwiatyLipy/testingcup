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

def check_element(driver, how, what, error_exp_text, tekst): 
	try:
		element = driver.find_element(how, what)
	except NoSuchElementException as error:
		screenshot(driver, tekst)
		print(error_exp_text + " \r\n %s" % error)
	return element

def assertion(driver, what, withwhat, error_text, tekst): 
	try:
		assert what.text == withwhat
	except AssertionError as error:
		screenshot(driver, tekst)
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb) # Fixed format
		tb_info = traceback.extract_tb(tb)
		filename, line, func, text = tb_info[-1]
		print(error_text + "\r\n")
		print('An error occurred on line {} in statement {}'.format(line, text))
	return 

def screenshot(driver, tekst):
	screen = self.path + "\\" + tekst + str(self.scr) + '.png'
	self.scr = self.scr + 1
	self.save_screenshot(screen)
	return 