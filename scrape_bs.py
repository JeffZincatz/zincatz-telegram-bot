from bs4 import BeautifulSoup
from request import Request

class Scraper():

    def __init__(self):
        self.request = Request()
    
    def _get_soup(self):
        data = self.request.request_html_content()
        return BeautifulSoup(data, 'html.parser')
    
    def get_match_info(self):
        soup = self._get_soup()
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
        

    def get_regualr_team_rank(self):
        soup = self._get_soup()
        result = ["|Rank|  |Team|  |Points|  |Difference|"]
        
        # teams
        teams = soup.find_all('div', attrs={'class': 'p-ranking__team-item'})
        for team in teams:
            rank = team.find('div', attrs={'class': 'p-ranking__rank-number'}).contents[0]
            team_name = team.find('img')['alt']
            current_point = team.find('div', attrs={'class': 'p-ranking__current-point'}).contents[0]
            diff_point = team.find('div', attrs={'class': 'p-ranking__diff-point'}).contents[0].strip()
            result.append(f"{rank}. {team_name} {current_point} {diff_point}")
        
        return result
    
if __name__ == '__main__':
    scraper = Scraper()
    # match_info = scraper.get_match_info()
    # print(match_info)
    team_ranking = scraper.get_regualr_team_rank()
    print(team_ranking)
