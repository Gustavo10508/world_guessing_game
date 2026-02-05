import requests
import random

class RestCountriesAPI:
    URL = (
        "https://restcountries.com/v3.1/all"
        "?fields=name,capital,region,translations,population"
    )

    def buscar_pais(self):
        resposta = requests.get(self.URL, timeout=10)
        resposta.raise_for_status()
        return random.choice(resposta.json())
