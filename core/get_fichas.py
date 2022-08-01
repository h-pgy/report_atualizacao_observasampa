from requests import session
from bs4 import BeautifulSoup
from .utils import solve_dir, solve_path
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

        soup = BeautifulSoup(html)

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




    





    