from scraper.scraper import get_soup, get_data, get_rooms
import csv

def attempt(url):
    soup_file = get_soup(url)
    extract = get_data(soup_file, url)
    all_data = get_rooms(extract)
    return all_data

# make a list of urls out of a csv file
list_1 = []
csv_input_path = "data/first_1000_urls.csv"
with open(csv_input_path, mode='r', newline='') as file:
    line = file.readline()
    list_1 = line.strip().split(",")

list_raw_1 = []
for i in list_1:
    list_raw_1.append(attempt(i))


# remove dictionaries with life sales
list_raw_1 = [d for d in list_raw_1 if 'Maandelijkse rente' not in d]
# Remove dictionaries without price value (=sold)
list_raw_1 = [d for d in list_raw_1 if d.get('price')]
# remove all keys except for 17 must-haves
columns = ['property_type', 'price', 'property_id', 'postal_code', 'locality_name', 'property_subtype', 'Staat van het gebouw', 'Aantal gevels', 'Bewoonbare oppervlakte', 'Type keuken', 'Oppervlakte tuin', 'Oppervlakte terras', 'Gemeubeld', 'Aantal open haarden', 'Zwembad', 'rooms', 'sale_type']
list_raw_1 = [{key: value for key, value in d.items() if key in columns} for d in list_raw_1]
# remove keys with empty values ('Niet gespecificeerd', '')
list_raw_1 = [{key: value for key, value in d.items() if value not in ('', 'Niet gespecificeerd')} for d in list_raw_1]
# replace values 'Ja' with '1', and 'Nee' with '0'
list_raw_1 = [{key: (True if value == 'Ja' else value) for key, value in d.items()} for d in list_raw_1]
list_raw_1 = [{key: (False if value == 'Nee' else value) for key, value in d.items()} for d in list_raw_1]
# Setting specified values to True/False
list_raw_1 = [{
        **d,  # Keep all existing key-value pairs
        'Aantal open haarden': d.get('Aantal open haarden', 0) != 0,
        'Zwembad': d.get('Zwembad', 'Nee') == 'Ja',
        'Type keuken': len(d.get('Type keuken', '')) > 3,
        'Gemeubeld': d.get('Gemeubeld', 'Nee') == 'Ja'
    } for d in list_raw_1]
# setting specified values to null if not present
list_raw_1 = [{
        **d,
        **{key: d.get(key, 'null') for key in ['Oppervlakte tuin', 'Oppervlakte terras']}} for d in list_raw_1]


# Collect all unique keys for columns
all_keys = set()
for i in list_raw_1:
    all_keys.update(i.keys())
# Write dictionaries to CSV
with open('output1.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
    writer.writeheader()
    for i in list_raw_1:
        writer.writerow(i)

