
# IMDB Scraper

![Python](https://img.shields.io/badge/Python-3.6-blueviolet)
![Framework](https://img.shields.io/badge/Framework-Flask-red)
![Data Base](https://img.shields.io/badge/Database-MongoDb-yellow)
![Library](https://img.shields.io/badge/Library-Selenium-green)
![Front End](https://img.shields.io/badge/Framework-ReactJs-blue)

A web scraper project which extracts various details of movies, episodes and tv shows from the official IMDB website.

# Demo

* API Link : [https://imdb--scraper.herokuapp.com/](https://imdb--scraper.herokuapp.com/)
* Use a client service like [Post Man](https://www.postman.com/downloads/) for testing the [API](#demo)  

Basic Details
* API Demo
![2022-10-18](https://user-images.githubusercontent.com/64437927/196725924-4863453a-2113-4eee-917a-79c45bca590b.png)

* Data Base Demo
![2022-10-18 (1)](https://user-images.githubusercontent.com/64437927/196726112-da1a693b-5709-433f-87e7-5a888d40d0fa.png)

Reviews sample
* API Demo
![2022-10-18 (3)](https://user-images.githubusercontent.com/64437927/196726269-9b0bfa9a-0a7c-4732-a411-458775e6fb54.png)
* DB demo
![2022-10-18 (2)](https://user-images.githubusercontent.com/64437927/196726462-e320b031-a082-49fb-9c7b-7ad646cbe7db.png)

## API Reference

#### Get basic details of movies and tv shows.

```
  POST https://imdb--scraper.herokuapp.com//search
  Body:
      kwd : search word
      type: movie or tv_show or tv_episode 
```

| Body      | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `JSON`    | `string`    | **Required** |

#### Get review of a movie or tv show

```
  POST https://imdb--scraper.herokuapp.com/reviews
  Body:
     num : number of review to get
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `kwd`, `type`      | `string` | **Required** |



## Web Scraping
Scraped the various details of a show
 ### Basic details
 * authors , description, genres, popularity, rating, release date etc.
 ### Review details
 * date, name, ratingm title, helped_votes, total_votes, spoiler
## Setup and Installation
After cloning/ downloading the code, create a virtual environment with python >3.6 as explained [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands).
#### Client (React) Setup
```bash
  cd /client
  npm install 
  cd /client/src
  npm run
```
#### Server (Flask) Setup

```bash
  cd /server
  pip install -r requirements.txt
  py app.py - to activate the server
```
#### Database setup (Mongo DB) Setup
```
1. Follow this mongodb atlas [tutorial](https://www.mongodb.com/basics/mongodb-atlas-tutorial) to create your own cluster.
2. Create a .env file and copy the code in env sample file. Then replce your cluster password in the place holder.
```

    ## Deployement on Heroku
Login or signup in order to create virtual app. You can either connect your github profile or download ctl to manually deploy this project.

[![](https://i.imgur.com/dKmlpqX.png)](https://heroku.com)

* Our next step would be to follow the instruction given on [Heroku Documentation](https://devcenter.heroku.com/articles/getting-started-with-python) to deploy a web app.
* Also, refer [this](https://www.andressevilla.com/running-chromedriver-with-python-selenium-on-heroku/) to setup enviornment variables related to selenium and chrome driver extension on Heroku.
