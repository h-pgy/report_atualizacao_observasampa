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
