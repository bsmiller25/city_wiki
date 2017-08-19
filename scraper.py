'''
usage: python scraper.py "New York City"

'''
import wikipedia
import pandas as pd
from bs4 import BeautifulSoup
import sys
import re
import os
import sqlalchemy as sql

def scrape_city(city):
    '''
    scrape wikipedia taking the first result matching the search of city
    this can be called from the browser
    '''
    # find right page
    options = wikipedia.search(city)
    choice = options[0]
    
    # isolate html for govt panel
    page = wikipedia.page(choice)
    html = BeautifulSoup(page.html(), "lxml")
    card = html.find_all('table')[0]
    df = pd.read_html(str(card))
    panel = df[0]
    
    # parse  gov't fields
    # government type
    try:
        gtype_loc = panel[0][panel[0].str.contains('Type')].index.tolist()[0]
    except:
        gtype_loc = 'NA'
    # mayor's name
    try:
        mayor_loc = panel[0][panel[0].str.contains('Mayor')].index.tolist()[0]
    except:
        mayor_loc = 'NA'
        
    # if the location exists, get the field value
    if gtype_loc != 'NA':
        gtype = panel[1][gtype_loc]
    else:
        gtype = 'NA'
    if mayor_loc != 'NA':
        mayor = panel[1][mayor_loc]
    else:
        mayor = 'NA'
    
    # get the website
    website = card.find_all('a')[-1]['href']
    
    # find a photo
    photos = str(html.find_all(attrs={'class': 'image'})[0])
    try:
        img = 'https://upload.wikimedia.org{}.png'.format(
            re.findall('upload\.wikimedia\.org(\S*?)\.png"', photos)[0])
    except:
        try:
            img = 'https://upload.wikimedia.org{}.jpg'.format(
                re.findall('upload\.wikimedia\.org(\S*?)\.jpg"', photos)[0])
        except:
            img = 'NA'
    
    # create dataframe for adding to sql
    tosql = pd.DataFrame({'city': city,
                          'type': gtype,
                          'mayor': mayor,
                          'website': website,
                          'img': img}, index=[0])
    
    engine = sql.create_engine(os.getenv('DATABASE_URL'))
    tosql.to_sql('city_wiki', engine, if_exists='append', index=False)


def scrape_city_manual(city):
    '''
    run from command line
    let's the user choose which wikipedia page to reference
    '''
    # find right page
    print('Which wikipedia entry do you mean?')
    options = wikipedia.search(city)
    [print('{}: {}'.format(i, options[i])) for i in range(len(options))]
    selection = int(input('Enter number: '))
    choice = options[selection]
    print('Scraping wikipedia page for: {}'.format(choice))
    
    # isolate html for govt panel
    page = wikipedia.page(choice)
    html = BeautifulSoup(page.html(), "lxml")
    card = html.find_all('table')[0]
    df = pd.read_html(str(card))
    panel = df[0]
    
    # parse  gov't fields
    # government type
    try:
        gtype_loc = panel[0][panel[0].str.contains('Type')].index.tolist()[0]
    except:
        gtype_loc = 'NA'
    # mayor's name
    try:
        mayor_loc = panel[0][panel[0].str.contains('Mayor')].index.tolist()[0]
    except:
        mayor_loc = 'NA'
        
    # if the location exists, get the field value
    if gtype_loc != 'NA':
        gtype = panel[1][gtype_loc]
    else:
        gtype = 'NA'
    if mayor_loc != 'NA':
        mayor = panel[1][mayor_loc]
    else:
        mayor = 'NA'
    
    # get the website
    website = card.find_all('a')[-1]['href']
    
    # find a photo
    photos = str(html.find_all(attrs={'class': 'image'})[0])
    try:
        img = 'https://upload.wikimedia.org{}.png'.format(
            re.findall('upload\.wikimedia\.org(\S*?)\.png"', photos)[0])
    except:
        try:
            img = 'https://upload.wikimedia.org{}.jpg'.format(
                re.findall('upload\.wikimedia\.org(\S*?)\.jpg"', photos)[0])
        except:
            img = 'NA'
    
    # create dataframe for adding to sql
    tosql = pd.DataFrame({'city': city,
                          'type': gtype,
                          'mayor': mayor,
                          'website': website,
                          'img': img}, index=[0])
    
    return(tosql)
 

if __name__ == '__main__':
    engine = sql.create_engine(os.getenv('DATABASE_URL'))
    city = scrape_city_manual(sys.argv[1])
    print('Writing to sql')
    city.to_sql('city_wiki', engine, if_exists='append', index=False)
    print('Done')
