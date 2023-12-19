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

    def request(self, url:str, method:str="GET", headers:dict = {}, body:dict = {}):
        return requests.request(method, url, headers=headers, data=body)

    def request_html_content(self):
        # only request if last_update_time is older than {self.cache_duration_minutes} minute
        if self.current_page_data:
            if datetime.datetime.now() - self.last_update_time < datetime.timedelta(minutes=self.cache_duration_minutes):
                logging.info("Use cached data.")
                return self.current_page_data
        
        # html content, binary
        self.current_page_data = self.request("https://m-league.jp/").content
        self.last_update_time = datetime.datetime.now()
        logging.info("Update data.")
        return self.current_page_data

    def _process_personal_bytes(self, personal:bytes)->list[str]:
        result = ""
        is_inside = False
        
        for ch in personal.decode():
            if is_inside:
                if ch == '>':
                    is_inside = False
                continue
            else:
                if ch == '<':
                    is_inside = True
                else:
                    result += str(ch)
        return result.split()

    def get_personal_score(self)->list:
        data = self.request_html_content()
        
        _, personal_score_raw, personal_highest_raw, last_avoid_rate_raw = data.split(b'<h3 class="p-ranking__personal-heading">')
        
        personal_score_title, personal_score_raw = personal_score_raw.split(b'</h3>')
        personal_scores = personal_score_raw.split(b'<td>')[1:]
        
        result = []
        result.append(personal_score_title.decode())
        result.append("|順位|  |個人名|  |Point|")
        
        for each in personal_scores:
            info = self._process_personal_bytes(each)
            pos, name, point = info[0], info[1], info[2]
            result.append(f"{pos}. {name} {point}")

        return result

    def get_personal_highest(self)->list:
        data = self.request_html_content()
        
        _, personal_score_raw, personal_highest_raw, last_avoid_rate_raw = data.split(b'<h3 class="p-ranking__personal-heading">')
        
        personal_highest_title, personal_highest_raw = personal_highest_raw.split(b'</h3>')
        personal_highest = personal_highest_raw.split(b'<td>')[1:]

        result = []
        result.append(personal_highest_title.decode())
        result.append("|順位|  |個人名|  |Point|")
        
        for each in personal_highest:
            info = self._process_personal_bytes(each)
            pos, name, point = info[0], info[1], info[2]
            result.append(f"{pos}. {name} {point}")

        return result

    def get_last_avoid_rate(self)->list:
        data = self.request_html_content()
        
        _, personal_score_raw, personal_highest_raw, last_avoid_rate_raw = data.split(b'<h3 class="p-ranking__personal-heading">')
        
        last_avoid_rate_title, last_avoid_rate_raw = last_avoid_rate_raw.split(b'</h3>')[:2]
        last_avoid_rate = last_avoid_rate_raw.split(b'<td>')[1:]

        result = []
        result.append(last_avoid_rate_title.decode())
        result.append("|順位|  |個人名|  |Rate|")
        
        for each in last_avoid_rate:
            info = self._process_personal_bytes(each)
            pos, name, point = info[0], info[1], info[2]
            result.append(f"{pos}. {name} {point}")

        return result


if __name__ == "__main__":
    req = Request()
    
    personal_score = req.get_personal_score()
    print(personal_score)

    personal_highest = req.get_personal_highest()
    print(personal_highest)

    last_avoid = req.get_last_avoid_rate()
    print(last_avoid)
    
    
    