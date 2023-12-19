from enum import Enum
from bs4 import BeautifulSoup
from request import Request

class Scraper():

    def __init__(self):
        self.request = Request()
    
    def _get_soup(self):
        data = self.request.request_html_content()
        return BeautifulSoup(data, 'html.parser')
    
    def get_match_info(self)->list[str]:
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
        

    def get_regualr_team_rank(self)->list[str]:
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

    class PersonalRankingType(Enum):
        SCORE = 0
        HIGHEST = 1
        LAST_AVOID_RATE = 2
    
    def get_personal_ranking(self, ranking_type:PersonalRankingType)->list[str]:
        soup = self._get_soup()

        column = soup.find_all('div', attrs={'class': 'p-ranking__personal-column'})[ranking_type.value]
        
        result = []
        
        # title
        title = column.find('h3', attrs={'class': 'p-ranking__personal-heading'}).contents[0]
        result.append(title)
        
        # heading
        headings = column.find('thead').find_all('th')
        heading = str()
        for th in headings:
            if th.contents:
                heading += f"|{th.contents[0]}|  "
            else:
                heading += "|Rate|" # last avoid rate missing last column heading
        
        result.append(heading)
        
        # table
        table = column.find_all('tr')[1:]
        for row in table:
            rank = row.find('div', attrs={'class': 'p-ranking__personal-number'}).contents[0].strip()
            player_name = row.find('div', attrs={'class': 'p-ranking__personal-name'}).contents[0].strip()
            point = row.find('td', attrs={'class': 'p-ranking__personal-point'}).contents[0].strip()
            result.append(f"{rank}. {player_name} {point}")
        
        return result

    def get_personal_score(self):
        return self.get_personal_ranking(self.PersonalRankingType.SCORE)
    
    def get_personal_highest(self):
        return self.get_personal_ranking(self.PersonalRankingType.HIGHEST)

    def get_last_avoid_rate(self):
        return self.get_personal_ranking(self.PersonalRankingType.LAST_AVOID_RATE)

if __name__ == '__main__':
    scraper = Scraper()
    match_info = scraper.get_match_info()
    print(match_info)
    team_ranking = scraper.get_regualr_team_rank()
    print(team_ranking)
    personal_score = scraper.get_personal_score()
    print(personal_score)
    personal_highest = scraper.get_personal_highest()
    print(personal_highest)
    last_avoid_rate = scraper.get_last_avoid_rate()
    print(last_avoid_rate)
