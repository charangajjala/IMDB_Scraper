import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from locators import Locator
from exception_handling import MyException
from mydb import  MyDB


chrome_executable_path = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-dev-shm-usage")

kwd = None
type = None
driver = None
url = None

main_url = "https://www.imdb.com/"
on_searched = None


class Scraper:

    url = ""
    size = None
    kwd = ""
    type = ""
    driver = None

    def __init__(self, urll):
        global driver, url
        try:
            DRIVER = webdriver.Chrome(
                executable_path=chrome_executable_path,
                chrome_options=chrome_options,
            )
            DRIVER.maximize_window()
            Scraper.size = DRIVER.get_window_size()
            driver = DRIVER
            Scraper.driver = DRIVER
            Scraper.openURL(urll)
            url = urll
            Scraper.url = urll

        except Exception as e:
            Scraper.showException("Error in initialization of chromedriver", e)
            raise e

    @classmethod
    def openURL(cls, url):
        if cls.driver is None:
            print("No driver available")
            raise Exception("No xpath available")
        try:
            Scraper.url = url
            cls.driver.get(url)
        except Exception as e:
            Scraper.showException("Error opening url", e)
            raise e

    @classmethod
    def findByXpath(cls, xpath, with_wait=False):
        if xpath is None:
            cls.showException("findByXpath: No xpath available")
            raise Exception("No xpath available")
        try:
            print("searching path: " + xpath)

            if with_wait:
                WebDriverWait(cls.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            element = cls.driver.find_element(By.XPATH, xpath)
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
            time.sleep(0.5)
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
    def search_keyword(
        cls,
        kwdd,
        typee,
    ):
        global main_url, on_searched, driver
        if driver:
            driver.close()
        Scraper(main_url)
        try:
            cls.kwd = kwdd
            cls.type = typee
            global kwd
            global type
            kwd = kwdd
            type = typee
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
            db = MyDB()
            title = cls.get_title()
            basic_details = db.handle_basic_details(title)
            if basic_details is None:
                basic_details = cls.getBasicDetials()
                db.handle_basic_details(title,basic_details.copy())
            on_searched = True
            return basic_details

        except NoSuchElementException as e:
            raise e

        except WebDriverException as e:
            driver = None
            kwd = None
            type = None
            cls.search_keyword(kwdd, typee)

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
        basic_details = {}
        basic_details["title"] = cls.get_title()
        basic_details.update(cls.get_runtime())
        basic_details["genres"] = cls.get_genre()
        basic_details["description"] = cls.get_description()
        basic_details.update(cls.get_release_end_details())
        basic_details.update(cls.get_all_persons())
        basic_details.update(cls.get_rating())
        basic_details.update(cls.get_popularity())
        basic_details.update(cls.get_top_rating())

        return basic_details

    @classmethod
    def get_title(cls):
        Locator.set_page_top_path(cls.type)
        Locator.set_page_top_left_right_path(cls.check_if_released())
        title = cls.findByXpath(Locator.get_title_path(cls.type)).text
        return title

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
    def get_runtime(cls):
        dict = {}
        run_time = ""
        if cls.check_if_released():
            if cls.type != "tv_episode":
                path = Locator.get_runtime_path(type=cls.type)
                count = len(cls.findByXpathMany(path))
                path = Locator.get_runtime_path(num=count, type=cls.type)
                run_time = cls.findByXpath(path).text
                if cls.type == "tv":
                    run_time = f"{run_time} per episode"
            else:
                print("check_tech", "title-techspecs-section" in cls.driver.page_source)
                if "title-techspecs-section" in cls.driver.page_source:
                    path = Locator.get_runtime_path(type=cls.type, is_techspec=True)
                    run_time = cls.findByXpath(path).text
                else:
                    path = Locator.get_runtime_path(type=cls.type, num=count)
                    count = len(cls.findByXpathMany(path))
                    run_time = cls.findByXpath(path).text
            dict["run_time"] = run_time
        else:
            pass
        return dict

    @classmethod
    def get_genre(cls):
        path = Locator.get_genre_path()
        print("genre_path", path)
        elements = cls.findByXpathMany(path)
        print("elements", elements)
        genres = []
        for i in range(len(elements)):
            path = Locator.get_genre_path(get_one=True, num=i + 1)
            genre = cls.findByXpath(path).text
            genres.append(genre)
        return genres

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

    @staticmethod
    def is_max_size():
        return Scraper.driver.get_window_size() == Scraper.size

    @staticmethod
    def get_single_authors(lists, for_writers=None):
        authors = []
        for i in range(len(lists)):
            paths = Locator.get_author_paths(i + 1, for_writers, type=Scraper.type)
            main_text = Scraper.findByXpath(paths[0]).text
            final_text = main_text
            try:
                subst_text = Scraper.findByXpath(paths[1]).text
                final_text = f"{main_text} {subst_text}"
            except NoSuchElementException as e:
                pass
            authors.append(final_text)
        return authors

    @classmethod
    def get_authors(cls):
        lists = cls.findByXpathMany(Locator.get_authors_path(type=cls.type))
        return cls.get_single_authors(lists)

    @classmethod
    def get_writers(cls, for_writers):
        path = Locator.get_authors_path(for_writers=for_writers, type=cls.type)
        print("path_writers", path)
        authors = None
        try:
            writers = cls.findByXpathMany(path)
            print("len_writers", len(writers))
        except NoSuchElementException as e:
            return authors
        authors = cls.get_single_authors(writers, for_writers=for_writers)
        return authors

    @classmethod
    def get_all_persons(cls):
        persons = cls.findByXpathMany(Locator.get_persons_paths(type=cls.type))
        dict = {}
        print("persons", len(persons))
        if not persons:
            return dict
        if len(persons) > 2:
            authors = cls.get_authors()
            stars = cls.get_writers(for_writers=False)
            writers = cls.get_writers(for_writers=True)
            dict["stars"] = stars
            dict["writers"] = writers
            dict["authors"] = authors
        elif len(persons) < 2:
            stars = cls.get_authors()
            dict["stars"] = stars
        else:
            authors = cls.get_authors()
            stars = cls.get_writers(for_writers=True)
            dict["stars"] = stars
            dict["authors"] = authors
        return dict

    @classmethod
    def get_release_end_details(cls):
        dict = {}
        if cls.check_if_released():
            released_time = cls.findByXpath(
                Locator.get_releasedtime_path(cls.type)
            ).text
            released = True
            released_time = released_time
        else:
            release_time = cls.get_release_time()
            released = False
            release_time = release_time

        if released:
            if cls.type != "tv_episode":
                year = released_time
                years = year.split("–")
                print("years", year, years)
                dict = {}
                if years[1]:
                    dict["released_in"] = years[0]
                    dict["ended_in"] = years[1]
                else:
                    dict["released_in"] = years[0]
            else:
                dict["released_in"] = released_time
            dict["released"] = True
        else:
            dict["release_in"] = release_time
            dict["released"] = False

        return dict

    @classmethod
    def get_rating(cls):
        path = Locator.get_rating_path(type=cls.type)
        element = cls.get_if_element_exits(path)
        dict = {}
        if element is not None:
            print("rating", element.get_attribute("innerText"))
            text = element.get_attribute("innerText")
            texts = text.split("\n")
            dict["rating_info"] = {"rating": texts[0], "no_ratings": texts[2]}
        else:
            print("rating", None)

        return dict

    @classmethod
    def get_popularity(cls):
        path = Locator.get_popularity_path()
        element = cls.get_if_element_exits(path)
        dict = {}
        if element is not None:
            dict["popularity"] = element.text
        return dict

    @staticmethod
    def get_if_element_exits(xpath, with_wait=False):
        element = None
        try:
            element = Scraper.findByXpath(xpath, with_wait=with_wait)
        except NoSuchElementException as e:
            print(e)
        except TimeoutException as e:
            print(e)
        return element

    @classmethod
    def get_review_details(cls, kwdd, typee, num_reviews):
        global driver, url, on_searched, main_url, kwd, type

        if not Scraper.check_if_same_search(kwdd, type):
            cls.search_keyword(kwdd, typee)

        reviews_list = []
        up_to = []
        try:

            link = cls.get_if_element_exits(Locator.get_reviews_link_path())

            if link:
                cls.openURL(link.get_attribute("href"))

                if num_reviews is None:

                    while True:
                        print("check", len(reviews_list), num_reviews)

                        reviews, upto = Scraper.get_reviews(len(reviews_list))
                        reviews_list += reviews
                        up_to.append(upto)

                        if "ipl-load-more--loaded-all" in cls.driver.page_source:
                            break
                        else:
                            button = WebDriverWait(cls.driver, 10).until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        Locator.get_review_detail_paths()[
                                            "load_more_path"
                                        ],
                                    )
                                )
                            )
                            button.click()
                else:

                    while len(reviews_list) < num_reviews:
                        print("check", len(reviews_list), num_reviews)

                        reviews, upto = Scraper.get_reviews(
                            len(reviews_list), asked_for=num_reviews
                        )
                        reviews_list += reviews
                        up_to.append(upto)
                        if "ipl-load-more--loaded-all" in cls.driver.page_source:
                            break
                        else:
                            button = WebDriverWait(cls.driver, 10).until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        Locator.get_review_detail_paths()[
                                            "load_more_path"
                                        ],
                                    )
                                )
                            )
                            button.click()
                            # time.sleep(5)

            print("reviews_list", len(reviews_list))
            on_searched = False
            return {"reviews": reviews_list, "progress": up_to}

        except NoSuchElementException as e:
            raise e

        except WebDriverException as e:
            driver = None
            kwd = None
            type = None
            print(e)
            print("Raising get_review_details again")
            print("reviews_list", len(reviews_list))
            cls.get_review_details(kwdd, typee, num_reviews)

    @staticmethod
    def get_reviews(num_reviews, asked_for=None):
        paths = Locator.get_review_detail_paths(num_reviews + 1)
        Scraper.findByXpath(paths["single_review_path"], with_wait=True)
        reviews = WebDriverWait(Scraper.driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    Locator.get_review_detail_paths()["count_path"],
                )
            )
        )
        reviews_list = []
        upto = len(reviews)
        print("len(reviews)", len(reviews), num_reviews)
        if asked_for is not None and len(reviews) > asked_for:
            upto = asked_for

        for i in range(num_reviews, upto):
            review = {}
            paths = Locator.get_review_detail_paths(num=i + 1)
            rating = Scraper.get_if_element_exits(paths["rating_path"])
            spoiler = Scraper.get_if_element_exits(paths["spoiler_path"])
            review["rating"] = rating.text if rating else "Rating not available"
            review["spoiler"] = spoiler.text if spoiler else "No spoilers"
            review["title"] = Scraper.findByXpath(paths["title_path"]).text
            description = Scraper.get_if_element_exits(paths["des_path"])
            review["description"] = (
                description.text
                if description and description.text
                else "No description available"
            )
            name_date = (
                Scraper.findByXpath(paths["name_date_path"])
                .get_attribute("innerText")
                .split(" ")
            )
            print("new_date", name_date)
            last_two = name_date[0][len(name_date[0]) - 2 :]
            date = last_two if last_two.isdigit() else last_two[1]
            review["name"] = (
                name_date[0][: len(name_date[0]) - 2]
                if last_two.isdigit()
                else name_date[0][: len(name_date[0]) - 1]
            )
            review["date"] = f"{date} {name_date[1]} {name_date[2]} "
            helpfulness = (
                Scraper.findByXpath(paths["helpfulness_path"])
                .get_attribute("innerText")
                .split(" ")
            )
            review["helped_votes"] = helpfulness[0]
            review["total_votes"] = helpfulness[3]

            reviews_list.append(review)
        return reviews_list, upto

    @classmethod
    def get_popularities(cls, kwdd, typee):
        global driver, kwd, type
        if typee == "tv_episode":
            raise MyException("No popularity for episodes", 404)
        if not Scraper.check_if_same_search(kwdd, typee):
            cls.search_keyword(kwdd, typee)
        try:
            cls.openURL(
                f"https://www.imdb.com/chart/{typee}meter/?sort=rk,asc&mode=simple&page=1"
            )
            pops = cls.findByXpathMany(Locator.get_topshows_paths())
            pops_list = []
            for i in range(len(pops)):
                paths = Locator.get_topshows_paths(i + 1)
                title, rank_info = (
                    cls.findByXpath(paths["title_path"])
                    .get_attribute("innerText")
                    .split("\n")
                )
                print("rank_info", rank_info.split(" "))
                rank = rank_info.split(" ")[0]
                rating = cls.findByXpath(paths["rating_path"]).get_attribute(
                    "innerText"
                )
                pop = {"rating": rating, "title": title, "rank": rank}
                change_ele = cls.get_if_element_exits(paths["change_path"])
                if change_ele:
                    class_name = change_ele.get_attribute("class")
                    change = rank_info.split(" ")[3].replace(")", "")
                    pop["change"] = (
                        f"Increased by {change}"
                        if "up" in class_name
                        else f"Decreased by {change}"
                    )
                else:
                    pop["change"] = "No change"

                pops_list.append(pop)
                on_searched = False
            return pops_list

        except NoSuchElementException as e:
            raise e

        except WebDriverException as e:
            driver = None
            kwd = None
            type = None
            cls.get_popularities(kwdd, typee)
            cls.showException("WebDriverException")

        except Exception as e:
            raise e

    @classmethod
    def get_top_rating(cls):
        dict = {}
        element = cls.get_if_element_exits(Locator.get_top_rating_path())
        if element is not None:
            dict["top_rating"] = element.get_attribute("innerText").split(" ")[3]
        return dict

    @classmethod
    def get_toprated_shows(cls, kwdd, typee):
        global driver, kwd, type
        if typee == "tv_episode":
            raise MyException("No top ratings for episodes", 404)
        if not Scraper.check_if_same_search(kwdd, typee):
            cls.search_keyword(kwdd, typee)
        try:
            cls.openURL(
                f"https://www.imdb.com/chart/top{typee if typee=='tv' else ''}?ref_=tt_awd"
            )
            shows = cls.findByXpathMany(Locator.get_topshows_paths())
            shows_list = []
            for i in range(len(shows)):
                paths = Locator.get_topshows_paths(i + 1)
                title_info = cls.findByXpath(paths["title_path"]).get_attribute(
                    "innerText"
                )
                print("title_info", title_info)
                rank, title = title_info.split(" ", 1)
                title = title.strip()
                rank = rank.replace(".", "")
                rating = cls.findByXpath(paths["rating_path"]).get_attribute(
                    "innerText"
                )
                show = {"rating": rating, "title": title, "rank": rank}
                shows_list.append(show)
                on_searched = False
            return shows_list

        except NoSuchElementException as e:
            raise e

        except WebDriverException as e:
            driver = None
            kwd = None
            type = None
            cls.get_toprated_shows(kwdd, typee)
            cls.showException("WebDriverException")

        except Exception as e:
            raise e

    @staticmethod
    def check_if_same_search(kwdd, typee):
        global kwd, type, driver
        return (
            kwd is not None
            and type is not None
            and driver is not None
            and kwd == kwdd
            and type == typee
            and on_searched is True
        )

    @classmethod
    def showException(cls, msg, err=""):
        print(f"{__class__.__name__}: {msg}\n{str(err)}")
