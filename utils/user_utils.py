import os

from dotenv import load_dotenv

load_dotenv()
TIME_BETWEEN_REQS = os.getenv("TIME_BETWEEN_REQUISITIONS")
STOP_CRITERIA = os.getenv("STOP_CRITERIA")


def welcome():
    print("\n\tCrawler MERCADO LIVRE!")
    print(
        "\nEste sistema de Recuperação de Informação foi desenvolvido com o objetivo de coletar dados do domínio "
        "mercadolivre.com.br"
        ""
    )
    print(f"O ponto de partida padrão é definido pelo usuário!")
    print(f"A busca será executada a cada {TIME_BETWEEN_REQS} segundo...")
    print(f"O critério de parada é {STOP_CRITERIA} itens...")
    print("\n")


def get_initial_url(name_item):
    initial_url = "https://lista.mercadolivre.com.br/" + name_item
    return initial_url

