from distutils.util import subst_vars
from black import main
from flask import abort
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
    size = None
    kwd = ""
    type = ""

    def __init__(self):
        try:
            global DRIVER
            DRIVER = webdriver.Chrome(
                executable_path=chrome_executable_path, chrome_options=chrome_options
            )
            DRIVER.maximize_window()
            Scraper.size = DRIVER.get_window_size()
            Scraper.driver = DRIVER

        except Exception as e:
            Scraper.showException("Error in initialization of chromedriver", e)
            raise e

    @classmethod
    def openURL(cls, url):
        if cls.driver is None:
            raise cls.getException("No driver available")
        try:
            Scraper.url = url
            cls.driver.get(url)
        except Exception as e:
            Scraper.showException("Error opening url", e)
            raise e

    @classmethod
    def findByXpath(cls, xpath):
        if xpath is None:
            cls.showException("findByXpath: No xpath available")
            raise Exception("No xpath available")
        try:
            print("searching path: " + xpath)
            element = cls.driver.find_element(By.XPATH, xpath)

            """ element = WebDriverWait(cls.driver, 20).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )[0] """

            print("got the webelement: " + str(element))
            return element

        except NoSuchElementException as ne:
            cls.showException("No such element at " + xpath, ne)
            raise ne
        except Exception as e:
            cls.showException(f"Error Finding element at {xpath}", e)
            raise e

    @classmethod
    def findByClass(cls, cname):
        if cname is None:
            print("findBycname: No cname available")
            raise Exception("No cname available")
        try:
            print("searching path: " + cname)
            element = cls.driver.find_element(By.CLASS_NAME, cname)

            """ element = WebDriverWait(cls.driver, 20).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )[0] """

            print("got the webelement: " + str(element))
            return element

        except NoSuchElementException as ne:
            cls.showException("No such element at " + cname, ne)
            raise ne
        except Exception as e:
            cls.showException(f"Error Finding element at {cname}", e)
            raise e

    @classmethod
    def findByXpathMany(cls, xpath):
        if xpath is None:
            print(
                "findByXpath: No xpath available",
            )
            raise Exception("No xpath available")
        try:
            elements = cls.driver.find_elements(By.XPATH, xpath)
            print("Searching:", xpath, elements)
            return elements
        except NoSuchElementException as ne:
            cls.showException("No such elements at " + xpath, ne)
            raise ne
        except Exception as e:
            cls.showException("Error Finding elements at {xpath}", e)
            raise e

    @classmethod
    def search_keyword(cls, kwd, type):
        try:
            cls.kwd = kwd
            cls.type = type
            search_bar = cls.findByXpath(Locator.searchbox_path)
            search_bar.send_keys(kwd)
            search_button = cls.findByXpath(Locator.searchbutton_path)
            search_button.click()
            cls.openURL(cls.get_urlfor_type())
            try:
                first_a_tag = cls.findByXpath(Locator.first_title_path)
            except NoSuchElementException as e:
                cls.showException("search_keyword: No results for search word", e)
                raise MyException("404 Not Found", 404)
            cls.openURL(first_a_tag.get_attribute("href"))
            basic_details = cls.getBasicDetials()
            return basic_details

        except Exception as e:
            raise e

    @classmethod
    def get_urlfor_type(cls):

        type_info = {
            "tv": "tv",
            "tv_episode": "ep",
            "video_game": "vg",
            "movie": "ft",
            "type_url": "find?q={}&s=tt&ttype={}&ref_=fn_",
        }
        type_tag = type_info[cls.type]
        return cls.url + type_info["type_url"].format(cls.kwd, type_tag) + type_tag

    @classmethod
    def getBasicDetials(cls):

        Locator.set_page_top_path(cls.type)
        Locator.set_page_top_left_right_path(cls.check_if_released())
        title = cls.findByXpath(Locator.get_title_path(cls.type))
        basic_details = {"title": title.text}

        if cls.check_if_released():
            released_time = cls.findByXpath(
                Locator.get_releasedtime_path(cls.type)
            ).text
            basic_details["released"] = True
            basic_details["released_time"] = released_time
        else:
            release_time = cls.get_release_time()
            basic_details["released"] = False
            basic_details["release_time"] = release_time

        basic_details["genres"] = cls.get_genre()
        basic_details["description"] = cls.get_description()
        if type != "tv_episode":
            basic_details["authors"] = cls.get_authors()

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
    def get_genre(cls):
        path = Locator.get_genre_path()
        print("genre_path", path)
        elements = cls.findByXpathMany(path)
        return [x.text for x in elements]

    @classmethod
    def get_description(cls):

        des = ""
        try:
            path = Locator.get_description_path(cls.is_max_size(), cls.type)
            des = cls.findByXpath(path).text
        except NoSuchElementException as e:
            path = Locator.get_description_path(
                cls.is_max_size(), cls.type, give_alt=True
            )
            des = cls.findByXpath(path).text
        if not des:
            des = "No Description Available"
        return des

    @classmethod
    def is_max_size(cls):
        return cls.driver.get_window_size() == cls.size

    @classmethod
    def get_authors(cls):
        lists = cls.findByXpathMany(Locator.get_authors_path())
        authors = []
        print("authors", lists)
        for i in range(len(lists)):
            paths = Locator.get_author_paths(i + 1)
            main_text = cls.findByXpath(paths[0]).text
            final_text = main_text
            try:
                subst_text = cls.findByXpath(paths[1]).text
                final_text = f"{main_text} {subst_text}"
            except NoSuchElementException as e:
                pass
            authors.append(final_text)
        return authors

    @classmethod
    def showException(cls, msg, err):
        print(f"{__class__.__name__}: {msg}\n{str(err)}")
