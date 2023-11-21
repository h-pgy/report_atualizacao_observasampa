from dotenv import load_dotenv
import os


def get_env_var(varname:str)->str:

    load_dotenv()
    try:
        return os.environ[varname]
    except KeyError:
        raise ValueError(f'Env var {varname} not defined.')

def get_conn_data():

    conn_data = dict(dbname=get_env_var('DATABASE'),
                    user=get_env_var('USER'),
                    password=get_env_var('PASSWORD'),
                    host=get_env_var('HOST'),
                    port=get_env_var('PORT')
                    )
    
    return conn_data

CONNECTION_DATA = get_conn_data()