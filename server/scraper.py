from platform import release
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from locators import Locator

DRIVER = None
chrome_executable_path = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


class Scraper:
    driver = DRIVER
    url = ''

    def __init__(self):
        try:
            global DRIVER
            DRIVER = webdriver.Chrome(
                executable_path=chrome_executable_path, chrome_options=chrome_options)
            Scraper.driver = DRIVER
            
        except Exception as e:
            raise Exception("Error in initialization of chromedriver", str(e))

    @classmethod
    def openURL(cls, url):
        if(cls.driver is None):
            raise cls.getException('No driver available')
        try:
            Scraper.url = url
            cls.driver.get(url)
        except Exception as e:
            raise cls.getException('Error in opening url', str(e))

    @classmethod
    def findByXpath(cls, xpath):
        if(xpath is None):
            raise cls.getException('findByXpath: No xpath available')
        try:
            return cls.driver.find_element(By.XPATH, xpath)
        except Exception as e:
            raise cls.getException(
                f'Error in finding the element at {xpath} ', str(e))

    @classmethod
    def search_keyword(cls, kwd, type):
        search_bar = cls.findByXpath(Locator.searchbox_path)
        search_bar.send_keys(kwd)
        search_button = cls.findByXpath(Locator.searchbutton_path)
        search_button.click()
        type_tag = Locator.type_info[type]
        cls.openURL(
            cls.url+Locator.type_info['type_url'].format(kwd,type_tag)+type_tag)
        first_a_tag = cls.findByXpath(Locator.first_title_path)
        cls.openURL(first_a_tag.get_attribute('href'))
        basic_details = cls.getBasicDetials(type)
        return basic_details

    @classmethod
    def getBasicDetials(cls,type):
        Locator.set_page_top_path(type)
        Locator.set_page_top_left_right_path(True)
        title = cls.findByXpath(Locator.get_title_path(type))
        release_time = cls.findByXpath(Locator.get_releasetime_path(type))
        print(release_time)
        return {'title': title.text, 'release_time': release_time.text}


    @classmethod
    def getException(cls, msg, err_msg=''):
        return Exception(f"{__class__.__name__}: {msg}\n{err_msg}")

    

    