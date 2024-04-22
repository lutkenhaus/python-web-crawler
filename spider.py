import requests
from bs4 import BeautifulSoup
from utils import excel_utils as excel, user_utils as user, time_utils as time

listaProdutos = []
listaUrls = excel.read_spreadsheet_as_a_list("lista_urls")
allURLS = excel.read_spreadsheet_as_a_list("lista_urls")
listaUrls = listaUrls[0]

user.welcome()
contador = 0
while contador < 5:
    time.sleep(1)
    url_atual = listaUrls.pop()
    resposta = requests.get(url_atual)
    html_tratado = BeautifulSoup(resposta.content, "html.parser")

    produtosLinks = html_tratado.find_all(
        "a",
        class_="ui-search-item__group__element ui-search-link__title-card ui-search-link",
    )

    for link in produtosLinks:
        url_nova = link["href"]
        if "mercadolivre" in url_nova:
            listaUrls.append(url_nova)
            allURLS.append(url_nova)

    # se a URL atual for uma página de produto
    if url_atual.find("lista") == -1:
        produto = {}
        produto["nome"] = html_tratado.select_one(".ui-pdp-title").get_text()
        produto["preco"] = html_tratado.select_one(
            ".andes-money-amount__fraction"
        ).get_text()
        produto["url"] = url_atual
        listaProdutos.append(produto)
    print(contador)
    contador = contador + 1
print("SALVANDO...")
excel.save_new_spreadsheet(listaProdutos, "dados_coletados")
# excel.append_to_existing_spreadsheet(allURLS, "lista_urls")
