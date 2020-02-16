import sys
import time
import os
import codecs
import re
from bs4 import BeautifulSoup as bs
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlencode
from pdb import set_trace as bp

class Co:

    def __init__(self, url):
        self.url = url

    def logIn(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.browser = webdriver.Chrome(chrome_options = options)
        self.log('logIn', 'completed')

    def getElement(self, by, name):
        try:
            return self.wait.until(EC.presence_of_element_located((by, name)))
        except:
            if self.debug:
                codecs.open('tmp/dump', 'w', encoding='utf-8').write(self.browser.page_source)
            raise

    def getJobs(self):
        self.browser.get(self.url + '/')
        self.wait = WebDriverWait(self.browser, timeout = 5) # seconds
        jobs = self.getElement(By.ID, 'jobs-list')
        soup = bs(self.browser.page_source, "html.parser")
        rows = soup.find('div', {'class': 'jobs list list-container'})
        if rows is not None:
            rows = rows.find_all('a')
        self.jobs = []
        pattern = {
                    'name': [
                                r'(\S.*\S)',
                                'title',
                            ],
                  }
        pattern = {
                    field: [
                              pattern[field][0],
                              pattern[field][1],
                              re.compile(pattern[field][0]),
                           ]
                    for field in pattern
                  }
        if rows is not None:
            for row in rows:
                cols =  {
                            field: row.find('h5', {'class': pattern[field][1]})
                                for field in pattern
                        }
                job =   {
                            field: pattern[field][2].search(cols[field].get_text())
                                for field in pattern
                        }
                job =   {
                            field: job[field].group(1)
                                for field in pattern
                                if job[field] is not None
                        }
                self.jobs.append(job)
        self.log('Jobs', self.jobs)
        return self.jobs

    def isElementExist(self, parent, locator):
        try:
            parent.find_element_by_xpath(locator)
        except NoSuchElementException:
            self.log('No such thing: {}'.format(locator))
            return False
        return True

    def Quit(self):
        self.browser.quit()

    def log(self, *args):
        if self.debug:
            print(args)
