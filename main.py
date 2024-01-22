from src.connection import SalesforceConnection
import pandas as pd
import os


def main():
    sf = SalesforceConnection()
    # result = sf.query()

    df, report_name = sf.extract_data_report()

    if not os.path.exists(f"Salesforce/{report_name}"):
        os.makedirs("Salesforce", exist_ok=True)

    df.to_csv(f"Salesforce/{report_name}.csv")

    # for name, query_result in result:
    #     if not os.path.exists(f"Salesforce/{name}"):
    #         os.makedirs("Salesforce", exist_ok=True)

    #     df = pd.DataFrame(query_result)

    #     df.to_csv(f"Salesforce/{name}.csv")


if __name__ == "__main__":
    main()
