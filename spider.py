import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from utils import excel_utils as excel, user_utils as user, time_utils as time, indexacao as index, recovery

load_dotenv()
TIME_BETWEEN_REQS = int(os.getenv("TIME_BETWEEN_REQUISITIONS", "2"))
STOP_CRITERIA = int(os.getenv("STOP_CRITERIA", "5"))

allURLS = []
listaProdutos = []
listaUrls = []

user.welcome()
name_item = input("Digite o nome de um item: ")
listaUrls.append(user.get_initial_url(name_item))

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
    produto = {}
    # se a URL atual for uma página de produto
    if url_atual.find("lista") == -1:
        produto = {}
        produto["nome"] = html_tratado.select_one(".ui-pdp-title").get_text()
        # produto["preco"] = html_tratado.select_one(".andes-money-amount__fraction").get_text()
        produto["url"] = url_atual
        listaProdutos.append(produto)
        allURLS.append(produto["url"])
        print("Documento coletado [" + str(contador) + "]: ")
        print("Nome: " + produto["nome"])
        # print("Preço: R$" + produto["preco"])
        time.sleep(TIME_BETWEEN_REQS)
    contador = contador + 1

# Após coletar todos os dados, crie o índice invertido
sentences = [produto["nome"] for produto in listaProdutos]
inverted_index = index.create_inverted_index(sentences)

# Após coletar todos os dados, crie o índice invertido
inverted_index_dict = {k: dict(v) for k, v in inverted_index.items()}
output_path = os.path.join("inverted_index.json")
with open(output_path, 'w') as f:
    json.dump(inverted_index_dict, f, indent=4)

# FIM do loop
print("SALVANDO...")
print("Índice invertido salvo em 'inverted_index.json'")
excel.save_new_spreadsheet(listaProdutos, "dados_coletados")
excel.append_to_existing_spreadsheet(allURLS, "lista_urls")

inverted_index_path = os.path.join("inverted_index.json")

inverted_index = recovery.load_inverted_index(inverted_index_path)

documents = listaProdutos

user_query = name_item

ranked_results = recovery.search_inverted_index(user_query, inverted_index)

recovery.display_results(ranked_results, documents)
