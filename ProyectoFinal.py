import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import math
from collections import Counter


def leer_documentos_originales():
    documentos_originales = []
    id_doc = 0;
    for carpeta in os.listdir("BigData/data"):
        print carpeta
        archivo = open("BigData/data/" + carpeta, "r")
        noticias = archivo.read()
        noticias = noticias.replace('LYRICS', 'TEXTO')
        doc_html = BeautifulSoup(noticias, "lxml")
        docs = doc_html.find_all('body')
        for k, doc in enumerate(docs):
            titulo = doc.find('titulo')
            texto = doc.find('texto')
            artista = doc.find('artist').text
            if titulo is not None:
                if texto is not None:
                    titulo = titulo.getText()
                    texto = texto.getText()
                    dic = {
                        "_id": id_doc,
                        "artista": artista,
                        "titulo": titulo,
                        "texto": texto
                    }
                    documentos_originales.append(dic)
                    id_doc += 1
        archivo.close()
    return documentos_originales


def limpiar_texto(texto, numeroCiclo):
    cadena = ""
    vector = []
    texto = re.sub('[^A-Za-z ]+', '', texto).lower()
    word_tokens = word_tokenize(texto)
    for word in word_tokens:
        if not word in stop_words:
            vector.append(word)
            big.append(word)
            cadena += word + " "
    c = Counter(vector)
    vectores[numeroCiclo] = c
    return cadena


def texto_limpio_busqueda(texto):
    cadena = ""
    texto = re.sub('[^A-Za-z ]+', '', texto).lower()
    word_tokens = word_tokenize(texto)
    for word in word_tokens:
        if not word in stop_words:
            cadena += word + " "
    return cadena.lower()


def limpiar_documentos(documentos_originales):
    id_doc = 0
    for d in documentos_originales:
        texto = re.sub('[^A-Za-z ]+', '', (d['titulo'] + " " + re.sub('[\n]+', " ", d['texto']))).lower()
        textoLimpio = limpiar_texto(texto, id_doc)
        documentos[id_doc] = {
            "texto": textoLimpio
        }
        id_doc += 1


# obtener diccionario
def obtener_diccionario():
    diccionario = {}
    id_ter = 0
    listas = dict.fromkeys(big).keys()
    for lista in listas:
        diccionario[id_ter] = lista
        id_ter += 1
    return diccionario


# indice invertido
def indice_invertido(diccionario, vectores):
    indice_invertido = {}
    for k, v in diccionario.items():
        indice_invertido[v] = []
        for a, b in vectores.items():
            if (v in b):
                indice_invertido[v].append(a)
    return indice_invertido




# Vectores normalizados
def normalizar(tf, D, dED):
    res = tf * math.log(D / dED, 10)
    return res


def normalizar_vectores(vectores, indice_invertido, D):
    norm_vectores = vectores
    for k, v in norm_vectores.items():
        for t, f in v.items():
            if indice_invertido[t] != '':
                ndocs = len(indice_invertido[t])
                v[t] = normalizar(f, D, ndocs)
    return norm_vectores


# normalizar q
def normalizar_q(q, indice_invertido, D):
    norm_q = q
    for t, f in norm_q.items():
        try:
            ndocs = len(indice_invertido[t])
            norm_q[t] = (normalizar(f, D, ndocs))
        except:
            continue
    return norm_q


# obtener documentos a comparar
def obtener_listadocs(norm_q, indice_invertido):
    docs_comparar = []
    for t, f in norm_q.items():
        try:
            for d in indice_invertido[t]:
                if d not in docs_comparar:
                    docs_comparar.append(d)
        except:
            continue
    return docs_comparar


# aplicar similitud coseno
import operator


def similitud_coseno(dj, q):
    res = 1
    dividendo = 0
    divisor = 0
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for k, v in diccionario.items():
        sum1 += (dj[v] * q[v])
        sum2 += dj[v] ** 2
        sum3 += q[v] ** 2
    dividendo = sum1
    divisor = math.sqrt(sum2) * math.sqrt(sum3)
    res = dividendo / divisor
    return res


# MAIN
stop_words = set(stopwords.words('english'))
big = []
documentos = {}
vectores = {}

documentos_originales = leer_documentos_originales()
limpiar_documentos(documentos_originales)
diccionario = obtener_diccionario()
D = len(diccionario)
indice_invertido = indice_invertido(diccionario, vectores)
norm_vectores = normalizar_vectores(vectores, indice_invertido, D)

palabras_consulta = raw_input("Ingrese palabras claves")
palabras_consulta = texto_limpio_busqueda(palabras_consulta)
q = Counter(palabras_consulta.split())
norm_q = normalizar_q(q, indice_invertido, D)
docs_comparar = obtener_listadocs(norm_q, indice_invertido)

r = {}
for d in docs_comparar:
    dj = norm_vectores[d]
    p = similitud_coseno(dj, norm_q)
    r[d] = p
res = sorted(r.items(), key=operator.itemgetter(1))
res.reverse()
nres = len(res)
print ("Se han encontrado " + str(nres) + " resultados: ")
for k, v in res:
    print ("Documento " + str(k) + " : " + str(round(v, 2)))
    print ("Artista: " + str(documentos_originales[k]["artista"]))
    print ("Titulo: " + str(documentos_originales[k]["titulo"] +"\n"))

