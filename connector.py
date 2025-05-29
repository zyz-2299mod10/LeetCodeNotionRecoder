import requests
from printer import *
import yaml
import os

class NOTION:
    def __init__(self):    
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "config.yml")

        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
        self.API_KEY = config["API"]
        self.topic = config["Topic"]

        self.headers = {
            "Authorization": "Bearer " + self.API_KEY["NOTION_TOKEN"],
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        self.check_conntection()

    def check_conntection(self,):
        url = f"https://api.notion.com/v1/databases/{self.API_KEY['DATABASE_ID']}"
        res = requests.get(url, headers=self.headers)

        printYellow("Check connection.... ")
        if res.status_code == 200:
            printGreen("Success\n")
        else:
            print(
                "False \n" \
                f"Status: {res.status_code} \n" \
                f"Text: {res.text} \n" \
                "Exit"
            )            
            
            exit()

    def create_page(self, data: dict, children:list = None):
        create_url = "https://api.notion.com/v1/pages"

        payload = {"parent": {"database_id": self.API_KEY["DATABASE_ID"]}, "properties": data}
        
        if children is not None:
            payload["children"] = children

        res = requests.post(create_url, headers=self.headers, json=payload)
        
        if res.status_code != 200:
            printRed("Create Fail")
            print("Response:", res.text)
        else:
            printGreen("Create page success\n")

        return res
    
    def get_pages(self, num_pages=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        url = f"https://api.notion.com/v1/databases/{self.API_KEY['DATABASE_ID']}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.headers)

        data = response.json()

        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{self.API_KEY['DATABASE_ID']}/query"
            response = requests.post(url, json=payload, headers=self.headers)
            data = response.json()
            results.extend(data["results"])

        return results

