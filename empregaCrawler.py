from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
import csv

# INSIDE FILTROS YOU PUT THE VACCANCIES KEYWORD YOU WANT TO SEARCH
filtros = ['BEBIDAS', 'ASSISTENTE', 'VENDEDOR', 'OPERADOR', 'GERAIS', 'SERVIÇOS', 'SEPARADOR', 'PORTEIRO']


# THIS IS HOW WE PREPARE A FILE TO RECEIVE OUR EXTRACTED DATA
# planilha = csv.writer(open('vagas.csv', 'w')) # old method


def pega_vagas(paginas_max):
    count = 1
    total = 0
    vagas_dict = {}

    for i in range(paginas_max):

        page = 'http://empregacampinas.com.br/categoria/vaga/page/{0}'.format(str(count))
        page_load = urlopen(page)
        page_code = page_load.read()
        page_load.close()

        page_soup = Soup(page_code, 'html.parser')
        vagas = page_soup.findAll('div', {'class': 'col-lg-12'})

        # print(vagas) #FOR DEBUG ONLY, TO VERIFY THE HTML PAGE YOU'RE GETTING

        for vaga in vagas:
            try:
                vaga_cargo = vaga.find('a', {'class': 'thumbnail'}).get('title')
                vaga_link = vaga.find('a', {'class': 'thumbnail'}).get('href')

                lista_dinamica = vaga_cargo.split()

                if any(palavra in filtros for palavra in lista_dinamica):
                    vagas_dict[vaga_cargo] = vaga_link
                    total += 1
                    # print(vaga_cargo) #DEBUG ONLY
                    # print(vaga_link + '\n') #DEBUG ONLY
            except:
                continue
        count += 1
        print('{} vagas foram encontradas. Boa sorte!'.format(total))
        preenche_csv(vagas_dict)


def preenche_csv(dict_vagas):
    with open('vagas.csv', 'a', newline='') as planilha:
        preenche_planilha = csv.writer(planilha, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for key, value in dict_vagas.items():
            preenche_planilha.writerow([key, value])


if __name__ == "__main__":
    # INSERT AMOUNT OF PAGES YOU WANT TO EXPLORE
    pega_vagas(20)
