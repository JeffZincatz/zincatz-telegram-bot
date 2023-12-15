import requests


def request(url:str, method:str="GET", headers:dict = {}, body:dict = {}):
    return requests.request(method, url, headers=headers, data=body)


def request_html_content():
    # html content, binary
    data = request("https://m-league.jp/").content
    with open("ml.html", "wb") as f:
        f.write(data)
    return data


def get_match_info()-> list:
    data = request_html_content()

    match_info = []

    # date
    def process_date_info(date_info:bytes):
        result = b''
        inside = False
        for each in date_info:
            each = each.encode()
            if not inside:
                if each == b"<":
                    inside = True
                else:
                    result += each
            else:
                if each == b">":
                    inside = False
        return result
    
    date_info = data.split(b'<div class="p-opponentCard__date" >')[1]
    date_info = date_info.split(b'</div>')[0].decode()
    
    date, weekday = process_date_info(date_info).decode().split()[0:2]

    # round of the day
    round_info = data.split(b'<b class="p-opponentCard__round">')[1]
    round_info = round_info.split(b'</b>')[0].decode()
    
    match_info.append(f"{date}{weekday} {round_info}")
    
    # opponent
    data = data.split(b'<ul class="p-opponentCard__list">')[1]
    data = data.split(b'</ul>')[0]
    data = data.split(b'alt=')[1:]
    
    for each in data:
        end_of_first_str = each.index(b'"', 1)
        match_info.append(each[1:end_of_first_str].decode('utf-8'))
    
    return match_info

def get_regualr_team_rank()->list:
    data = request_html_content()
    
    data = data.split(b'<ol class="p-ranking__team-list -regular">')[1]
    data = data.split(b'</ol>')[0]
    
    team_ranking = ["|Rank|  |Team|  |Points|  |Difference|"]
    
    raw_teams = data.split(b'alt=')[1:]
    for i, team in enumerate(raw_teams):
        _, team_name, temp = team.split(b'"', 2)
        temp = temp.split(b'<div class="p-ranking__current-point">')[1]
        points, temp = temp.split(b'</div>', 1)
        temp = temp.split(b'<div class="p-ranking__diff-point">')[1]
        diff, temp = temp.split(b'</div>', 1)
        
        result = team_name + b' ' + points + b' ' + diff
        team_ranking.append(str(i+1) + ". " + result.decode().strip())

    return team_ranking

if __name__ == "__main__":
    # match_info = get_match_info()
    # print(match_info)
    
    regular_team_rank = get_regualr_team_rank()
    print(regular_team_rank)
    