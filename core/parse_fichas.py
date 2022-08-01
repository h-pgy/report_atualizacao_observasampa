from bs4 import BeautifulSoup
import pandas as pd
from .utils import load_file_generator, remover_acentos, solve_path
from .exceptions import FichaForaPadrao

class FichaParser:

    def make_soup(self, html):

        return BeautifulSoup(html, features='lxml')

    def get_first_table(self, sopa):

        table = sopa.find('table')

        if table is None:
            raise FichaForaPadrao()

        return table

    def clean_text(self, text):

        t = text.lower()
        t = t.strip()
        t = t.replace(' ', '_')
        t = t.replace('\n', '')
        t = remover_acentos(t)
        t = t.strip()

        return t

    def parse_table(self, table):

        parsed = {}
        for row in table.find_all('tr'):
            key, val = row.find_all('td')
            key = self.clean_text(key.text)
            parsed[key] = val.text.strip()
        
        return parsed
    
    
    def __call__(self, html):

        sopa = self.make_soup(html)
        table = self.get_first_table(sopa)

        return self.parse_table(table)



def parse_all_fichas(data_dir = 'original_data', save_csv = True,
                    save_dir = 'generated_data'):

    html_files = load_file_generator(data_dir, '.html')
    parse_ficha = FichaParser()
    parsed_data = []
    for file in html_files:
        fname = file['file']
        html = file['content']
        try:
            parsed = parse_ficha(html)
            parsed['original_file'] = fname
            parsed['sucess'] = True
            
        except:
            parsed = {}
            parsed['original_file'] = fname
            parsed['sucess'] = False
        
        parsed_data.append(parsed)

    df = pd.DataFrame(parsed_data)

    if save_csv:
        fname = solve_path('fichas_parseadas.csv', parent=save_dir)
        df.to_csv(fname, encoding='utf-8', sep=';')


    return df

