from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

pd.set_option('display.max_columns', None)


def create_df():
    return pd.DataFrame(columns=('country', 'iso', 'capital', 'area', 'nominal_gdp_in_USD', 'currency'))

df = create_df()

url_countries = "https://en.wikipedia.org/wiki/List_of_sovereign_states"
headers = {
        'User-Agent': 'user_access'
    }
html_text = requests.get(url_countries, headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')
alldata = soup.select('tr > td > b > a')
count = 0
for data in alldata:
    #if count == 5:
    #    break
    url = 'https://en.wikipedia.org' + data['href']
    headers = {
        'User-Agent': 'user_access'
    }
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    country = soup.find('h1', class_='firstHeading mw-first-heading').text
    titles = soup.find_all('th', class_='infobox-label')

    capital = None
    currency = None
    iso = None
    area = None
    gdp = None
    for title in titles:
        if "Capital" in title.text:
            capital = title.next_sibling.a.text
        if "Currency" in title.text:
            currency = title.next_sibling.a.text
        if "ISO 3166 code" in title.text:
            iso = title.next_sibling.a.text
    area_lines = soup.find_all('th', class_='infobox-header')
    for aline in area_lines:
        if 'Area' in aline.text:
            area_unedit = aline.parent.next_sibling.td.text.rsplit('km2', 1)[0] + 'km2'
            area = re.sub('\[.+\]','',area_unedit)
    gdp_lines = soup.find_all('th', class_='infobox-label')
    for gline in gdp_lines:
        if 'GDP (nominal)' in gline.text:
            gdp_unedit = gline.parent.next_sibling.td.text
            gdp = re.sub('\[.+', '', gdp_unedit)

    df = df.append({'country': country, 'iso': iso, 'capital': capital, 'area': area, 'nominal_gdp_in_USD': gdp, 'currency': currency}, ignore_index=True)
    #count = count + 1
print(df)