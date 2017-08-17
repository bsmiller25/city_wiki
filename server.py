from flask import Flask, render_template, redirect, request, url_for
import sqlalchemy as sql
import pandas as pd
app = Flask(__name__)


@app.route('/city/<int:cid>')
def city_page(cid):
    # connect to sql backend
    engine = sql.create_engine('postgresql://localhost:5432/govex')
    
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
    

@app.route("/redir", methods=["GET", "POST"])
def redir():
    # data from POST
    nc = request.form.get('new_cid')
    if nc == "":
        return redirect(request.referrer)
    # connect to sql backend
    engine = sql.create_engine('postgresql://localhost:5432/govex')
    # get city ids
    query = "SELECT city FROM city_wiki;"
    cities = pd.read_sql_query(query, engine)
    cities['cid'] = list(range(len(cities)))
    cid = cities['cid'][cities['city'] == nc]
    
    return redirect(url_for('city_page', cid=cid))
