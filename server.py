from flask import Flask
from flask import render_template
import sqlalchemy as sql
import pandas as pd
import json
app = Flask(__name__)


@app.route('/city/<int:cid>')
def index(cid):
        # connect to sql backend
        engine = sql.create_engine('postgresql://localhost:5432/govex')
        
        # get city ids
        query = "SELECT city FROM city_wiki;"
        cities = pd.read_sql_query(query, engine)['city']
        
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


