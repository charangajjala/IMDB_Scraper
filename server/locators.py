
from platform import release
import re


class Locator:

    searchbox_path = "//input[@id='suggestion-search']"
    searchbutton_path = "//button[@id='suggestion-search-button']"
    
    type_info = {'tv': 'tv',
                 'tv_episode': 'ep',
                 'video_game': 'vg',
                 "movie" :'ft',
                 'type_url': 'find?q={}&s=tt&ttype={}&ref_=fn_'}

    first_title_path = "//table[@class='findList']//tbody[1]//tr[1]//td[2]//a[1]"

    top_path = "//section[@class='ipc-page-background ipc-page-background--baseAlt sc-910a7330-0 iZtLgL']//section[1]"

    page_top_path = ""

    page_top_left_path =""

    page_top_right_path = ""

    

    @classmethod
    def set_page_top_path(cls,type):

        if(type=="tv_episode"):
            cls.page_top_path = f"{cls.top_path}//div[3]"
        else:
            cls.page_top_path = f"{cls.top_path}//div[2]"

        
    @classmethod
    def set_page_top_left_right_path(cls,is_released):
        cls.page_top_left_path = f"{cls.page_top_path}//div[1]"
        if  is_released:
            cls.page_top_right_path = f"{cls.page_top_left_path}//div[2]"
        else:
            cls.page_top_right_path = None

    @classmethod
    def get_title_path(cls,type):
        return f"{cls.page_top_left_path}//h1[1]"

    @classmethod
    def get_releasetime_path(cls,type):
        path = f"{cls.page_top_left_path}//div[1]//ul[1]"
        if(type=="tv"):
            released_time_path = f"{path}//li[2]//a"
        elif (type=="tv_episode"):
            released_time_path = f"{path}//li[1]"
        elif (type=="movie"):
            released_time_path = f"{path}//li[1]//a"
        return released_time_path
        





    


       






    
