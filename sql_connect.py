import sqlalchemy as sql
import pandas as pd


def sql_connect():
    '''
    When working on my virtual box, localhost can't be specified
    When working on my remote server, localhost has to be specified
    I don't know, this is my hacky work-around
    '''
    # connect to sql backend
    engine = sql.create_engine('postgresql://localhost:5432/govex')
    # test connection
    try:
        test = pd.read_sql_query('SELECT * FROM city_wiki LIMIT 1', engine)
    except:
        engine = sql.create_engine('postgresql:///govex')
    return(engine)
