from requests import session
from bs4 import BeautifulSoup
from .utils import save_file, solve_dir, solve_path
from .exceptions import FichaNotFound

class FichaDownload:

    domain = 'https://observasampa.prefeitura.sp.gov.br/'

    def __init__(self):

        self.s = session()

        #get homepage to fill cookiejar
        self.s.get(self.domain)


        self.endpoint = self.domain + 'fichaDoIndicador/Print/{ficha_num}'

    def download_ficha(self, num):

        url = self.endpoint.format(ficha_num=num)
        with self.s.get(url) as r:
            #mesmo para urls não encontradas, Prodam retorna status 200, ao invés de 404
            if r.status_code != 200: 
                raise(ValueError(f'Requisicao para {url} falhou.'))

            return r.text

    def make_soup(self, html):

        soup = BeautifulSoup(html, features="lxml")

        return soup

    def check_error_page(self, soup):

        body = soup.body

        return 'error-page-wrapper' in body.get('class', [])

    def __call__(self, num):

        html = self.download_ficha(num)
        sopa = self.make_soup(html)

        if self.check_error_page(sopa):
            raise FichaNotFound(f'Ficha {num} não encontrada.')
        
        return sopa


def download_all_fichas(start=1, end=1000, max_not_found = 10, 
                        save_dir = 'original_data', save_report=True):


    download_ficha = FichaDownload()
    not_found = []
    not_found_seguido = 0
    for i in range(start, end):

        try:
            sopa = download_ficha(i)
            html = sopa.prettify()
            fname = f'ficha_{i}.html'
            save_file(html, fname, save_dir, callback='text')
            not_found_seguido=0

        except FichaNotFound as e:

            not_found.append(i)
            not_found_seguido+=1

            if not_found_seguido >= max_not_found:
                break

    total_fichas = i-len(not_found)
    print("Finalizando download das fichas"
        f"{total_fichas} fichas baixadas")
        

    report = {'total_fichas' : total_fichas,
            'iteracoes' : i,
            'max_not_found' : max_not_found,
            'total_nao_encontradas' : len(not_found),
            'nao_encontradas' : not_found}
    
    print(report)

    if save_report:
        save_file(report, 'relatorio_download_fichas.json', 
                    save_dir='generated_data', callback='json')

    return report


    





    