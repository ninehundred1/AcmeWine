import verify_orders
import json

class validate_CSV(object):
    """Class that handles the current order batch. It parses the raw entries, then
    formats and generates two lists of dicts, all_orders_details and 
    all_orders_summary. The latter can be returned in JSON format via get_orders_summary,
    the former can be queried for a specific order ID string (eg '1234') using 
    get_order_details_by_id, where then the order of that number gets returned in detail,
    or a 'order not found' message if the order does not exist.
    The processing of data will be initiated by the constructor when the instance is 
    created.


    Keyword arguments:
    csv_path = path to the CVS file
    all_orders_details(list) = a list that gets appended to by reference (usually empty)
        - will contain all the details of the orders as a list of dictionaries
    all_orders_summary = a list that gets appended to by reference (usually empty)
        - will contain all the details of the orders as a list of dictionaries
    """


    def __init__(self, csv_sort, csv_path = "C:\Users\Meyer\Downloads\orders.csv"):
        """constructor that upon receiving a file path starts the processing of file

        Keyword arguments:
        csv_path = path to the CVS file
        """
        self.sort_csv = csv_sort
        self.sort_csv = False
        self.all_orders_details = []
        self.all_orders_summary = []
        self.path = csv_path
        #process data
        self.process_new_order_file()


    def process_new_order_file(self):
        """this function calls parse_and_verify() from the verify_orders module to do 
        the actual processing of the file.
        """

        verify_orders.parse_and_verify(
            self.path, self.all_orders_details, self.all_orders_summary, self.sort_csv)
        

    def get_orders_summary(self, valid_only = True):
        """API function to get the order summaries from this instance, returned as JSON

        Keyword arguments:
        valid_only = Filter argument to only return valid orders

        Returns:
        depdening on filter toggle either all valid orders only or all orders, in JSON format
        """
  
        if valid_only:
            #remove all False entries
            only_valid = [num for num in self.all_orders_summary if num['valid'] == 'True']
            return json.dumps(only_valid)
        else:
            return json.dumps(self.all_orders_summary)


    def get_order_details_by_id(self, ID_query):
        """API function to get one order detail by the ID query, returned as JSON

        Keyword arguments:
        ID_query = the ID string eg ('1234')

        Returns:
        if found returns the order details, otherwise returns 'order not found:': ID_query' in JSON
        """

        oder_entry = [num for num in self.all_orders_details if num['order_id'] == ID_query]
        
        if len(oder_entry) == 0:
            return json.dumps({'order not found:': ID_query})
        else:
            return json.dumps(oder_entry)