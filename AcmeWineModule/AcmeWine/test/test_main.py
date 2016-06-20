
import unittest
import validate_CSV
import verify_orders

 
def test_split_and_check_num_colst():
    test_string1 = 'hello|only|a|few|words'
    return_string1 = ['hello','only','a','few','words']
    num_words = 5
    assert verify_orders.split_and_check_num_cols(test_string1, num_words) == return_string1
    
    num_words = 6
    assert verify_orders.split_and_check_num_cols(test_string1, num_words) == False
    
    test_string2 = 'hello only|a|few|words'
    assert verify_orders.split_and_check_num_cols(test_string2, num_words) == False
    
    test_string3 = ''
    assert verify_orders.split_and_check_num_cols(test_string3, num_words) == False
    
    test_string4 = 04
    assert verify_orders.split_and_check_num_cols(test_string4, num_words) == False


def test_create_order_summary():

    test_string1 = {
            "order_id": "0",
            "name": "1",
            "state": "3",
            "email": "2",
            "zipcode": '4',
            "birthday": '5 6',
            "valid": 'true',
            "errors": []}  

    return_string1 = {"order_id":'0', 'name': '1', 'valid': 'true'}
    assert set(verify_orders.create_order_summary(test_string1))== set(return_string1)
  
    test_string3 = {'email':'hello@sm.com', 'name': 'j', 'valid': 'true'}
    assert verify_orders.create_order_summary(test_string3) == False

    test_string4 = 10
    assert verify_orders.create_order_summary(test_string4) == False
 

def test_transfer_attributes_to_order_details():
    test_string1 = ['0', '1','2', '3', '4', '5','6'] 
    return_string1 = {
            "order_id": "0",
            "name": "1",
            "state": "3",
            "email": "2",
            "zipcode": '4',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  
     
    assert set(verify_orders.transfer_attributes_to_order_details(test_string1)) == set(return_string1)

    test_string2 = ['0', '1','2', '5','6']
    assert verify_orders.transfer_attributes_to_order_details(test_string2)== False

    test_string3 = 40
    assert verify_orders.transfer_attributes_to_order_details(test_string3)== False
 

def test_check_valid_state():
    test_string1 = {
            "order_id": "0",
            "name": "1",
            "state": "NJ",
            "email": "2",
            "zipcode": '4',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_valid_state(test_string1)== False

    test_string2 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '4',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_valid_state(test_string2)== True

    test_string3 = 0
    assert verify_orders.check_valid_state(test_string3)== False


def test_check_valid_zip():
    test_string1 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '12345',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_valid_zip(test_string1)== True

    test_string2 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '123456789',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_valid_zip(test_string2)== False

    test_string3 = {
            "order_id": "0",
            "name": "1",
            "state": "NJ",
            "email": "2",
            "zipcode": '4',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_valid_zip(test_string3)== False

    test_string4 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '4000000000',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_valid_zip(test_string4)== False

    test_string5 = 0
    assert verify_orders.check_valid_zip(test_string5)== False

    test_string6 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '000010101',
            "birthday": '5 6',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_valid_zip(test_string6)== True


def test_check_age():
    test_string1 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '12345',
            "birthday": 'Mar 11 1998',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_age(test_string1)== False

    test_string2 = 0
    assert verify_orders.check_age(test_string2)== False

    test_string3 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '000010101',
            "birthday": 'Mar 11 1978',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_age(test_string3)== True

    test_string4 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "2",
            "zipcode": '000010101',
            "birthday": 'Mar 1111 1978',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_age(test_string4)== False


def test_check_email():
    test_string1 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "hello@hello.com",
            "zipcode": '12345',
            "birthday": 'Mar 11 1998',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_email(test_string1)== True

    test_string2 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "hello@hello.net",
            "zipcode": '12345',
            "birthday": 'Mar 11 1998',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_email(test_string2)== True

    test_string3 = {
            "order_id": "0",
            "name": "1",
            "state": "NY",
            "email": "hello@hello.net",
            "zipcode": '12345',
            "birthday": 'Mar 11 1998',
            "valid": 'False',
            "errors": []}  

    assert verify_orders.check_email(test_string3)== False

    test_string4 = 0
    assert verify_orders.check_email(test_string4)== False


def test_do_verification_checks():
    test_string1 = {
            "order_id": "2",
            "name": "john",
            "state": "CA",
            "email": "hello@hello.com",
            "zipcode": '12345',
            "birthday": 'Mar 11 1978',
            "valid": 'False',
            "errors": []}  

    return_string1 = {
            "order_id": "0",
            "name": "1",
            "state": "CA",
            "email": "hello@hello.com",
            "zipcode": '12345',
            "birthday": 'Mar 11 1998',
            "valid": 'True',
            "errors": []}  

    assert set(verify_orders.do_verification_checks(test_string1))== set(return_string1)

    test_string2 = {
            "order_id": "2",
            "name": "john",
            "state": "CA",
            "email": "hello@hello.com",
            "zipcode": '12345',
            "birthday": 'Mar 11 1978',
            "valid": 'False',
            "errors": []}  

    return_string2 = {
            "order_id": "0",
            "name": "1",
            "state": "NJ",
            "email": "hello@hello.com",
            "zipcode": '12345',
            "birthday": 'Mar 11 1998',
            "valid": 'False',
            "errors": [{"message":  "We don't ship to NJ"}]
            }  

    assert set(verify_orders.do_verification_checks(test_string2))== set(return_string2)



