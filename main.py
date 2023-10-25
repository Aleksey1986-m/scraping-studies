import json
from unicodedata import normalize
import requests
import bs4
from  fake_headers import Headers
import time

keywords = ['Django', 'Flask']

headers_gen = Headers(browser='opera', os='win')
response = requests.get('https://spb.hh.ru/search/vacancy?text=Python+flask+django&salary=&ored_clusters=true&area=2&hhtmFrom=vacancy_search_list', headers=headers_gen.generate())
html = response.text
soup = bs4.BeautifulSoup(html, features='lxml')

vacancy_list_tag = soup.find('main', class_='vacancy-serp-content')
vacancy_tags = vacancy_list_tag.find_all('div', class_='serp-item')

vacancy_info = []
for vacancy_tag in vacancy_tags:
    h3_tag = vacancy_tag.find('h3')
    span_tag = h3_tag.find('span')
    a_tag = span_tag.find('a', class_='serp-item__title')

    company_block_info_tag = vacancy_tag.find('div', class_='vacancy-serp-item__info')
    company_name_tag = company_block_info_tag.find('a', class_='bloko-link bloko-link_kind-tertiary')

    city_name_tag = company_block_info_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})

    salary_tag = vacancy_tag.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

    headers = h3_tag.text
    link = a_tag['href']
    company_name = normalize('NFKD', company_name_tag.text)
    city_name = city_name_tag.text

    if salary_tag:
        salary = normalize('NFKD', salary_tag.text)
    else:
        salary = 'Не указана'
    time.sleep(0.1)
    vacancy_info.append({
        'link': link,
        'header': headers,
        'company-name': company_name,
        'city': city_name,
        'salary': salary
    })

if __name__ == '__main__':
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy_info, file, ensure_ascii=False)
