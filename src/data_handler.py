import pandas as pd

class DataHandler:
    @staticmethod
    def parse_query_results(results):
        return pd.DataFrame(results['records'])