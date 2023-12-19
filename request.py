import datetime
import requests
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

class Request():
    def __init__(self, cache_duration_minutes:int = 1):
        self.last_update_time:datetime.datetime = None
        self.current_page_data:bytes = None
        self.cache_duration_minutes = cache_duration_minutes

    def _request(self, url:str, method:str="GET", headers:dict = {}, body:dict = {}):
        return requests.request(method, url, headers=headers, data=body)

    def request_html_content(self):
        # only request if last_update_time is older than {self.cache_duration_minutes} minute
        if self.current_page_data:
            if datetime.datetime.now() - self.last_update_time < datetime.timedelta(minutes=self.cache_duration_minutes):
                logging.info("Use cached data.")
                return self.current_page_data
        
        # html content, binary
        self.current_page_data = self._request("https://m-league.jp/").content
        self.last_update_time = datetime.datetime.now()
        logging.info("Update data.")
        return self.current_page_data

if __name__ == "__main__":
    req = Request()
    
    data = req.request_html_content()
    
    
    