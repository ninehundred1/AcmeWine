from flask import Flask
#import pymongo

app = Flask(__name__)

#directory to store incoming orders
ORDER_UPLOAD_FOLDER = 'C:/Users/Meyer/Documents/GitHub/TouchBehaviorApp/Uploaded_orders/'
app.config['ORDER_UPLOAD_FOLDER'] = ORDER_UPLOAD_FOLDER

