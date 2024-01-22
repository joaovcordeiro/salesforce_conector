from simple_salesforce import Salesforce
from simple_salesforce import SalesforceAuthenticationFailed, SalesforceMalformedRequest
from src.config import get_salesforce_config
import pandas as pd
import requests
import logging
from io import StringIO
import time

class SalesforceExtractionError(Exception):
    def __init__(self, mensagem="An error occurred while extracting the report from Salesforce."):
        self.mensagem = mensagem
        super().__init__(self.mensagem)

class SalesforceConnection:
    def __init__(self):
        config = get_salesforce_config()
        self.username = config['username']
        self.password = config['password']
        self.security_token = config['security_token']
        self.domain = config['domain']
        self.instance_url = config['instance_url']
        self.report_id = config['report_id']
        self.export = config['export']
        self.sf = None

    def connect(self):
        try:
            if not self.sf:
                self.sf = Salesforce(
                    username=self.username,
                    password=self.password,
                    security_token=self.security_token,
                    domain=self.domain,
                )
                return self.sf
        except (SalesforceAuthenticationFailed, SalesforceMalformedRequest) as e:
            raise SalesforceExtractionError(f"Salesforce connection failed: {e}")

    def extract_data_report(self, report_id=None, export=None, log_errors=True):
        if not self.sf:
            self.connect()

        report_id = report_id or self.report_id

        try:
            if not (self.report_id and self.instance_url):
                raise ValueError("Salesforce report not configured")

            export = export or self.export
            sf_url = self.instance_url + self.report_id + export

            response = requests.get(sf_url, headers=self.sf.headers, cookies={'sid': self.sf.session_id})
            response.raise_for_status()  # Raises an exception for HTTP status codes other than 2xx

            downloaded_data = response.content.decode('utf-8')
            df = pd.read_csv(StringIO(downloaded_data))

            report_name = self.sf.query_all(f"SELECT Name FROM Report where Id = '{report_id}'")
            report_name = report_name['records'][0]['Name']

            return df, report_name

        except requests.exceptions.RequestException as e:
            # Handles exceptions related to HTTP requests (connection, timeout, etc.)
            if log_errors:
                logging.error(f"Error during HTTP request: {e}")
            raise SalesforceExtractionError(f"Error during HTTP request: {e}")

        except ValueError as e:
            # Handles exceptions related to invalid values
            if log_errors:
                logging.error(f"Error during data extraction: {e}")
            raise SalesforceExtractionError(f"Error during data extraction: {e}")

    def query(self, query, log_errors=True):
        if not isinstance(query, str):
            raise ValueError("Query must be a string.")

        if not self.sf:
            self.connect()

            try:
                result = self.sf.query_all(query)
                return result
            except SalesforceAuthenticationFailed as e:
                if log_errors:
                    logging.error(f"Authentication error: {e}")
                raise SalesforceExtractionError(f"Authentication error: {e}")
            except SalesforceMalformedRequest as e:
                if log_errors:
                    logging.error(f"Malformed request error: {e}")
                raise SalesforceExtractionError(f"Malformed request error: {e}")
            except Exception as e:
                if log_errors:
                    logging.error(f"Unexpected error during query execution: {e}")
                raise SalesforceExtractionError(f"Unexpected error during query execution: {e}")

   