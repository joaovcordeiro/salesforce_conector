from dotenv import load_dotenv
import os
import json

load_dotenv()


def get_salesforce_config():
    credentials = {
        "username": os.getenv("SF_USERNAME"),
        "password": os.getenv("SF_PASSWORD"),
        "security_token": os.getenv("SF_SECURITY_TOKEN"),
        "domain": os.getenv("SF_DOMAIN") or "login",
        "instance_url": os.getenv("SF_INSTANCE_URL"),
        "report_id": os.getenv("SF_REPORT_ID"),
        "export": os.getenv("SF_EXPORT") or "?isdtp=p1&export=1&enc=UTF-8&xf=csv",
        "querys": json.loads(os.getenv("SF_QUERYS")),
    }

    if not all(
        [
            credentials["username"],
            credentials["password"],
            credentials["security_token"],
            credentials["instance_url"],
        ]
    ):
        raise Exception("Missing Salesforce credentials")

    return credentials
