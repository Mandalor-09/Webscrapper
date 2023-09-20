
from flask import Flask,render_template,request,jsonify
from pymongo.mongo_client import MongoClient
from scrapper import scrape_product_data
import logging

from urllib.parse import quote_plus  # Import quote_plus
# URL encode special characters in the password
password = quote_plus("")
# Construct the MongoDB connection URI
uri = f"mongodb+srv://Mandalor_09:{password}@webscrapper.vzcp7cg.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client['webscrapper']
coll_pw_eng = db['scraper_pwskills_eng']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':

        search_query = request.form['content'].replace(" ","")
        #print(search_query,'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>')
        reviews = scrape_product_data(search_query)
        #print(reviews,'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>')
        coll_pw_eng.insert_many(reviews)
        return render_template('result.html', reviews=reviews)

    else:
        return render_template('index.html')
    # return render_template('results.html')
if __name__=="__main__":
    app.run(host="0.0.0.0")


