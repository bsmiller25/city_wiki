'''
usage: python scraper.py "New York City"
'''
import wikipedia
import pandas as pd
from bs4 import BeautifulSoup
import sys
import re


def new_city(city):
    '''
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
    # website
    try:
        web_loc = panel[0][panel[0].str.contains('Website')].index.tolist()[0]
    except:
        web_loc = 'NA'
        
    # if the location exists, get the field value
    if gtype_loc != 'NA':
        gtype = panel[1][gtype_loc]
    else:
        gtype = 'NA'
    if mayor_loc != 'NA':
        mayor = panel[1][mayor_loc]
    else:
        mayor = 'NA'
    if web_loc != 'NA':
        website = panel[1][web_loc]
    else:
        website = 'NA'
    
    # find a photo
    photos = str(html.find_all(attrs={'class': 'image'})[0])
    try:
        img = 'https://upload.wikimedia.org{}.png'.format(
            re.findall('upload\.wikimedia\.org(.*?)\.png', photos)[0])
    except:
        try:
            img = 'https://upload.wikimedia.org{}.png'.format(
                re.findall('upload\.wikimedia\.org(.*?)\.jpg', photos)[0])
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
    
    print(new_city(sys.argv[1]))
    
