import requests
from bs4 import BeautifulSoup
from utils import excel_utils as excel, user_utils as user, time_utils as time
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
TIME_BETWEEN_REQS = int(os.getenv("TIME_BETWEEN_REQUISITIONS"))
STOP_CRITERIA = int(os.getenv("STOP_CRITERIA"))


allURLS = []
listaProdutos = []
listaUrls = []

user.welcome()
listaUrls.append(user.get_initial_url())

contador = 0
while contador <= STOP_CRITERIA:
    url_atual = listaUrls.pop(0)
    resposta = requests.get(url_atual)
    html_tratado = BeautifulSoup(resposta.content, "html.parser")

    produtosLinks = html_tratado.find_all(
        "a",
        class_="ui-search-item__group__element ui-search-link__title-card ui-search-link",
    )
    recomendationLinks = html_tratado.find_all(
        "a", class_="ui-recommendations-card__link"
    )

    for link in produtosLinks:
        url_nova = link["href"]
        if "mercadolivre" in url_nova:
            listaUrls.append(url_nova)

    for link in recomendationLinks:
        url_recomendada = link["href"]
        if "mercadolivre" in url_nova:
            listaUrls.append(url_recomendada)

    # se a URL atual for uma página de produto
    if url_atual.find("lista") == -1:
        produto = {}
        produto["nome"] = html_tratado.select_one(".ui-pdp-title").get_text()
        produto["preco"] = html_tratado.select_one(
            ".andes-money-amount__fraction"
        ).get_text()
        produto["url"] = url_atual
        listaProdutos.append(produto)
        allURLS.append(produto["url"])
        print("Documento coletado [" + str(contador) + "]: ")
        print("Nome: " + produto["nome"])
        print("Preço: R$" + produto["preco"])
        time.sleep(TIME_BETWEEN_REQS)
    contador = contador + 1
# FIM do loop

print("SALVANDO...")
excel.save_new_spreadsheet(listaProdutos, "dados_coletados")
excel.append_to_existing_spreadsheet(allURLS, "lista_urls")
