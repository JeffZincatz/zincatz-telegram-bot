import requests
import re

def request(url:str, method:str="GET", headers:dict = {}, body:dict = {}):
    return requests.request(method, url, headers=headers, data=body)

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

def get_match_info()-> list:
    response = request("https://m-league.jp/")
    data = response.content
    
    match_info = []
    
    date_info = data.split(b'<div class="p-opponentCard__date" >')[1]
    date_info = date_info.split(b'</div>')[0].decode()
    
    date, weekday = process_date_info(date_info).decode().split()[0:2]

    round_info = data.split(b'<b class="p-opponentCard__round">')[1]
    round_info = round_info.split(b'</b>')[0].decode()
    
    match_info.append(f"{date}{weekday} {round_info}")
    
    data = data.split(b'<ul class="p-opponentCard__list">')[1]
    data = data.split(b'</ul>')[0]
    data = data.split(b'alt=')[1:]
    
    for each in data:
        end_of_first_str = each.index(b'"', 1)
        match_info.append(each[1:end_of_first_str].decode('utf-8'))
    
    return match_info

if __name__ == "__main__":
    match_info = get_match_info()
    print(match_info)
    