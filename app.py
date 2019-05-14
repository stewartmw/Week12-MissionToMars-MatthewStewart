from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_document_for_index = mongo.db.mars_documents.find_one()
    return render_template("index.html", mars_document=mars_document_for_index)

@app.route("/scrape")
def scraper():
    mars_documents = mongo.db.mars_documents
    mars_documents_data = scrape_mars.scrape()
    mars_documents.update({}, mars_documents_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)