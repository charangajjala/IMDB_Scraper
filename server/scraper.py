from flask import abort
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from locators import Locator
from exception_handling import MyException
from inspect import stack

DRIVER = None
chrome_executable_path = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-dev-shm-usage")


class Scraper:
    driver = DRIVER
    url = ""

    def __init__(self):
        try:
            global DRIVER
            DRIVER = webdriver.Chrome(
                executable_path=chrome_executable_path, chrome_options=chrome_options
            )
            Scraper.driver = DRIVER

        except Exception as e:
            raise Exception("Error in initialization of chromedriver", str(e))

    @classmethod
    def openURL(cls, url):
        if cls.driver is None:
            raise cls.getException("No driver available")
        try:
            Scraper.url = url
            cls.driver.get(url)
        except Exception as e:
            raise cls.getException("Error in opening url", str(e))

    @classmethod
    def findByXpath(cls, xpath):
        if xpath is None:
            raise cls.getException("findByXpath: No xpath available")
        try:

            element = cls.driver.find_element(By.XPATH, xpath)
            print("Searching:", xpath, element)
            return element
        except NoSuchElementException as ne:
            cls.showException("No such element at "+xpath,ne)
            raise ne
        except Exception as e:
            cls.showException("Error Finding element at {xpath}",e)
            raise Exception(str(e))

    @classmethod
    def search_keyword(cls, kwd, type):
        try:
            search_bar = cls.findByXpath(Locator.searchbox_path)
            search_bar.send_keys(kwd)
            search_button = cls.findByXpath(Locator.searchbutton_path)
            search_button.click()
            cls.openURL(cls.get_urlfor_type(kwd, type))
            
            first_a_tag = cls.findByXpath(Locator.first_title_path)
            cls.openURL(first_a_tag.get_attribute("href"))
            basic_details = cls.getBasicDetials(type)
            return basic_details
            
        except NoSuchElementException as e:
            cls.showException("search_keyword: No results for search word",e)
            raise MyException("404 Not Found",404)

        except Exception as e:
            raise e

    @classmethod
    def get_urlfor_type(cls, kwd, type):

        type_info = {
            "tv": "tv",
            "tv_episode": "ep",
            "video_game": "vg",
            "movie": "ft",
            "type_url": "find?q={}&s=tt&ttype={}&ref_=fn_",
        }
        type_tag = type_info[type]
        return cls.url + type_info["type_url"].format(kwd, type_tag) + type_tag

    @classmethod
    def getBasicDetials(cls, type):

        Locator.set_page_top_path(type)
        Locator.set_page_top_left_right_path(cls.check_if_released())
        title = cls.findByXpath(Locator.get_title_path(type))
        basic_details = {"title": title.text}

        if cls.check_if_released():
            released_time = cls.findByXpath(Locator.get_releasedtime_path(type)).text
            basic_details["released"] = True
            basic_details["released_time"] = released_time
        else:
            release_time = cls.get_release_time()
            basic_details["released"] = False
            basic_details["release_time"] = release_time

        return basic_details

    @classmethod
    def check_if_released(cls):
        try:
            path = Locator.get_checkif_released_path()
            cls.findByXpath(path)
            return False
        except NoSuchElementException as e:
            return True

    @classmethod
    def get_release_time(cls):
        path = Locator.get_releaseTime_path()
        return cls.findByXpath(path).text

    @classmethod
    def showException(cls, msg, err):
         print(f"{__class__.__name__}: {msg}\n{str(err)}")
