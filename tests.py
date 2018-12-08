from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# OBTIENE LAS CATEGORIAS DE LA A - Z
# url = 'https://www.azlyrics.com/'
# respuesta1 = urlopen(url)
# contenidoWeb1 = respuesta1.read()
# soup1 = BeautifulSoup(contenidoWeb1, 'html.parser')
#
# super_categorias = []
# for valor in soup1.find_all('a', attrs={'class': 'btn btn-menu'}):
#     a = valor.get("href")
#     a = a[2:]
#     super_categorias.append("https://"+a)
#
# print(super_categorias)


# OBTIENE EL LISTADO DE ARTISTAS EN UNA CATEGORIA A - Z

##*** PARA TODAS LAS CARTEGORIAS
#for cat in super_categorias:
#    respuesta1 = urlopen(cat)
#respuesta1 = urlopen('https://www.azlyrics.com/a.html')

##*** PARA UNA CATEGORIA
# artistas = []
#
# respuesta1 = urlopen('https://www.azlyrics.com/a.html')
# contenidoWeb1 = respuesta1.read()
# soup1 = BeautifulSoup(contenidoWeb1, 'html.parser')
#
# for section in soup1.find_all('a', attrs={'class': None}):
#     a = section.get("href")
#     artistas.append("https://www.azlyrics.com/"+a)
#
# print(artistas)

# OBTIENE EL LISTADO DE CANCIONES DE UN ARTISTA

##*** PARA TODAS LOS ARTISTAS
#for art in artistas:
#    respuesta1 = urlopen(art)

##*** PARA UN ARTISTA
canciones = []
respuesta1 = urlopen('https://www.azlyrics.com/a/a1.html')
contenidoWeb1 = respuesta1.read()
soup1 = BeautifulSoup(contenidoWeb1, 'html.parser')

for section in soup1.find_all('a', attrs={'target': "_blank"}):
    a = section.get("href")
    a = a[3:]
    canciones.append("https://www.azlyrics.com/"+a)

print(canciones)
i = 0
#OBTIENE LA LETRA DE UNA CANCIÓN
for can in canciones:
    i = i + 1
#url2 = 'https://www.azlyrics.com/lyrics/a1/bethefirsttobelieve.html'
    url2 = can
    file = open("C:/Users/CHUCHO/PycharmProjects/DataAnalytics/"+i+".txt", "w")
    respuesta = urlopen(url2)
    contenidoWeb = respuesta.read()
    soup = BeautifulSoup(contenidoWeb, 'html.parser')
    titulo = soup.find('div', attrs={'class': 'ringtone'}).findNext('b').contents[0]
    archivoFinal = "<TITULO>" + titulo + "</TITULO>"
    file.write(archivoFinal)
    file.write("<LYRICS>")

    for valor in soup.find_all('div', attrs={'class': None}):
       a = valor.text
       file.write(a)
    file.write("</LYRICS>")
    file.close()




#for cat in aux:
 #   print(cat)
  #  categorias.append(re.search(r'[\w\.-]+.[\w\.-]+.[\w\.-]+/[\w\.-]+.[\w\.-]', cat.str()))

#print(categorias)