import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import math
from collections import Counter

# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
# License: BSD 3 clause

from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

def leer_documentos_originales():
    documentos_originales = []
    id_doc = 0;
    for carpeta in os.listdir("BigData/noticias"):
        print carpeta
        archivo = open("BigData/noticias/" + carpeta, "r")
        noticias = archivo.read()
        noticias = noticias.replace('BODY', 'TEXTO')
        doc_html = BeautifulSoup(noticias, "lxml")
        docs = doc_html.find_all('reuters')
        for k, doc in enumerate(docs):
            titulo = doc.title
            texto = doc.find('texto')
            if titulo is not None:
                if texto is not None:
                    titulo = titulo.getText()
                    texto = texto.getText()
                    dic = {
                        "_id": id_doc,
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
    textoImport.append(cadena)
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
        ndocs = len(indice_invertido[t])
        norm_q[t] = (normalizar(f, D, ndocs))
    return norm_q


# obtener documentos a comparar
def obtener_listadocs(norm_q, indice_invertido):
    docs_comparar = []
    for t, f in norm_q.items():
        for d in indice_invertido[t]:
            if d not in docs_comparar:
                docs_comparar.append(d)
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
textoImport =[]
documentos = {}
vectores = {}
n_samples = 2000
n_features = 1000
n_components = 10
n_top_words = 20

documentos_originales = leer_documentos_originales()
limpiar_documentos(documentos_originales)
diccionario = obtener_diccionario()
D = len(diccionario)
indice_invertido = indice_invertido(diccionario, vectores)
norm_vectores = normalizar_vectores(vectores, indice_invertido, D)

def buscar_noticia(palabras):
    palabras_consulta = texto_limpio_busqueda(palabras)
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
    i=0
    for k, v in  res:
        if  i<3:
            print ("Documento " + str(k) + " : " + str(round(v, 2)))
            print ("Titulo: " + str(documentos_originales[k]["titulo"]))
            text = documentos_originales[k]["texto"]
            print ("Texto: " + str(text[1:1000]))
            i+=1
        else:
            break

def limpiar_texto(texto):
    cadena = ""
    word_tokens = word_tokenize(texto)
    for word in word_tokens:
        if not word in stop_words and word.isalnum():
            cadena += word + " "
    textoImport.append(cadena)


# MAIN

stop_words = set(stopwords.words('english'))
textoImport =[]

n_samples = 2000
n_features = 1000
n_components = 100
n_top_words = 20



def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        palabras = " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        message += palabras
        print(message)
        buscar_noticia(palabras)
    print()


# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.


# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   max_features=n_features,
                                   stop_words='english')
t0 = time()

tfidf = tfidf_vectorizer.fit_transform(textoImport)


# Fit the NMF model
print("Fitting the NMF model (Frobenius norm) with tf-idf features, "
      "n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)

print("\nTopics in NMF model (Frobenius norm):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

# Fit the NMF model
print("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
      "tf-idf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

print("\nTopics in NMF model (generalized Kullback-Leibler divergence):")
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
print_top_words(nmf, tfidf_feature_names, n_top_words)

