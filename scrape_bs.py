from bs4 import BeautifulSoup
from request import Request

class Scraper():

    def __init__(self):
        self.request = Request()
    
    def get_match_info(self):
        data = self.request.request_html_content()
        soup = BeautifulSoup(data, 'html.parser')
        result = list()
        
        # date
        oppo_date = soup.find('div', attrs={'class': 'p-opponentCard__date'})
        match_date = oppo_date.time['datetime']
        match_weekday = oppo_date.find('span', attrs={'class': 'p-opponentCard__date-brackets'}).contents[0]
        # round
        round_info = soup.find('b', attrs={'class': 'p-opponentCard__round'}).contents[0]
        
        result.append(f"{match_date}{match_weekday} {round_info}")
        
        # players
        players = soup.find_all('li', attrs={'class': 'p-opponentCard__item'})
        for player in players:
            player_name = player.find('img')['alt']
            result.append(player_name)
        
        return result
        

if __name__ == '__main__':
    scraper = Scraper()
    match_info = scraper.get_match_info()
    print(match_info)
