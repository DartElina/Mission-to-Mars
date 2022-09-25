from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import Scrape

app=Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

@app.route("/")
def index():
    mars= mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrap")
def scrape():
    mars=mongo.db.mars
    mars_data = Scrape.scrape_all()
    mars.update_one({},{"$set":mars_data}, upsert=True)
    return redirect('/',code=302)

if __name__ == "__main__":
    app.run()
    