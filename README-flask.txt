from here run 

1. start local Flask app:

>python main.py


2. use cURL to make a post to the local server with the csv file

>curl -F file=@C:\Users\Meyer\Downloads\orders.csv http://localhost:5000/orders/import


3. Get a the summary of all orders (HERE I AM NOT SURE HOW TO PASS IT ON BETWEEN THE VIEWS IN FLASK, SO I DIDN'T GET THAT TO WORK)


>curl http://localhost:5000/orders?valid=0





