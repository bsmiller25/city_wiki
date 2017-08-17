from flask import Flask, render_template, redirect, request, url_for
import sqlalchemy as sql
import pandas as pd
from sql_connect import sql_connect
import scraper
app = Flask(__name__)


@app.route('/city/<int:cid>')
def city_page(cid):
    '''
    The main page of this webtool. Displays city data scraped from wikipedia
    '''
    # connect to psql
    engine = sql_connect()
    
    # get city ids
    query = "SELECT city FROM city_wiki;"
    cities = pd.read_sql_query(query, engine)['city']
    
    # get chosen city data
    query = "SELECT * \
    FROM city_wiki \
    WHERE city = '{}';".format(cities[cid])
    city_data = pd.read_sql_query(query, engine)
    
    return render_template('index.html',
                           title='City-Wiki',
                           city=cities[cid],
                           mayor=city_data['mayor'][0],
                           gtype=city_data['type'][0],
                           img=city_data['img'][0],
                           website=city_data['website'][0],
                           cities=cities)
    

@app.route('/new_city', methods=["GET", "POST"])
def new_city():
    '''
    url endpoint for adding a new city
    '''
    return render_template('new_city.html',
                           title='City-Wiki')

@app.route('/creator', methods=["GET", "POST"])
def creator():
    '''
    url endpoint for scraping new information from wikipedia
    '''
    # data from post
    name = request.form.get('newname')
    # run the scraper on the input
    #scraper.new_city(name)

    # connect to sql backend
    engine = sql_connect()
    # get city ids
    query = "SELECT city FROM city_wiki;"
    cities = pd.read_sql_query(query, engine)
    cities['cid'] = list(range(len(cities)))
    cid = cities['cid'][len(cities) - 1]
    return redirect(url_for('city_page', cid=cid))

@app.route("/redir", methods=["GET", "POST"])
def redir():
    '''
    gateway for redirecting
    '''
    # data from POST
    nc = request.form.get('new_cid')
    if nc == "":
        return redirect(request.referrer)
    elif nc == "other":
        return redirect(url_for('new_city'))
    # connect to sql backend
    engine = sql_connect()
    # get city ids
    query = "SELECT city FROM city_wiki;"
    cities = pd.read_sql_query(query, engine)
    cities['cid'] = list(range(len(cities)))
    cid = cities['cid'][cities['city'] == nc]
    
    return redirect(url_for('city_page', cid=cid))
