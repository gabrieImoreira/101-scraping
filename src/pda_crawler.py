import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

class PaoDeAcucarCrawl():
    def __init__(self):
        self.api_key = 'paodeacucar'
        self.page = 1
        self.results_per_page = 100
        self.http = self._get_session()
    
    def _get_session(self):
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session
    
    def get_total_pages(self, content):
        pages = content['pagination']['last'].split("&page=")[-1].split("&")[0]
        return int(pages) + 1

    def start(self, term):
        content = self.search_products(term)
        pages = self.get_total_pages(content)
        for page in range(2, pages):
            self.page = page
            content['products'] += self.search_products(term)['products']

        return self.get_products(content)
    
    def search_products(self, term):
        try: 
            url = f'https://api.linximpulse.com/engage/search/v3/search?apikey={self.api_key}&origin=https://www.paodeacucar.com&page={self.page}&resultsPerPage={self.results_per_page}&terms={term}&allowRedirect=true&salesChannel=461&salesChannel=catalogmkp&sortBy=relevance&filter=d:3718:3719'
            response = self.http.get(url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                raise Exception('Error on request')
        except:
            raise Exception('Error on request')

    def get_products(self, content):
        products = []
        for product in content['products']:
            products.append({
                'name': product['name'],
                'price': product['price'],
                'old_price': product['oldPrice'],
                'url': product['url'],
                'image': product['images']['default'],
                'category': product['categories']
            })
        return products


# Test the crawler with the term
crawler = PaoDeAcucarCrawl()
content = crawler.start('vinho')
print(json.dumps(content, indent=4, sort_keys=True))