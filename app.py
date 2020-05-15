from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape
import pymongo

app = Flask(__name__)

# Establish the connection
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Define the database
#db = client.mars_db

@app.route("/")
def index(): 
  mars = mongo.db.mars.find_one()
  return render_template("index.html", mars_data=mars)

@app.route("/scrape")
def scraper():
  mars = mongo.db.mars
  mars_data = mars_scrape.scrape()
  mars.update({}, mars_data, upsert=True)
  return redirect ("/", code=302)

if __name__ == "__main__":
  app.run(debug=True)