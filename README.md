
# IMDB Scraper


A web scraper project which extracts various details of movies, episodes and tv shows from the official IMDB website.

## Demo

* API Link : [https://imdb--scraper.herokuapp.com/](https://imdb--scraper.herokuapp.com/)
* Use a client service like [Post Man](https://www.postman.com/downloads/) for testing the [API](#demo)
#### Basic Details
* API Demo
![Test](https://im4.ezgif.com/tmp/ezgif-4-a194e32433.gif)
* Data Base sample
![Test](https://im4.ezgif.com/tmp/ezgif-4-d989ab5a6d.gif)

#### Reviews sample
* API Demo
![Test](https://im4.ezgif.com/tmp/ezgif-4-b8674a891f.gif)
* DB demo
![Test](https://im4.ezgif.com/tmp/ezgif-4-acfd474fb5.gif)





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
