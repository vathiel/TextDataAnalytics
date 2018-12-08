from urllib.request import urlopen
from bs4 import BeautifulSoup


# OBTIENE LAS CATEGORIAS DE LA A - Z
url = 'https://www.azlyrics.com/'
respuesta1 = urlopen(url)
contenidoWeb1 = respuesta1.read()
soup1 = BeautifulSoup(contenidoWeb1, 'html.parser')

super_categorias = []
for valor in soup1.find_all('a', attrs={'class': 'btn btn-menu'}):
    a = valor.get("href")
    a = a[2:]
    super_categorias.append("https://"+a)

print(super_categorias)


# OBTIENE EL LISTADO DE ARTISTAS EN UNA CATEGORIA A - Z

##*** PARA TODAS LAS CARTEGORIAS
#for cat in super_categorias:
#    respuesta1 = urlopen(cat)

##*** PARA UNA CATEGORIA
artistas = []

respuesta1 = urlopen('https://www.azlyrics.com/a.html')
contenidoWeb1 = respuesta1.read()
soup1 = BeautifulSoup(contenidoWeb1, 'html.parser')

for section in soup1.find_all('a', attrs={'class': None}):
    a = section.get("href")
    artistas.append("https://www.azlyrics.com/"+a)

print(artistas)

# OBTIENE EL LISTADO DE CANCIONES DE UN ARTISTA
canciones = []
##*** PARA TODAS LOS ARTISTAS
#for url in artistas:
#    respuesta1 = urlopen(url)

##*** PARA UN ARTISTA
url = 'https://www.azlyrics.com/a/aaliyah.html'
pos = url.rindex('/')
pos1 = url.rindex('.')
artist_name = url[pos+1:pos1]
print(artist_name)

respuesta1 = urlopen(url)
contenidoWeb1 = respuesta1.read()
soup1 = BeautifulSoup(contenidoWeb1, 'html.parser')

for section in soup1.find_all('a', attrs={'target': "_blank"}):
    a = section.get("href")
    a = a[3:]
    canciones.append("https://www.azlyrics.com/"+a)

print(canciones)

i = 0
##OBTIENE LA LETRA DE UNA CANCIÓN
for can in canciones:
    i = i + 1
    url2 = can
    file = open("C:/Users/CHUCHO/PycharmProjects/DataAnalytics/" + str(i) + ".txt", "w")
    respuesta = urlopen(url2)
    contenidoWeb = respuesta.read()
    soup = BeautifulSoup(contenidoWeb, 'html.parser')
    titulo = soup.find('div', attrs={'class': 'ringtone'}).findNext('b').contents[0]
    cantante = "<ARTIST>" + artist_name + "<d/ARTIST>"
    archivoFinal = "<TITULO>" + titulo + "</TITULO>"
    file.write(cantante + archivoFinal)
    file.write("<LYRICS>")

    for valor in soup.find_all('div', attrs={'class': None}):
       a = valor.text
       file.write(a)
    file.write("</LYRICS>")
    file.close()