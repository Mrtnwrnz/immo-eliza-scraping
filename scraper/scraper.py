import requests
from bs4 import BeautifulSoup

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html")
    return soup

def get_data(soup, url):
    data_dict = {}
    url_split = url.split("/")
    # add price
    price_element = soup.find("p", attrs={"class": "classified__price"})
    if price_element:
        price = price_element.text.split(" ")[-1].strip()
        if price[-1] == "€":
            price = price[:-1]
        data_dict["price"] = price
    else:
        data_dict["price"] = ''
    # add data from url
    data_dict["property_id"] = url_split[-1]
    data_dict["postal_code"] = url_split[-2]
    data_dict["locality_name"] = url_split[-3]
    data_dict["property_subtype"] = url_split[-5]
    # add all data from classified table
    rows = soup.find_all('tr', class_='classified-table__row')
    for row in rows:
        header = row.find('th', class_='classified-table__header')
        data_cell = row.find('td', class_='classified-table__data')
        if header and data_cell:
            header_key = header.contents[0].strip()
            data_cell_value = data_cell.contents[0].strip()
        else:
            pass
        data_dict[header_key] = data_cell_value
    return data_dict

def get_rooms(data_dict):
    rooms = 0
    if 'Oppervlakte woonkamer' in data_dict.keys():
        rooms +=1
    if 'Oppervlakte keuken' in data_dict.keys():
        rooms +=1
    if 'Slaapkamers' in data_dict.keys():
        rooms += int(data_dict['Slaapkamers'])
    if 'Badkamers' in data_dict.keys():
        rooms += int(data_dict['Badkamers'])
    if 'Kelder' in data_dict.keys():
        rooms +=1
    data_dict['rooms'] = rooms
    return data_dict