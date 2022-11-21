import os

def build_conn_str(user, password, host, port, 
                       database, dbms='postgresql'):
    
    conn_str = f'{dbms}://{user}:{password}@{host}:{port}/{database}'
    
    return conn_str

def solve_dir(folder):

    if not os.path.exists(folder):
        os.mkdir(folder)

    return os.path.abspath(folder)


def solve_path(path, parent=None):
    
    if parent:
        parent = solve_dir(parent)
        path = os.path.join(parent, path)
    
    return os.path.abspath(path)
