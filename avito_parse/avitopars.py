import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from bingmaps.apiservices import LocationByQuery

def get_html(url):
    r = requests.get(url)
    return r.text


def get_page_numbers(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_="catalog-content").find_all('a', class_="pagination-page")[-1].get('href').split('=')[1]
    return pages

def get_data(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('div', class_="catalog-content").find_all('div', class_="description item_table-description snippet-experiment-wrapper")
    df = pd.DataFrame(columns=('title', 'price', 'area', 'link'))
    
    for n, i in enumerate(content):
        try:
            title = i.find('h3', class_="title item-description-title").text.strip()
        except:
            title = ''
        try:
            price = i.find('span', class_="price").text.strip().replace(" ","").replace("₽", "")
        except:
            price = ''
        try:
            area = i.find('p', class_="address").text.strip()
        except:
            area = ''
        try:
            link = "https://www.avito.ru" + i.find('a', class_="item-description-title-link").get('href')
        except:
            link =''
        df.loc[n] = [title, price, area, link]
    return df

def main(url):
    main_url_part = url
    pages = get_page_numbers(url)
    df = pd.DataFrame(columns=('title', 'price', 'area', 'link'))
    for i in range(1, int(pages)+1):
        df = df.append(get_data(main_url_part+str(i)))
        sleep(15)
        print(df)
    return df
    

def get_location_by_adress(query):
    key = 'AgcVYmjfwxWBgQBPEQPyRI6b1AcYG7TfwCrC-AlqobSZVOACADEBikizH9uo28ax'
    data = {'q': query, 'key': key}
    loc_by_query = LocationByQuery(data)
    return loc_by_query.get_coordinates


data = pd.read_excel(r'D:\Github\areas.xlsx')
lat = []
long = []
for a in data["area"]:
    try:
        loc = get_location_by_adress(a)[0]
        lat.append(loc[0])
        long.append(loc[1])
    except:
        loc = ''
        lat.append("")
        long.append("")

data["lat"] = lat
data["long"] = long








get_location_by_adress("р-н Октябрьский, ул Астрономическая, 26")

df = main("https://www.avito.ru/rostov-na-donu/zemelnye_uchastki/prodam/izhs?p=")




key = ''
data = {'q': '7266 Canterbury Court Oshkosh, WI 54901', 'key': key}
loc_by_query = LocationByQuery(data)
print(loc_by_query.status_code)



if __name__ == '__main__':
    main()