from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time

pd.set_option('display.max_columns', None)


def create_df():
    return pd.DataFrame(columns=('country', 'iso', 'capital', 'area', 'nominal_gdp_in_USD', 'currency'))


def get_request(url):
    headers = {
        'User-Agent': 'user_access'
    }
    response = requests.get(url, headers=headers)
    html_text = response.text
    return BeautifulSoup(html_text, 'lxml')


def get_data(soup):
    capital = None
    currency = None
    iso = None
    titles = soup.find_all('th', class_='infobox-label')
    for title in titles:
        if "Capital" in title.text:
            capital = title.next_sibling.a.text
        if "Currency" in title.text:
            currency = title.next_sibling.a.text
        if "ISO 3166 code" in title.text:
            iso = title.next_sibling.a.text
    return capital, currency, iso


def get_area(soup):
    area = None
    area_lines = soup.find_all('th', class_='infobox-header')
    for aline in area_lines:
        if 'Area' in aline.text:
            area_unedit = aline.parent.next_sibling.td.text.rsplit('km2', 1)[0] + 'km2'
            area = re.sub('\[.+\]','',area_unedit)
    return area


def get_gdp(soup):
    gdp = None
    gdp_lines = soup.find_all('th', class_='infobox-label')
    for gline in gdp_lines:
        if 'GDP (nominal)' in gline.text:
            gdp_unedit = gline.parent.next_sibling.td.text
            gdp = re.sub('\[.+', '', gdp_unedit)
    return gdp


def wikipedia_country_data(first_n_countries = None):
    df = create_df()
    url_countries = "https://en.wikipedia.org/wiki/List_of_sovereign_states"
    soup_all = get_request(url_countries)
    countries_a_tag_list = soup_all.select('tr > td > b > a')
    countries_soup = []
    count = 0
    for country_a_tag in countries_a_tag_list:
        if first_n_countries != None :
             if count == first_n_countries:
                 break
        url = 'https://en.wikipedia.org' + country_a_tag['href']
        countries_soup.append(get_request(url))
        count = count + 1
    for country_soup in countries_soup:
        country = country_soup.find('h1', class_='firstHeading mw-first-heading').text
        capital, currency, iso = get_data(country_soup)
        area = get_area(country_soup)
        gdp = get_gdp(country_soup)
        df = df.append({'country': country, 'iso': iso, 'capital': capital, 'area': area, 'nominal_gdp_in_USD': gdp, 'currency': currency}, ignore_index=True)
    return df



df = wikipedia_country_data()
print(df)