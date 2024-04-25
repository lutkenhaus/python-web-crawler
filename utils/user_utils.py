import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
TIME_BETWEEN_REQS = os.getenv("TIME_BETWEEN_REQUISITIONS")
STOP_CRITERIA = os.getenv("STOP_CRITERIA")


def welcome():
    print("\n\tCrawler MERCADO LIVRE!")
    print(
        "\nEste sistema de Recuperação de Informação foi desenvolvido com o objetivo de coletar dados do domínio "
        "lista.mercadolivre.com.br"
        ""
    )
    print(
        "\nO ponto de partida padrão é: " "https://lista.mercadolivre.com.br/cadeira" ""
    )
    print("\nA busca será executada a cada " + TIME_BETWEEN_REQS + " segundo...")
    print("\nO critério de parada é " + STOP_CRITERIA + " itens...")
    print("\n")
