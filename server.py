from flask import Flask
from flask import render_template
import sqlalchemy as sql
import pandas as pd
import os
app = Flask(__name__)


@app.route('/')
def index(city='New York City'):
        engine = sql.create_engine('postgresql://localhost:5432/govex')
        query = "SELECT * FROM city_wiki WHERE city = '{}';".format(city)
        city_data = pd.read_sql_query(query, engine)
        return render_template('index.html',
                               title='title',
                               city=city,
                               mayor=city_data['mayor'][0],
                               img=city_data['img'][0])
