from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv

# INSIDE FILTROS YOU PUT THE VACCANCIE KEYWORD YOU WANT TO SEARCH
filtros = ['ASSISTENTE', 'OPERADOR', 'GERAIS', 'SERVIÇOS']
cidades = ['CAMPINAS']

# THIS IS HOW WE PREPARE A FILE TO RECEIVE OUR EXTRACTED DATA
planilha = csv.writer(open('vagas.csv', 'w'))


def pegaVagas(paginasMax):

    count = 1
    total = 0

    for i in range(paginasMax):

        page = 'http://empregacampinas.com.br/categoria/vaga/page/' + \
            str(count)
        pageLoad = urlopen(page)
        pageCode = pageLoad.read()
        pageLoad.close()

        pageSoup = soup(pageCode, 'html.parser')
        vagas = pageSoup.findAll('div', {'class': 'col-lg-12'})

        # print(vagas) #FOR DEBUG ONLY, TO VERIFY THE HTML PAGE YOU'RE GETTING

        for vaga in vagas:
            try:
                vagaCargo = vaga.find('a', {'class': 'thumbnail'}).get('title')
                vagaLink = vaga.find('a', {'class': 'thumbnail'}).get('href')

                listaDinamica = vagaCargo.split()
                # print(listaDinamica)

                if any(cidade in cidades for cidade in listaDinamica):
                    if any(palavra in filtros for palavra in listaDinamica):
                        planilha.writerow([vagaCargo, vagaLink])
                        total += 1
                        print(vagaCargo)
                        # print(vagaLink + '\n')
            except:
                continue
        count += 1
    print(total, 'vagas foram encontradas. Boa sorte!')


# INSERT AMOUNT OF PAGES YOU WANT TO EXPLORE
pegaVagas(40)
