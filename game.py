import math
from datetime import datetime
from api import RestCountriesAPI
from utils import normalizar

class Game:
    def __init__(self):
        self.api = RestCountriesAPI()
        self.pais = None
        self.inicio = None
        self.pontos = 0

    def nova_rodada(self):
        self.pais = self.api.buscar_pais()
        self.inicio = datetime.now()
        return self.pais

    def verificar(self, resposta):
        resposta = normalizar(resposta)

        nomes = [
            normalizar(self.pais["name"]["common"])
        ]

        try:
            nomes.append(
                normalizar(self.pais["translations"]["por"]["common"])
            )
        except KeyError:
            pass

        if resposta in nomes:
            tempo = (datetime.now() - self.inicio).total_seconds()
            base = math.floor(1000 / max(tempo, 1))
            populacao = self.pais.get("population", 1)
            bonus = math.log(populacao, 10)

            pontos = int(base / bonus)
            self.pontos += pontos
            return True, pontos

        return False, 0
