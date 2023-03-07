import requests
from bs4 import BeautifulSoup as BS
import csv

def get_categories_links_and_names(url):
    page = requests.get(url)
    soup = BS(page.text, "html.parser")
    links: list = []
    names: list = []
    for el in soup.findAll(class_='name-grid'):
        links.append(el.get('href'))
        names.append(el.text)
    return links, names

def get_things_blocks(url: str) -> list:
    page = requests.get(url)
    soup = BS(page.text, "html.parser")
    ans: list = []
    for el in soup.findAll(class_='product-layout'):
        ans.append(el)
    return ans

def get_thing_information(thing):
    s = {}

    s['Name'] = thing.find(class_ = 'caption').find(class_ = 'productTitle').text

    try:
        s['Old price'] = thing.find(class_ = 'caption').find(class_ = 'price-old').text
    except:
        s['Old price'] = thing.find(class_ = 'caption').find(class_ = 'price').text.strip()

    try:
        s['Sale'] = thing.find(class_ = 'sale').text
    except:
        s['Sale'] = 'Нет'

    try:
        s['New price'] = thing.find(class_ = 'caption').find(class_ = 'price-new').text
    except:
        s['New price'] = 'Нет'
        

    s['Link'] = thing.find(class_ = 'caption').find(class_ = 'productTitle').find('a').get('href')
    s['Image link'] = thing.find(class_ = 'product-thumb').find(class_ = 'image').find('a').find('img').get('src')
    return s

def main():
    links, names = get_categories_links_and_names('https://nestidno.ru/')
    fields = ['Name', 'Old price', 'Sale', 'New price', 'Link', 'Image link']

    for i in range(len(links)):
        positions = []
        
        for el in get_things_blocks(links[i]):
            positions.append(get_thing_information(el))

        with open(f'{names[i]}.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fields)
            writer.writerows(positions)

if __name__ == '__main__':
    main()