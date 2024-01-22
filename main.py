from src.connection import SalesforceConnection
import pandas as pd
import os

def main():
    sf = SalesforceConnection()
        # result = sf.query('SELECT Id, Name FROM Account LIMIT 10')
        # print(result)


    df, report_name = sf.extract_data_report()

    if not os.path.exists('data'):
        os.makedirs('data')

    df.to_csv(f'data/{report_name}.csv')

    

    


if __name__ == '__main__':
    main()