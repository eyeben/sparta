import re
import requests
from bs4 import BeautifulSoup



def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantexts = re.split(cleanr, raw_html)
    lists=[]
    for i in cleantexts:
        if(i!='' and i!='\n'):
            lists.append(i)
    if len(lists)!=0:
        return lists


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


def get_context(url_comes_here, range_comes_here):
    data_list=[]
    source = requests.get(url_comes_here, headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(source.text, 'html.parser')
    # select를 이용해서, tr들을 불러오기
    first_data = soup.select(range_comes_here)
    print(first_data)
    for i in first_data:
        data_list.append(cleanhtml(str(i)))
    return data_list


print(get_context('http://spartacodingclub.shop/homework','html'))
