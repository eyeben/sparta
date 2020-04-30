import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('http://spartacodingclub.shop/homework')
#a=driver.find_elements_by_css_selector('#powerbbsBody > table > tbody > tr > td > div > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > form > table > tbody')
a=driver.find_elements_by_css_selector('html')

print('(',a,')')

