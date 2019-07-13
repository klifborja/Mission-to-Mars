from flask import Flask, render_template
from flask_pymongo import flask_pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017/mission_to_mars'

client = pymongo.MongoClient(conn)


@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)

@pp.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_all()

if __name__=="__main__":
    app.run()