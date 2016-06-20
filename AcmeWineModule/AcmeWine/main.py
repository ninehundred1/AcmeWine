import os
import sys
import validate_CSV


if __name__ == '__main__':

    path = sys.argv[1]
    if len(sys.argv) > 2:
        sort_csv = sys.argv[2]
    else:
        sort_csv = False
    
    if os.path.exists(path):
        order = validate_CSV.validate_CSV(sort_csv, path)
        print order.get_orders_summary()
    