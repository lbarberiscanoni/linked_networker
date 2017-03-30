from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
import sys
import time

username = sys.argv[1]
password = sys.argv[2]

class LinkedIn():

    def __init__(self, browser, username, password):
        self.browser = browser
        self.username = username
        self.password = password

    def login(self):
        self.browser.get("https://www.linkedin.com/uas/login")
        emailInpt = self.browser.find_element_by_id("session_key-login")
        emailInpt.send_keys(self.username)
        passInpt = self.browser.find_element_by_id("session_password-login")
        passInpt.send_keys(self.password)
        passInpt.submit()

    def scrollToBottom(self):
        for i in range(0, 50):
            self.browser.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(1)

    def network(self):
        self.browser.get("https://www.linkedin.com/people/pymk?trk=nav_responsive_sub_nav_pymk")
        self.scrollToBottom()
        connectionList = self.browser.find_elements_by_css_selector(".mn-person-info__picture.ember-view")
        urlList = [ card.get_attribute("href") for card in connectionList ]
        print len(connectionList), " connections found"
        while len(urlList) > 0:
            index = randint(0, len(urlList) - 1)
            url = urlList[index]
            urlList.pop(index)

            self.browser.execute_script("window.open('" + str(url) + "');")
            time.sleep(2)
            self.browser.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)

            handles = self.browser.window_handles
            self.browser.switch_to.window(handles[1])
            self.browser.execute_script("window.close();")
            self.browser.switch_to.window(handles[0])

    def run(self):
        self.login()
        time.sleep(2)
        self.network()

if sys.platform == "darwin":
    networker = LinkedIn(webdriver.Chrome(), username, password)
else:
    networker = LinkedIn(webdriver.PhantomJS(), username, password)
networker.run()
