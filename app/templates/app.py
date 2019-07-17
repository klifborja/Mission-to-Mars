from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017/mission_to_mars'

client = pymongo.MongoClient(conn)


@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars_data=scrape_mars.scrape_all()
   # Update the Mongo database using update and upsert=True
   client.db.collection.update({}, mars_data, upsert=True)

   # Redirect back to home page
   return redirect("/")

if __name__=="__main__":
    app.run(debug=True)