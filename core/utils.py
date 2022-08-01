import os
import json

def solve_dir(folder):

    if not os.path.exists(folder):
        os.mkdir(folder)
    
    return os.path.abspath(folder)

def solve_path(path, parent = None):

    if parent:
        parent = solve_dir(parent)
        path = os.path.join(parent, path)

    return os.path.abspath(path)

def solve_path_relative(path, parent):

    if not os.path.exists(parent):
        os.mkdir(parent)

    return os.path.join(parent, path)

def list_files(folder, extension=None):

    folder = solve_path(folder)
    files = [os.path.join(folder, file) for file in os.listdir(folder)]
    
    if extension is not None:
        return [f for f in files if f.endswith(extension)]
    
    return files


def load_file_generator(folder, extension=None, read_type='r'):

    read_modes = ('r', 'rb')
    if read_type not in read_modes:
        raise ValueError(f'Read type must be in {read_modes}')

    files = list_files(folder, extension)
    for file in files:
        with open(file, read_type) as f:
            yield {'file' : file, 
                'content': f.read()}

def delete_existing_files(folder, extension=None):

    folder = solve_dir(folder)

    files = list_files(folder, extension)
    if files:
        print('Found existing files')
    for file in files:
        os.remove(file)
        print(f'File {file} deleted.')


def save_file(obj, file_name, save_dir, callback=None):

    file_name = solve_path(file_name, parent=save_dir)

    if callable(callback):
        return callback(file_name, obj)

    if callback is None or callback == 'text':
        with open(file_name, 'w') as f:
            f.write(obj)
    elif callback == 'json':
        with open(file_name, 'w') as f:
            json.dump(obj, f)
    elif callback == 'bin':
        with open(file_name, 'wb') as f:
            f.write(obj)
    
    return file_name


def remover_acentos(name):
    
    acento_letra = {
        'ç' : 'c',
        'á' : 'a',
        'â' : 'a',
        'à' : 'a',
        'ã' : 'a',
        'ä' : 'a',
        'é' : 'e',
        'ê' : 'e',
        'è' : 'e',
        'ë' : 'e',
        'í' : 'i',
        'î' : 'i',
        'ì' : 'i',
        'ï' : 'i',
        'ó' : 'o',
        'ô' : 'o',
        'ò' : 'o',
        'ø' : 'o',
        'õ' : 'o',
        'ö' : 'o',
        'ú' : 'u',
        'û' : 'u',
        'ù' : 'u',
        'ü' : 'u',
        'ñ' : 'n',
        'ý' : 'y'
    }
    
    chars = list(name)
    
    return ''.join([acento_letra.get(char, char) for char in chars])
