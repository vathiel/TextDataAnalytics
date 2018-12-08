import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

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
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

documentos_originales = leer_documentos_originales()
for d in documentos_originales:
    texto = re.sub('[^A-Za-z ]+', '', (d['titulo'] + " " + re.sub('[\n]+', " ", d['texto']))).lower()
    limpiar_texto(texto)

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

