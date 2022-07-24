from flask import Flask, render_template, request
from flask_cors import cross_origin
from selenium import webdriver
from scraper import Scraper


app = Flask(__name__)


main_url = 'https://www.imdb.com/'


""" @app.route('/')
@cross_origin()
def getPageSource():
    try:
        res = Scraper.openURL(main_url)
    except Exception as e:
        res = str(e)
        print(e)
    return res """

@app.route('/search',methods=['POST'])
@cross_origin()
def search():
 try:
    Scraper()
    Scraper.openURL(main_url)
    kwd = request.json['kwd']
    type = request.json['type']
    Scraper.search_keyword(kwd,type)
 except Exception as e:
    print(e)
    raise e
    
if(__name__ == '__main__'):
    app.run(debug=True)
