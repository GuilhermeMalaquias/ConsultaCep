import sys
import time

import requests

BASE_URL = 'https://cep.awesomeapi.com.br/json/'
BASE_URL_ALT = 'https://viacep.com.br/ws/'
BASE_URL_MAPS = 'https://www.google.com/maps/search/?api=1&query='


SAIR = 1

class BotCep:
    __version__ = '1.1.1'

    def __init__(self):
        self.name_dev = 'Guilherme Malaquias'

    def search_zipcode_request(self, code):
        """
        Busca Cep!
        :zipcode: recebe uma string
        :return: string
        """
        req_zipcode = requests.get(f'{BASE_URL}{code}')
        if req_zipcode.status_code != 200:
            req_zipcode_alt = requests.get(f'{BASE_URL_ALT}{code}/json')
            if req_zipcode_alt.status_code != 200:
                return 'Cep nao encontrado'
            response_json_alt = req_zipcode_alt.json()
            return f'CEP: {response_json_alt["cep"].replace("-", "")}\n' \
                   f'Entereco: {response_json_alt["logradouro"]}\n' \
                   f'UF: {response_json_alt["uf"]}\n' \
                   f'Bairro: {response_json_alt["bairro"]}\n' \
                   f'Cidade: {response_json_alt["localidade"]}\n' \
                   f'Ir para o google maps: {BASE_URL_MAPS}{response_json_alt["cep"].replace("-", "")}'
        else:
            response = req_zipcode.json()
            return f'CEP: {response["cep"].replace("-", "")}\n' \
                   f'Entereco: {response["address"]}\n' \
                   f'UF: {response["state"]}\n' \
                   f'Bairro: {response["district"]}\n' \
                   f'Cidade: {response["city"]}\n' \
                   f'Ir para o google maps: {BASE_URL_MAPS}{response["cep"].replace("-", "")}'

    def get_zipcode(self, code: str) -> str:
        self.code = code
        self.code.replace("-", "")
        if len(self.code) != 8:
            raise ValueError('O CEP deve conter somente numeros!\nExemplo: 27273305')
        return self.code

    class Menu:

        def __init__(self):
            self.separador = '=' * 20

        def inicial_menu(self):
            return f'{self.separador}\n' \
                   f'ConsultaCEP\n' \
                   f'{self.separador} '

        def consultar_novamente_menu(self):
            return f'{self.separador}\n' \
                   f'0 - Consultar Novamente\n' \
                   f'1 - Sair\n' \
                   f'{self.separador}'


if __name__ == '__main__':
    Menu = BotCep.Menu()
    MainBot = BotCep()

    print(Menu.inicial_menu())
    print(f'Desenvolvedor: {MainBot.name_dev}')
    print(Menu.separador)
    while True:
        try:
            zipcode = input('Informe o CEP: ')
            print(Menu.separador)
            print(MainBot.search_zipcode_request(MainBot.get_zipcode(zipcode)))
        except ValueError as Erro:
            print(Erro)
        finally:
            print(Menu.consultar_novamente_menu())
            escolha_novamente_decisao = int(input('Escolha: '))
            if escolha_novamente_decisao == SAIR:
                print('Saindo...')
                time.sleep(1)
                break
            print(Menu.separador)
            continue


