# https://hh.ru /search/vacancy ?clusters=true& area=1& ored_clusters=true& enable_snippets=true& salary=& text=analyst
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
#from pprint import pprint

pos = input('Ведите должность: ')
pages = int(input('Сколько страниц просмотреть (введите число): '))
url = 'https://hh.ru'
params = {'clusters': 'true',
          'area': 1,
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'salary': None,
          'text': pos,
          'page': 0}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/94.0.4606.81 Safari/537.36'}
# response = requests.get(url + '/search/vacancy', params=params, headers=headers)
# dom = bs(response.text, 'html.parser')
vacancy_list = []
while params['page'] < pages:
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    if response.ok and vacancies:
        for vacancy in vacancies:
            vac_data = {}
            info = vacancy.find('a', {'class': 'bloko-link'})
            name = info.text
            company = vacancy.find('div', {'class': 'bloko-text bloko-text_small bloko-text_tertiary'}).text
            place = vacancy.find('div', {'class': 'bloko-text bloko-text_small bloko-text_tertiary'}).nextSibling.text
            link = info['href']
            site = url
            try:
                salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
                s = salary.split()
                if ' – ' in salary:
                    salary_min, salary_max, salary_cur = int(s[0]+s[1]), int(s[3]+s[4]), s[5]
                elif 'от' in salary:
                    salary_min, salary_max, salary_cur = int(s[1] + s[2]), None, s[3]
                elif 'до' in salary:
                    salary_min, salary_max, salary_cur = None, int(s[1] + s[2]), s[3]
                else:
                    salary_min, salary_max, salary_cur = int([0] + s[1]), int(s[0] + s[1]), s[2]
            except:
                salary = None
            vac_data['name'] = name
            vac_data['company'] = company
            vac_data['place'] = place
            vac_data['link'] = link
            vac_data['salary_min'] = salary_min
            vac_data['salary_max'] = salary_max
            vac_data['salary_cur'] = salary_cur
            vacancy_list.append(vac_data)
        print(f"Обработана {params['page']+1} страница")
        params['page'] += 1
    else:
        break

result = pd.DataFrame(vacancy_list)
result.to_excel(f'./vac-{pos}.xlsx')
print('End')


