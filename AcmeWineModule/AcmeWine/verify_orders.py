
import sys
import csv
from datetime import datetime
import re
import pandas as pd




def parse_and_verify(csv_path, all_orders_details, all_orders_summary, sort_CSV = False):
    """Parse a CSV file line by line. It modifies the passed in lists by reference

    Keyword arguments:
    csv_path = path to the CVS file
    all_orders_details(list) = a list that gets appended to by reference (usually empty)
        - will contain all the details of the orders as a list of dictionaries
    all_orders_summary = a list that gets appended to by reference (usually empty)
        - will contain all the details of the orders as a list of dictionaries
    """

    #init empty dict for the first check if prev_state and zip_code matches previous line
    order_data = {'prev_state' : None, 'prev_zipcode' : None}

    if sort_CSV:
        sort_csv_by_order(csv_path)

    with open(csv_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)

        for i, row in enumerate(csv_reader):
           
           #skip header
            if i > 0:

                # split each row into a list of order attributes **
                # only needed if not sorted and cleaned by Pandas before
                if not sort_CSV:
                        split_row_entry = split_and_check_num_cols('|'.join(row), 7)
                else:
                    split_row_entry = row
      
                if not split_row_entry:
                    pass
                    #print 'Cannot process, order details missing: '+ '|'.join(row)
                else:
                    order_data = validate_entry_handler(split_row_entry, order_data)

                    if order_data:
                        all_orders_details.append(order_data['current_details'])
                        all_orders_summary.append(order_data['current_summary'])
                    else:
                    #set order data back to default if there was an invalid return
                        order_data = {'prev_state' : None, 'prev_zipcode' : None}


def sort_csv_by_order(csv_file_path):
    """ This function parses a CSV file into Pandas, sorts it by 'id' and saves with same name

    Keyword arguments:
    csv_file_path = path to file
    
    Returns:
    None - saves files with name csv_file_path
    """
    index_=['id', 'name', 'email', 'state', 'zipcode', 'birthday', 'birthyear']
    df = pd.DataFrame(columns=index_)

    #parse into Pandas dataframe
    with open(csv_file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)

        for i, row in enumerate(csv_reader):

            if i > 0:
                split_row_entry = split_and_check_num_cols('|'.join(row), 7)

                if split_row_entry:
                    df = df.append(pd.Series(split_row_entry, index=index_), ignore_index=True)

    #convert the order ID to numeric
    df['id'] = df['id'].convert_objects(convert_numeric=True)
    #sort by id
    df = df.sort_values(by='id', ascending=True)
    #save with same name to be parsed again (can use database also)
    df.to_csv(csv_file_path, sep=',', index=False)


def split_and_check_num_cols(row_in, required_row_size):
    """ This function splits '|' deliminated string and checks if the required number of entries are present

    Keyword arguments:
    row_in = list of strings
    required_row_size = the number to check for 
   
    Returns:
    None - if row size doesn't match
    List of entry strings if matches

    """
    if isinstance(row_in, basestring):
        split_row = row_in.split("|")
    else:
        split_row = []
    return [False, split_row][len(split_row) == required_row_size]


def validate_entry_handler(order_attributes, prev_order):
    """ This function handles 4 tasks: 
    1.Transfer all entries into a dict with appropriate keys
    2.Check if the zip code and State match the previous function call
    3.If not, pass the dict into the verification check function
    4.Create a condensed order summary dict

    Keyword arguments:
    current_data_row = A string of '|' separated order attributes
    prev_order = a dict containing the previous order's state and zip code
   
    Returns:
    One dict that contains:
    1. The dict of the validated order details 
    2. The dict of the validated order summary 
    3. The current state
    4. The current zip code
    """

    # ** 1. Add all attributes to the order detail dict **
    current_order_details = transfer_attributes_to_order_details(order_attributes)
    
    # ** 2. Check if previous state and zip match current, then pass without further checks **
    if prev_order['prev_state'] == current_order_details['state'] and prev_order['prev_zipcode'] == current_order_details['zipcode']:
        #print 'auto-pass ID: %s ' %current_order_details["order_id"]
        current_order_details["valid"] = 'True'
    else:
        # ** 3. If no match, do all checks
        current_order_details = do_verification_checks(current_order_details)

    # ** 4. Create a condensed order summary dict **
    current_order_summary = create_order_summary(current_order_details)

    return {'current_details' : current_order_details, 
            'current_summary' : current_order_summary,
            'prev_state' : current_order_details['state'], 
            'prev_zipcode' : current_order_details['zipcode']}


def do_verification_checks(current_order_details):
    """ This function handles all the checks required for the dict of entries

    Keyword arguments:
    current_order_details = A dict with all the order attributes
   
    Returns:
    None - The passed in dict gets modified by reference
    """

    # ** 1. Check valid state **
    check_valid_state(current_order_details)

    # ** 2. Check valid zip (num digits & sum) **
    check_valid_zip(current_order_details)

    # ** 3. Check age is above 21 from now **
    check_age(current_order_details)

    # ** 4 Checkif email format is valid & and not .net AND NY **
    check_email(current_order_details)

    # ** 5. Set order to Valid = True if no errors found **
    if len(current_order_details["errors"]) == 0:
        current_order_details["valid"] = 'True' 
      
    return  current_order_details


def check_dic_integrity(dict_in):
    """ This function checks if all keys are present in dictionary

    Keyword arguments:
    order_details = A dict with all the order attributes
       
    Returns:
    False if the type is not dict or if keys are missing
    """

    keys_needed = ('order_id','name','state', 'email', 'zipcode', 'birthday', 'valid', 'errors')

    if not isinstance(dict_in, dict):
        return False

    elif all (keys in dict_in for keys in keys_needed):
        return True
    
    else:
        return False
 


def create_order_summary(current_order_details):
    """ This function creates a new summary dict from the detail dict passed in

    Keyword arguments:
    current_order_details = A dict with all the order attributes
   
    Returns:
    order_summary - A dict with selected order attributes
    """

    if not check_dic_integrity(current_order_details):
        return False
    else:
        order_summary = {
                "order_id": current_order_details["order_id"],
                "name":  current_order_details["name"],
                "valid":  current_order_details["valid"],
                }
    return order_summary


def transfer_attributes_to_order_details(order_attributes):
    """ This function transfers a list of strings into a dict with appropriate keys

    Keyword arguments:
    order_attributes = list of strings of order attributes
   
    Returns:
    A dict with all the order attributes
    """
   
    if not isinstance(order_attributes, list):
        return False

    if len(order_attributes) == 7:

        order_details = {
            "order_id": "",
            "name": "",
            "state": "",
            "email": "",
            "zipcode": -1,
            "birthday": "",
            "valid": 'False',
            "errors": []}

        order_details["order_id"] = order_attributes[0]
        order_details["name"] = order_attributes[1]
        order_details["email"] = order_attributes[2]
        order_details["state"] = order_attributes[3]
        order_details["zipcode"] = order_attributes[4]
        order_details["birthday"] = order_attributes[5]+' '+order_attributes[6]
        order_details["valid"] = 'False'

        return order_details

    else:
        return False

        

def check_valid_state(order_details):
    """ This function looks at the 'state' in the dict and checks if matching invalid states.
    if yes, an error gets appended to the 'errors' key of the dict

    Keyword arguments:
    order_details = A dict with all the order attributes
       
    Returns:
    None - The passed in dict gets modified by reference
    """
    if not check_dic_integrity(order_details):
        return False
    else:
        invalid_states = ['NJ', 'CT', 'PA', 'MA', 'IL', 'IH', 'OR']
        if order_details["state"].upper() in invalid_states:
            order_details["errors"].append({"rule": "AllowedStates"})
            order_details["errors"].append({"message":  "We don't ship to %s" %order_details["state"]})
            return False
        else:
            return True


def check_valid_zip(current_order_details):
    """ This function looks at the 'zipcode' in the dict and checks if matching 5 or 9 digits.
    if no, an error gets appended to the 'errors' key of the dict

    Keyword arguments:
    order_details = A dict with all the order attributes
       
    Returns:
    None - The passed in dict gets modified by reference
    """

    if not check_dic_integrity(current_order_details):
        return False
    else:
        if len(str(current_order_details["zipcode"])) is not 5 and not len(str(current_order_details["zipcode"])) is 9:
            current_order_details["errors"].append({"rule": "ZipCodeDigits"})
            current_order_details["errors"].append(
                {"message":  "Zipcode is not in proper format: %s" %current_order_details["zipcode"]})
            return False
     
        elif reduce(lambda x, y:int(x)+int(y), list(str(current_order_details["zipcode"]))) > 20:
            current_order_details["errors"].append({"rule": "ZipCodeSum"})
            current_order_details["errors"].append(
                {"message":  "Zipcode sum is larger than 20: %s" %current_order_details["zipcode"]})
            return False

        return True


def check_age(order_details):
    """ This function looks at the 'birthday' in the dict and checks if before 21 years from now.
    There are many ways to do that, if you use epoch to count days, you need to get into leap years, etc 
    to be precise.
    All you really need to know if the person was born before now, 21 years ago. 
    So substract 21 years from today and see if date is after the birthdate

    If no, an error gets appended to the 'errors' key of the dict

    Keyword arguments:
    order_details = A dict with all the order attributes
       
    Returns:
    None - The passed in dict gets modified by reference

    """

    now_string = datetime.now().strftime("%Y %m %d")
    year_ago_21 = int(now_string[0:4])-21
    date_21_years_ago = str(year_ago_21) + now_string[4:]
    date_object_21_years_ago = datetime.strptime(date_21_years_ago,"%Y %m %d")

    if not check_dic_integrity(order_details):
        return False
    else:
    
        #when doing pandas sort, the date is converted, so catch that with an alternative
        try:
            date_object_born = datetime.strptime(order_details["birthday"], '%b %d %Y')
        except:
            try:
                date_object_born = datetime.strptime(order_details["birthday"], '%d-%b %Y')
            except:
                #not compatible date format
                return False

        #if date of birth before today 21 years ago
        if date_object_born > date_object_21_years_ago:
            order_details["errors"].append({"rule": "Age"})
            order_details["errors"].append(
                {"message":  "Age is less that 21 : %s" %order_details["birthday"]})
            return False
        return True

    
def check_email(order_details):
    """ This function looks at the 'email' in the dict and checks if matching 
    a regex that has the usually used characters and check if present. 
    if no, an error gets appended to the 'errors' key of the dict

    Keyword arguments:
    order_details = A dict with all the order attributes
       
    Returns:
    None - The passed in dict gets modified by reference
    """
    if not check_dic_integrity(order_details):
        return False
    else:

        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", 
                order_details["email"]):
            order_details["errors"].append({"rule": "InvalidEmail"})
            order_details["errors"].append(
                {"message":  "Email is not in a valid format: %s" % order_details["email"]})
            return False

        if order_details["state"].upper() == 'NY' and order_details["email"].lower()[-4:] == '.net':
            order_details["errors"].append({"rule": "NYdotNetAddress"})
            order_details["errors"].append(
                {"message":"Email %s (.net) from %s is not allowed" %(order_details["email"],order_details["state"])})
            return False
        return True
