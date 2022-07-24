
class Locator:

    searchbox_path = "//input[@id='suggestion-search']"
    searchbutton_path = "//button[@id='suggestion-search-button']"
    movie = 'ft'
    type_info = {'tv': 'tv',
                 'tv_episode': 'tv_ep',
                 'video_game': 'vg',
                 'type_url': 'find?q=onepiece&s=tt&ttype={}&ref_=fn_'}

    first_title_path = "//table[@class='findList']//tbody[1]//tr[1]//td[2]//a[1]"
