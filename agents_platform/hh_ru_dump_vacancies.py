import http.client
import datetime
import json
import re

#Providing headers as recomennded in API Documentation
headers = {"User-Agent": "HH-User-Agent"}

#function to get all the related vacancy ids
def get_vacancy_ids(keyword):
    vacancy_ids = []
    conn = http.client.HTTPSConnection("api.hh.ru")
    per_page = 100 #100 is a maximum allowed by API
    page = 0
    count = per_page
    date_from = (datetime.datetime.now() - datetime.timedelta(days=29)).strftime('%Y-%m-%dT%H:%M:%S')
    date_to = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    area_id = 113 #Russia
    
    while count == per_page:
        path = ("/vacancies?text={}&area={}&per_page={}&date_from={}&date_to={}&page={}"
                .format(keyword,area_id,per_page, date_from, date_to, page))
        
        conn.request("GET", path, headers=headers)
        resp = conn.getresponse()
        if resp.status != 200:
        # something went wrong
            raise ValueError('API error happened.')
        vacancies = resp.read()
        conn.close()

        count = len(json.loads(vacancies)['items'])
        page = page+1
        for item in json.loads(vacancies)['items']:
            vacancy_ids.append(item['id'])
    return vacancy_ids


#function to retrieve vacancy description for previously received vacancy ids.
def get_vacancies(vacancy_ids):
    vac_list = []
    for vac_id in vacancy_ids:
        conn = http.client.HTTPSConnection("api.hh.ru")
        conn.request("GET", "/vacancies/{}".format(vac_id), headers=headers)
        resp = conn.getresponse()
        if resp.status != 200:
        # something went wrong
            raise ValueError('API error happened.')
        vacancy_txt = resp.read()
        conn.close()
        vacancy = json.loads(vacancy_txt)
        dept=vacancy['department']
        if dept!=None:
#             print(dept, type(dept))
            dept_name=dept['name']
#             print(dept_name)
            vac_list.append(dept_name)
        #cleaning description out of html tags and other irrelevant charachters
        clean_desc = ''
    return vac_list
#     print('file corpus.txt with vacancies descriptions is created in the working directory')
        
ids = get_vacancy_ids("Data+Scientist")
# print (len(ids)) #print number of vacancies
get_vacancies(ids)
def get_search(name_vac): 
    name_vac = name_vac.replace(' ', '+')
    ids = get_vacancy_ids(name_vac)
    #print (len(ids)) #print number of vacancies
    result=get_vacancies(ids)
    result = set(result)
    return result
	