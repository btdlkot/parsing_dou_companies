import requests
from bs4 import BeautifulSoup
import csv
import time

ts_1 = time.strftime("%d_%m_%Y")
CSV_1 = '{}_dou_companies.csv'.format(ts_1)
HEADERS_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

max_phones = 0
max_emails = 0

def get_html(url, params=''):
    r1 = requests.get(url + '/offices/', headers=HEADERS_1, params=params)
    return r1


def set_phones(items):
    if not items:
        return '-'
    _set = []
    for phone in items:
        _set.append(phone.get_text(strip=True))
    global max_phones
    if len(set(_set)) > max_phones:
        max_phones = len(set(_set))
    return set(_set)


def set_emails(items):
    if not items:
        return '-'
    _set = []
    for email in items:
        _set.append(deCFEmail(email.find('a').get('href')[28:]))
    global max_emails
    if len(set(_set)) >= max_emails:
        max_emails = len(set(_set))
    return set(_set)


def deCFEmail(fp):
    try:
        r = int(fp[:2],16)
        email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
        return email
    except (ValueError):
        pass


def get_content():
    with open('companies.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

    companies = soup.find_all('div', {"class": "company"})
    results = []
    for company in companies:
        url = company.find('a', {"class": "cn-a"}).get('href')
        name = company.find('a', {"class": "cn-a"}).get_text(strip=True)
        description = company.find('div', {"class": "descr"}).get_text(strip=True)
        company_page = BeautifulSoup(get_html(url).text, 'lxml')
        try:
            company_size = company_page.find('div', {"class": "company-info"}).get_text(strip=True, separator='|').split('|')[1]
        except:
            company_size = '-'
        try:
            website = company_page.find('div', {"class": "site"}).find('a').get('href')
        except:
            website = '-'
        if company_page.find_all('div', {"class": "phones"}):
            phones = list(set_phones(company_page.find_all('div', {"class": "phones"})))
        else:
            phones = None
        if company_page.find_all('div', {"class": "mail"}):
            emails = list(set_emails(company_page.find_all('div', {"class": "mail"})))
        else:
            emails = None
        company_profile = {
                'url': url,
                'name': name,
                'size': company_size,
                'description': description if description else '-',
                'website': website,
                'phones': phones,
                'emails': emails,
        }
        results.append(company_profile)
    return results


def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        first_row = ['URL', 'Name', 'Size', 'Description', 'Website']
        for n in range(1, max_phones+1):
            first_row.append(f'Phone{n}')
        for n in range(1, max_emails+1):
            first_row.append(f'Email{n}')
        writer.writerow(first_row)
        for item in items:
            item_row = [item['url'], item['name'], item['size'], item['description'], item['website']]
            items_in_max_range(item['phones'], max_phones, item_row)
            items_in_max_range(item['emails'], max_emails, item_row)
            writer.writerow(item_row)


def items_in_max_range(items, max_range, item_row):
    if items:
        for n in range(max_range):
            if n < len(items):
                item_row.append(items[n])
            else:
                item_row.append('-')
    else:
        for n in range(max_range):
            item_row.append('-')


start = time.monotonic()
save_doc(get_content(), CSV_1)
print(f'script_time = {time.monotonic() - start}')
print(max_phones)
print(max_emails)
