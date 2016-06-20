
#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import session
from flask import g
from werkzeug import secure_filename
import os
import sys


from app import app

sys.path.append('AcmeWineModule/AcmeWine/')


import validate_CSV



def allowed_file(filename):
    '''
    Helper function to check if a file ends with a certain extension.
    '''
    EXTENSIONS_ALLOWED = set(['csv'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in EXTENSIONS_ALLOWED

#cd first to C:\Program Files\cURL\bin
#curl -F file=@C:\Users\Meyer\Downloads\orders.csv http://localhost:5000/orders/import
@app.route('/orders/import', methods=['POST'])
def post_order_CVS_file():
    '''
    POST CSV FILE
    - the file is also saved in the UPLOAD_FOLDER. Another option is to load it into 
    a MongoDB database, so it can be sorted easily and extended.
    '''
    
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['ORDER_UPLOAD_FOLDER'], filename))
            return_JSON = jsonify({'CSV read':filename}), 201
            ##  GENERATE THE DATA OBJECT (current_order_batch) HERE  
            #Run the module to process the data THEN NOT SURE HOW TO PASS IT TO OTHER VIEWS
            current_order_batch = validate_CSV.validate_CSV(
                False, os.path.join(app.config['ORDER_UPLOAD_FOLDER'], filename))

        else:
            abort(422)
    return return_JSON
  



#curl http://localhost:5000/orders?valid=1
@app.route('/orders', methods=['GET'])
def get_order_summaries():
    '''
    2. GET IMPORTED ORDERS
    - the file is also saved in the UPLOAD_FOLDER. Another option is to load it into 
    a MongoDB database, so it can be sorted easily and extended.
    '''
    only_valid_bool = request.args.get('valid')
    if request.method == 'GET':
        
        return_JSON = jsonify({'No data yet loaded':0}), 201
        '''
        #ACESS THE ORDER OBJECT (current_order_batch) HERE TO CALL
        if only_valid_bool:
            return_JSON = jsonify(results = current_order_batch.get_orders_summary(1))
        else:
            return_JSON = jsonify(results = current_order_batch.get_orders_summary(0))
        '''
    return return_JSON




#curl http://localhost:5000/orders/1234
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_ID(order_id):
    '''
    2. GET ORDER BY ID
    - the file is also saved in the UPLOAD_FOLDER. Another option is to load it into 
    a MongoDB database, so it can be sorted easily and extended.
    '''
    if request.method == 'GET':

        ''
        if not order_id:
            abort(404)
        else:
            #CALL current_order_batch HERE TO GET A SINGLE ORDER DETAIL
            single_order = current_order_batch.get_order_details_by_id(order_id)

        return jsonify({single_order})





@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(422)
def invalid_data(error):
    return make_response(jsonify({'error': 'data received not valid'}), 422)

if __name__ == '__main__':
    app.run(debug=True)

