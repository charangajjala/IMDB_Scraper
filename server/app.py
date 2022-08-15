from flask import Flask, request, jsonify
from flask_cors import cross_origin
from scraper import Scraper
from exception_handling import MyException, error_handler, request_validation


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
    kwd = request.json.get("kwd")
    type = request.json.get("type")
    request_validation(kwd, type)
    basic_details = Scraper.search_keyword(kwd, type)
    return jsonify(basic_details)


@app.route("/reviews/<kwd>/<type>", methods=["POST"])
@cross_origin()
def reviews(kwd, type):
    num_reviews = request.json.get("num") 
    request_validation(kwd, type)
    if num_reviews is not None:
        if isinstance(num_reviews, str):
            raise MyException("Number of reviews must not be a string", 400)
        elif num_reviews <= 0:
            raise MyException("Number of reviews should be greater than zero", 400)
    reviews = Scraper.get_review_details(kwd, type, num_reviews)
    return jsonify(reviews)


@app.route("/toppopularities/<kwd>/<type>")
@cross_origin()
def popularities(kwd, type):
    request_validation(kwd, type)
    popularities = Scraper.get_popularities(kwd, type)
    return jsonify(popularities)


@app.route("/toprated/<kwd>/<type>")
@cross_origin()
def top_shows(kwd, type):
    request_validation(kwd, type)
    shows = Scraper.get_toprated_shows(kwd, type)
    return jsonify(shows)


@app.errorhandler(MyException)
def handle(err):
    return error_handler(err)


@app.errorhandler(500)
def handle(err):
    return jsonify({"msg": str(err)}), 500


if __name__ == "__main__":
    app.run(debug=True)
