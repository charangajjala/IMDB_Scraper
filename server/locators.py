
class Locator:

    searchbox_path = "//input[@id='suggestion-search']"
    searchbutton_path = "//button[@id='suggestion-search-button']"
    first_title_path = "//table[@class='findList']//tbody[1]//tr[1]//td[2]//a[1]"

    top_path = "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section"

    page_top_path = ""

    page_top_left_path = ""

    page_top_right_path = ""

    @classmethod
    def set_page_top_path(cls, type):

        if type == "tv_episode":
            cls.page_top_path = f"{cls.top_path}//div[3]"
        else:
            cls.page_top_path = f"{cls.top_path}//div[2]"

    @classmethod
    def set_page_top_left_right_path(cls, is_released):
        cls.page_top_left_path = f"{cls.page_top_path}//div[1]"
        if is_released:
            cls.page_top_right_path = f"{cls.page_top_left_path}//div[2]"
        else:
            cls.page_top_right_path = None

    @classmethod
    def get_title_path(cls, type):
        return f"{cls.page_top_left_path}//h1[1]"

    @classmethod
    def get_releasedtime_path(cls, type):
        path = f"{cls.page_top_left_path}//div[1]//ul[1]"
        if type == "tv":
            released_time_path = f"{path}//li[2]//a"
        elif type == "tv_episode":
            released_time_path = f"{path}//li[1]"
        elif type == "movie":
            released_time_path = f"{path}//li[1]//a"
        return released_time_path

    @classmethod
    def get_runtime_path(cls, type, num=None, is_techspec = False):
        path = ""
        if type != "tv_episode":

            if num is not None:
                path = f'//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[{num}]'
            else:
                path = f'//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li'

        else:
            if is_techspec:
                path = '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[@data-testid="TechSpecs"]/div[2]/ul/li[1]/div'
            else:
                path = f'//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[{num}]'
        return path

    @classmethod
    def get_page_middle_path(cls, type=""):
        """if (type=="tv_episode"):
        return f"{cls.top_path}//div[4]"
        else:
            return f"{cls.top_path}//div[3]" """

        find_div = cls.page_top_path.rfind("div")
        for char in cls.page_top_path[find_div:]:
            if char.isdigit():
                index = int(char) + 1
                return f"{cls.top_path}//div[{index}]"

    @classmethod
    def get_middle_left_right_path(cls, which):
        path = (
            f"{cls.get_page_middle_path()}//div[2]//div[{1 if which =='left' else 2}]"
        )
        return path

    @classmethod
    def get_checkif_released_path(cls):
        path = f"{cls.get_releaseCheck_path()}//div[@class='sc-5766672e-0 ldgxcp']"
        return path

    @classmethod
    def get_releaseCheck_path(cls):
        path = f"{cls.get_middle_left_right_path('right')}//div[1]"
        return path

    @classmethod
    def get_releaseTime_path(cls):
        path = f"{cls.get_checkif_released_path()}//div[2]"
        return path

    @classmethod
    def get_genre_path(cls,get_one=False,num=None):
        path = '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[@data-testid="Storyline"]/div[2]/ul[2]/li[@data-testid="storyline-genres"]/div/ul/li'
        if get_one:
            path = f'//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[@data-testid="Storyline"]/div[2]/ul[2]/li[@data-testid="storyline-genres"]/div/ul/li[{num}]/a'
        return path

    @classmethod
    def get_description_path(cls, is_max_size, type, give_alt=False):
        alt = "p" if give_alt else "div[2]"
        path = f"//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/{alt}/span[{3 if is_max_size else 2}]"

        if type == "tv_episode":
            path = f"//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[4]/div[2]/div[1]/div[1]/{alt}/span[{3 if is_max_size else 2}]"
        return path

    @classmethod
    def get_authors_path(cls, for_writers=None, type=None):
        path = f"{cls.get_persons_paths(type)}[{2 if for_writers else 1 if for_writers is None else 3}]/div/ul/li"
        return path

    @classmethod
    def get_author_paths(cls, no_author, for_writers=None, type=None):
        path1 = f"{cls.get_authors_path(for_writers,type=type)}[{no_author}]/a"
        path2 = f"{cls.get_authors_path(for_writers,type=type)}[{no_author}]/span"
        return path1, path2

    @classmethod
    def get_persons_paths(cls, type):
        path = ""
        if type == "tv_episode":
            path = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[4]/div[2]/div[1]/div[3]/ul/li'
        else:
            path = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li'
        return path

    @classmethod
    def get_rating_path(cls,type):
        path = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[@data-testid="hero-rating-bar__aggregate-rating"]/a/div/div/div[2]'
        if type == 'tv_episode':
            path = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div/div[@data-testid="hero-rating-bar__aggregate-rating"]/a/div/div/div[2]'
        return path

    @classmethod
    def get_popularity_path(cls):
        path = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[@data-testid="hero-rating-bar__popularity"]/a/div/div/div[2]/div[1]'
        return path

    @classmethod
    def get_reviews_link_path(cls):
        path = '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[@data-testid="UserReviews"]/div[1]/a[1]'
        return path

    def single_review_path(num):
        path = f'//*[@id="main"]/section/div[2]/div[@class="lister-list"]/div[{num}]'
        return path

    @classmethod
    def get_review_detail_paths(cls,num=None):
      if num is None:
        count_path = '//*[@id="main"]/section/div[2]/div[@class="lister-list"]/div'
        return count_path
      single_review_path = Locator.single_review_path(num)
      rating_path = f'{single_review_path}/div[1]/div[1]/div[@class="ipl-ratings-bar"]'
      spoiler_path = f'{single_review_path}/div[1]/div[1]/span[@class="spoiler-warning"]'
      title_path = f'{single_review_path}/div[1]/div[1]/a'
      des_path = f'{single_review_path}/div[1]/div[1]/div[@class="content"]/div[1]'
      name_date_path = f'{single_review_path}/div[1]/div[1]/div[@class="display-name-date"]'
      helpfulness_path = f'{single_review_path}//div[@class="actions text-muted"]'
      return {'rating_path':rating_path,'spoiler_path':spoiler_path,'name_date_path':name_date_path,'helpfulness_path':helpfulness_path,'title_path':title_path,'des_path':des_path,}