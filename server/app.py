from flask import Flask, request, jsonify
from flask_cors import cross_origin
from selenium import webdriver
from scraper import Scraper
from exception_handling import MyException, error_handler


app = Flask(__name__)


main_url = "https://www.imdb.com/"


""" @app.route('/')
@cross_origin()
def getPageSource():
    try:
        res = Scraper.openURL(main_url)
    except Exception as e:
        res = str(e)
        print(e)
    return res """


@app.route("/search", methods=["POST"])
@cross_origin()
def search():
    kwd = request.json["kwd"]
    type = request.json["type"]
    basic_details = Scraper.search_keyword(kwd, type)
    return jsonify(basic_details)


@app.route("/reviews/<kwd>/<type>")
@cross_origin()
def reviews(kwd, type):
    reviews = Scraper.get_review_details(kwd, type)
    return jsonify(reviews)


@app.errorhandler(MyException)
def handle(err):
    return error_handler(err)


@app.errorhandler(500)
def handle(err):
    return jsonify({"msg": str(err)}), 500


if __name__ == "__main__":
    app.run(debug=True)
