from flask import Flask
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Creating an instance of Flask
app = Flask(__name__)

# Set up Mongo connection
conn = "mongodb://localhost:27017"
mongo = pymongo.MongoClient(conn)

# Route to render index.html using data from Mongo
@app.route("/")
def home():

    data = mongo.mars_db.mars_collection.find_one()

    return render_template("index.html", mars_data=data)


@app.route("/scrape")
def scrape():
    result=scrape_mars.scrape()

    mongo.mars_db.mars_collection.update({}, result, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
