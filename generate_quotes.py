from api import API_NINJAS_KEY

from requests import get, codes


class QuoteGenerator:
    def generate_quote(self, category):
        headers = {
            'X-Api-Key':API_NINJAS_KEY
        }
        api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'

        r = get(api_url, headers=headers)
        if r.status_code == codes.ok:
            r = r.json()
            return (r[0]["quote"], r[0]["author"])
